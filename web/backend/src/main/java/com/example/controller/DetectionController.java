package com.example.controller;

import com.example.common.Result;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.*;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/detection")
public class DetectionController {
    private static final Logger logger = LoggerFactory.getLogger(DetectionController.class);

    @Value("${fastapi.url}")
    private String fastApiUrl;

    private final RestTemplate restTemplate;

    public DetectionController(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @PostMapping("/fish")
    public Result<Map<String, Object>> detectFish(@RequestParam("file") MultipartFile file) {
        logger.info("接收到鱼类检测请求");
        logger.info("文件名: {}", file.getOriginalFilename());
        logger.info("文件大小: {} bytes", file.getSize());
        logger.info("Content Type: {}", file.getContentType());

        try {
            // 保存上传的文件
            String fileName = UUID.randomUUID() + "_" + file.getOriginalFilename();
            Path tempPath = Files.createTempFile("upload_", fileName);
            file.transferTo(tempPath.toFile());
            logger.info("临时文件已创建: {}", tempPath);

            // 准备请求
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.MULTIPART_FORM_DATA);

            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            body.add("file", new FileSystemResource(tempPath.toFile()));

            HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
            logger.info("准备发送请求到FastAPI: {}", fastApiUrl + "/detect/fish");

            // 发送请求到 FastAPI
            ResponseEntity<Map> response = restTemplate.exchange(
                fastApiUrl + "/detect/fish",
                HttpMethod.POST,
                requestEntity,
                Map.class
            );
            logger.info("FastAPI响应状态: {}", response.getStatusCode());
            logger.info("FastAPI响应数据: {}", response.getBody());

            // 删除临时文件
            Files.deleteIfExists(tempPath);
            logger.info("临时文件已删除");

            return Result.success(response.getBody());
        } catch (Exception e) {
            logger.error("检测过程中发生错误", e);
            return Result.error("500", "检测失败：" + e.getMessage());
        }
    }

    @PostMapping("/shanhu")
    public Result<Map<String, Object>> detectShanhu(@RequestParam("file") MultipartFile file) {
        logger.info("接收到珊瑚检测请求");
        logger.info("文件名: {}", file.getOriginalFilename());
        logger.info("文件大小: {} bytes", file.getSize());
        logger.info("Content Type: {}", file.getContentType());

        try {
            // 保存上传的文件
            String fileName = UUID.randomUUID() + "_" + file.getOriginalFilename();
            Path tempPath = Files.createTempFile("upload_", fileName);
            file.transferTo(tempPath.toFile());
            logger.info("临时文件已创建: {}", tempPath);

            // 准备请求
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.MULTIPART_FORM_DATA);

            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            body.add("file", new FileSystemResource(tempPath.toFile()));

            HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
            logger.info("准备发送请求到FastAPI: {}", fastApiUrl + "/detect/shanhu");

            // 发送请求到 FastAPI
            ResponseEntity<Map> response = restTemplate.exchange(
                fastApiUrl + "/detect/shanhu",
                HttpMethod.POST,
                requestEntity,
                Map.class
            );
            logger.info("FastAPI响应状态: {}", response.getStatusCode());
            logger.info("FastAPI响应数据: {}", response.getBody());

            // 删除临时文件
            Files.deleteIfExists(tempPath);
            logger.info("临时文件已删除");

            return Result.success(response.getBody());
        } catch (Exception e) {
            logger.error("检测过程中发生错误", e);
            return Result.error("500", "检测失败：" + e.getMessage());
        }
    }

    @GetMapping("/image/{imageName}")
    public ResponseEntity<byte[]> getImage(@PathVariable String imageName) {
        logger.info("请求获取图片: {}", imageName);
        try {
            // 尝试从 FastAPI 获取图片
            ResponseEntity<byte[]> response = restTemplate.getForEntity(
                fastApiUrl + "/image/" + imageName,
                byte[].class
            );
            logger.info("成功获取图片，大小: {} bytes", response.getBody().length);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.IMAGE_JPEG);
            return new ResponseEntity<>(response.getBody(), headers, HttpStatus.OK);
        } catch (Exception e) {
            logger.error("获取图片失败", e);
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }
} 