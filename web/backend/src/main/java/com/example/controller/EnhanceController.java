package com.example.controller;

import com.example.common.Result;
import com.example.service.EnhanceService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/enhance")
public class EnhanceController {

    private static final Logger logger = LoggerFactory.getLogger(EnhanceController.class);
    private final EnhanceService enhanceService;

    public EnhanceController(EnhanceService enhanceService) {
        this.enhanceService = enhanceService;
    }

    @PostMapping("/image")
    public Result<?> enhanceImage(@RequestParam("file") MultipartFile file) {
        logger.info("接收到图像增强请求，文件名: {}, 文件大小: {} bytes", 
                file.getOriginalFilename(), file.getSize());
        
        try {
            ResponseEntity<?> response = enhanceService.enhanceImage(file);
            logger.info("FastAPI服务响应状态码: {}", response.getStatusCode());
            
            if (response.getStatusCode().is2xxSuccessful()) {
                logger.info("图像增强成功: {}", response.getBody());
                return Result.success(response.getBody());
            } else {
                logger.error("图像增强失败，状态码: {}, 响应: {}", 
                        response.getStatusCode(), response.getBody());
                return Result.error("500", "图像增强失败");
            }
        } catch (Exception e) {
            logger.error("图像增强处理异常", e);
            return Result.error("500", "图像增强处理异常: " + e.getMessage());
        }
    }

    @GetMapping("/image/{imageName}")
    public ResponseEntity<byte[]> getImage(@PathVariable String imageName) {
        logger.info("获取增强后的图像: {}", imageName);
        return enhanceService.getImage(imageName);
    }
} 