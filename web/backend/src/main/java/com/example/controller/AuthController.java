package com.example.controller;

import com.example.common.Result;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/auth")
public class AuthController {

    /**
     * 简单的 token 验证接口
     */
    @GetMapping("/check")
    public Result checkToken() {
        // 简单返回成功，不做任何处理
        return Result.success();
    }
}