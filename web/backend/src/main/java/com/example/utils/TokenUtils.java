package com.example.utils;

import cn.hutool.core.date.DateUtil;
import cn.hutool.core.util.ObjectUtil;
import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.example.common.Constants;
import com.example.common.enums.RoleEnum;
import com.example.entity.Account;
import com.example.service.AdminService;
import com.example.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import javax.annotation.PostConstruct;
import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import java.util.Date;

/**
 * Token工具类
 */
@Component
// 将当前类初始化到spring容器中
public class TokenUtils {

    // 日志记录
    private static final Logger log = LoggerFactory.getLogger(TokenUtils.class);

    // 静态变量用于存储service，方便调用service方法
    private static AdminService staticAdminService;
    private static UserService staticUserService;

    // 注入service 依赖注入
    @Resource
    AdminService adminService;

    @Resource
    UserService userService;

    // 将service注入到静态变量中,用于初始化静态变量
    @PostConstruct
    public void setUserService() {
        staticAdminService = adminService;
        staticUserService = userService;
    }

    /**
     *
     * 1. 静态方法的需求
     * TokenUtils 类中的 createToken 和 getCurrentUser 方法都是静态方法。
     * 静态方法属于类而不是实例，因此它们不能直接访问类的非静态成员（如 adminService 和 userService）。
     * 2. 依赖注入的问题
     * Spring 框架通过依赖注入（DI）机制将 AdminService 和 UserService 注入到 TokenUtils 类的实例中。
     * 但是，静态方法无法直接访问这些通过依赖注入设置的实例变量。
     * 3. 解决方案
     * 通过定义静态变量 staticAdminService 和 staticUserService，
     * 并在类初始化时将实例变量的值赋给静态变量，这样静态方法就可以访问这些服务了。
     *
     * **/

    /**
     * 生成token
     * @param data  用户id-角色
     *              1-admin
     * @param sign  加密的密钥，用于签名，防止数据泄露
     * @return 生成的token字符串
     */
    public static String createToken(String data, String sign) {
        // 创建一个JWT对象
        return JWT.create()
                // 将用户id-角色作为受众添加到JWT中
                .withAudience(data)
                // 设置token的过期时间为当前时间的24小时后
                .withExpiresAt(DateUtil.offsetHour(new Date(), 24))
                // 使用HMAC256算法和指定的密钥对token进行签名
                .sign(Algorithm.HMAC256(sign));
    }


    /**
     * 从请求头中获取 token，并解析出当前登录的用户信息。
     *
     * @return 当前登录的用户信息，如果获取失败则返回一个空的账号对象
     */
    public static Account getCurrentUser() {
        try {
            // 从 RequestContextHolder 中获取 HttpServletRequest 对象
            HttpServletRequest request = ((ServletRequestAttributes) RequestContextHolder.getRequestAttributes()).getRequest();
            // 从请求头中获取 token
            String token = request.getHeader(Constants.TOKEN);
            if (ObjectUtil.isNotEmpty(token)) {
                // 解码 token 获取受众信息
                String userRole = JWT.decode(token).getAudience().get(0);
                // 从受众信息中分割出用户 ID 和角色
                String userId = userRole.split("-")[0];  // 获取用户id
                String role = userRole.split("-")[1];    // 获取角色
                // 根据角色调用不同的服务获取用户信息
                if (RoleEnum.ADMIN.name().equals(role)) {
                    return staticAdminService.selectById(Integer.valueOf(userId));
                } else if (RoleEnum.USER.name().equals(role)) {
                    return staticUserService.selectById(Integer.valueOf(userId));
                }
            }
        } catch (Exception e) {
            // 捕获异常并记录错误信息
            log.error("获取当前用户信息出错", e);
        }
        // 返回空的账号对象
        return new Account();
    }

}

