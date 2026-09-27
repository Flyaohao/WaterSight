package com.example.common.config;

import cn.hutool.core.util.ObjectUtil;
import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.exceptions.JWTVerificationException;
import com.example.common.Constants;
import com.example.common.enums.ResultCodeEnum;
import com.example.common.enums.RoleEnum;
import com.example.entity.Account;
import com.example.exception.CustomException;
import com.example.service.AdminService;
import com.example.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * jwt拦截器
 */
@Component
public class JwtInterceptor implements HandlerInterceptor {

    private static final Logger log = LoggerFactory.getLogger(JwtInterceptor.class);

    @Resource
    private AdminService adminService;

    @Resource
    private UserService userService;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        String requestURI = request.getRequestURI();
        log.info("拦截器处理请求: {}", requestURI);

        // 检查是否是放行的路径
        if (isExcludedPath(requestURI)) {
            log.info("该路径已配置为放行: {}", requestURI);
            return true;
        }

        // 1. 从http请求的header中获取token
        String token = request.getHeader(Constants.TOKEN);
        if (ObjectUtil.isEmpty(token)) {
            // 如果没拿到，从参数里再拿一次
            token = request.getParameter(Constants.TOKEN);
        }
        // 2. 开始执行认证
        if (ObjectUtil.isEmpty(token)) {
            throw new CustomException(ResultCodeEnum.TOKEN_INVALID_ERROR.getCode(), ResultCodeEnum.TOKEN_INVALID_ERROR.getMsg());
        }
        Account account = null;
        String role = null;
        try {
            // 解析token获取存储的数据
            String userRole = JWT.decode(token).getAudience().get(0);
            String userId = userRole.split("-")[0];
            role = userRole.split("-")[1];
            // 根据userId查询数据库
            if (RoleEnum.ADMIN.name().equals(role)) {
                account = adminService.selectById(Integer.valueOf(userId));
            } else if (RoleEnum.USER.name().equals(role)) {
                account = userService.selectById(Integer.valueOf(userId));
            }
        } catch (Exception e) {
            throw new CustomException(ResultCodeEnum.TOKEN_CHECK_ERROR.getCode(), ResultCodeEnum.TOKEN_CHECK_ERROR.getMsg());
        }
        if (ObjectUtil.isNull(account)) {
            throw new CustomException(ResultCodeEnum.USER_NOT_EXIST_ERROR.getCode(), ResultCodeEnum.USER_NOT_EXIST_ERROR.getMsg());
        }
        try {
            // 用户密码加签验证 token
            JWTVerifier jwtVerifier = JWT.require(Algorithm.HMAC256(account.getPassword())).build();
            jwtVerifier.verify(token); // 验证token

            // 3. 检查请求路径与角色是否匹配
            if (requestURI.startsWith("/admin/") || requestURI.startsWith("/manager/")) {
                // 管理员接口只允许管理员访问
                if (!RoleEnum.ADMIN.name().equals(role)) {
                    log.warn("非管理员用户尝试访问管理员接口: {}", requestURI);
                    throw new CustomException(ResultCodeEnum.NO_AUTH_ERROR.getCode(), ResultCodeEnum.NO_AUTH_ERROR.getMsg());
                }
            } else if (requestURI.startsWith("/front/")) {
                // 前台接口允许所有已登录用户访问
                if (!RoleEnum.USER.name().equals(role) && !RoleEnum.ADMIN.name().equals(role)) {
                    log.warn("未登录用户尝试访问前台接口: {}", requestURI);
                    throw new CustomException(ResultCodeEnum.NO_AUTH_ERROR.getCode(), ResultCodeEnum.NO_AUTH_ERROR.getMsg());
                }
            } else if (requestURI.startsWith("/user/")) {
                // 用户接口允许管理员和普通用户访问
                if (!RoleEnum.USER.name().equals(role) && !RoleEnum.ADMIN.name().equals(role)) {
                    log.warn("未登录用户尝试访问用户接口: {}", requestURI);
                    throw new CustomException(ResultCodeEnum.NO_AUTH_ERROR.getCode(), ResultCodeEnum.NO_AUTH_ERROR.getMsg());
                }
            }
        } catch (JWTVerificationException e) {
            throw new CustomException(ResultCodeEnum.TOKEN_CHECK_ERROR.getCode(), ResultCodeEnum.TOKEN_CHECK_ERROR.getMsg());
        }
        return true;
    }

    private boolean isExcludedPath(String requestURI) {
        // 基础路径
        if (requestURI.equals("/") ||
            requestURI.equals("/login") ||
            requestURI.equals("/admin") ||
            requestURI.equals("/register") ||
            requestURI.equals("/error")) {
            return true;
        }

        // 文件相关路径
        if (requestURI.startsWith("/files/")) {
            return true;
        }

        // 公开接口
        if (requestURI.equals("/blog/selectPage") ||
            requestURI.equals("/blog/selectTop") ||
            requestURI.equals("/activity/selectPage") ||
            requestURI.equals("/activity/selectTop") ||
            requestURI.equals("/category/selectAll") ||
            requestURI.equals("/notice/selectAll") ||
            requestURI.equals("/user/refreshStats") ||
            requestURI.equals("/user/updateBrowseRole") ||
            requestURI.equals("/user/login")) {
            return true;
        }

        return false;
    }
}