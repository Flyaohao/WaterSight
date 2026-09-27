package com.example.service.impl;

import com.example.common.Result;
import com.example.service.DatasetService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.HashMap;
import java.util.Map;

@Service
public class DatasetServiceImpl implements DatasetService {
    
    private static final Logger logger = LoggerFactory.getLogger(DatasetServiceImpl.class);
    
    @Value("${dataset.url:http://localhost:8001}")
    private String DATASET_URL;
    
    private final RestTemplate restTemplate;

    public DatasetServiceImpl(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @Override
    public ResponseEntity<Result<?>> preprocessDataset(MultipartFile file, String options) {
        try {
            // 生成唯一的文件名
            String timestamp = String.valueOf(System.currentTimeMillis());
            String originalFilename = file.getOriginalFilename();
            String extension = originalFilename.substring(originalFilename.lastIndexOf("."));
            String filename = timestamp + extension;
            
            // 创建上传目录
            Path uploadDir = Paths.get("uploads");
            if (!Files.exists(uploadDir)) {
                Files.createDirectories(uploadDir);
            }
            
            // 保存文件
            Path filePath = uploadDir.resolve(filename);
            Files.copy(file.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);
            
            logger.info("文件已保存至: {}", filePath.toAbsolutePath());
            
            // 返回成功响应
            Map<String, Object> data = new HashMap<>();
            data.put("path", "./uploads/" + filename);
            data.put("message", "文件上传成功");
            
            return ResponseEntity.ok(Result.success(data));
        } catch (Exception e) {
            logger.error("预处理数据集失败", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Result.error("500", e.getMessage()));
        }
    }

    @Override
    public ResponseEntity<Result<?>> processDataset(MultipartFile file, String environment) {
        logger.info("开始处理数据集, 文件名: {}, 文件大小: {} bytes, 环境: {}", 
                file.getOriginalFilename(), file.getSize(), environment);
        
        Path tempFile = null;
        
        try {
            // 1. 保存上传的文件到临时目录
            String timestamp = String.valueOf(System.currentTimeMillis());
            String originalFilename = file.getOriginalFilename();
            tempFile = Files.createTempFile("dataset_" + timestamp + "_", originalFilename);
            file.transferTo(tempFile.toFile());
            
            logger.info("文件已保存至临时路径: {}", tempFile);
            
            // 2. 使用传入的环境参数，默认为深水环境
            if (environment == null || environment.isEmpty()) {
                environment = "deep"; // 默认环境
            }
            
            logger.info("使用环境参数: {}", environment);
            
            // 3. 准备向Python发送请求
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.MULTIPART_FORM_DATA);
            
            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            body.add("file", new FileSystemResource(tempFile.toFile()));
            body.add("environment", environment);
            
            HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
            
            logger.info("向Python服务发送请求: {}, 环境: {}", DATASET_URL + "/api/datasetprocess/process", environment);
            
            // 4. 发送请求到Python服务
            ResponseEntity<Map> response = restTemplate.exchange(
                DATASET_URL + "/api/datasetprocess/process",
                HttpMethod.POST,
                requestEntity,
                Map.class
            );
            
            logger.info("Python服务响应状态: {}", response.getStatusCode());
            
            // 5. 返回结果
            return ResponseEntity.ok(Result.success(response.getBody()));
            
        } catch (Exception e) {
            logger.error("处理数据集失败", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Result.error("500", "处理数据集失败: " + e.getMessage()));
        } finally {
            // 6. 清理临时文件
            if (tempFile != null) {
                try {
                    Files.deleteIfExists(tempFile);
                    logger.info("临时文件已删除: {}", tempFile);
                } catch (IOException e) {
                    logger.warn("删除临时文件失败: {}", tempFile, e);
                }
            }
        }
    }

    @Override
    public ResponseEntity<byte[]> getImage(String imagePath) {
        try {
            logger.info("获取图片: {}", DATASET_URL + imagePath);
            byte[] imageBytes = restTemplate.getForObject(DATASET_URL + imagePath, byte[].class);
            return ResponseEntity.ok()
                .contentType(MediaType.IMAGE_JPEG)
                .body(imageBytes);
        } catch (Exception e) {
            logger.error("获取图片失败: {}", imagePath, e);
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
    }
} 