package com.example.controller;

import cn.hutool.core.util.ObjectUtil;
import cn.hutool.core.util.StrUtil;
import com.example.common.Result;
import com.example.common.enums.ResultCodeEnum;
import com.example.common.enums.RoleEnum;
import com.example.entity.Account;
import com.example.service.AdminService;
import com.example.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;

/**
 * 基础前端接口
 */
@RestController
public class WebController {

    private static final Logger log = LoggerFactory.getLogger(WebController.class);

    @Resource
    private AdminService adminService;

    @Resource
    private UserService userService;

    @GetMapping("/")
    public Result hello() {
        return Result.success("访问成功");
    }

    /**
     * 登录
     *
     * @param account 用户登录信息
     * @return 登录结果
     */
    @PostMapping("/login")
    public Result login(@RequestBody Account account) {
        log.info("收到登录请求：username={}, role={}", account.getUsername(), account.getRole());
        
        // 检查参数是否为空
        if (ObjectUtil.isEmpty(account.getUsername()) || ObjectUtil.isEmpty(account.getPassword())
                || ObjectUtil.isEmpty(account.getRole())) {
            log.warn("登录参数缺失：username={}, role={}", account.getUsername(), account.getRole());
            return Result.error(ResultCodeEnum.PARAM_LOST_ERROR);
        }
        
        try {
            // 根据角色调用不同的登录服务
            if (RoleEnum.ADMIN.name().equals(account.getRole())) {
                log.info("管理员登录：{}", account.getUsername());
                account = adminService.login(account);
            } else if (RoleEnum.USER.name().equals(account.getRole())) {
                log.info("用户登录：{}", account.getUsername());
                account = userService.login(account);
            } else {
                log.warn("无效的角色类型：{}", account.getRole());
                return Result.error(ResultCodeEnum.PARAM_ERROR);
            }
            
            log.info("登录成功：username={}, role={}", account.getUsername(), account.getRole());
            return Result.success(account);
        } catch (Exception e) {
            log.error("登录失败：", e);
            return Result.error(ResultCodeEnum.USER_ACCOUNT_ERROR);
        }
    }

    /**
     * 注册
     *
     * @param account 用户注册信息
     * @return 注册结果
     */
    @PostMapping("/register")
    public Result register(@RequestBody Account account) {
        // 检查参数是否为空
        if (StrUtil.isBlank(account.getUsername()) || StrUtil.isBlank(account.getPassword())
                || ObjectUtil.isEmpty(account.getRole())) {
            return Result.error(ResultCodeEnum.PARAM_LOST_ERROR);
        }
        // 根据角色调用不同的注册服务
        if (RoleEnum.USER.name().equals(account.getRole())) {
            userService.register(account);
        } else {
            return Result.error(ResultCodeEnum.PARAM_ERROR);
        }
        return Result.success();
    }

    /**
     * 修改密码
     *
     * @param account 用户修改密码信息
     * @return 修改密码结果
     */
    @PutMapping("/updatePassword")
    public Result updatePassword(@RequestBody Account account) {
        // 检查参数是否为空
        if (StrUtil.isBlank(account.getUsername()) || StrUtil.isBlank(account.getPassword())
                || ObjectUtil.isEmpty(account.getNewPassword())) {
            return Result.error(ResultCodeEnum.PARAM_LOST_ERROR);
        }
        // 根据角色调用不同的修改密码服务
        if (RoleEnum.ADMIN.name().equals(account.getRole())) {
            adminService.updatePassword(account);
        } else if (RoleEnum.USER.name().equals(account.getRole())) {
            userService.updatePassword(account);
        }
        return Result.success();
    }

}

