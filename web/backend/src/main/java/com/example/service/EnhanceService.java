package com.example.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;

@Service
public class EnhanceService {

    private static final Logger logger = LoggerFactory.getLogger(EnhanceService.class);

    @Value("${enhance.url}")
    private String enhanceServiceUrl;

    private final RestTemplate restTemplate;

    public EnhanceService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
        logger.info("EnhanceService已初始化，FastAPI服务URL: {}", enhanceServiceUrl);
    }

    public ResponseEntity<?> enhanceImage(MultipartFile file) {
        logger.info("开始处理图像增强请求，文件名: {}, 大小: {} bytes", 
                file.getOriginalFilename(), file.getSize());
        
        try {
            // 构建请求URL
            String apiUrl = enhanceServiceUrl + "/api/enhance/image";
            URI uri = new URI(apiUrl);
            logger.info("请求FastAPI服务URL: {}", apiUrl);

            // 准备请求头
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.MULTIPART_FORM_DATA);

            // 准备请求体 - 创建包含文件的multipart请求
            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            ByteArrayResource fileResource = new ByteArrayResource(file.getBytes()) {
                @Override
                public String getFilename() {
                    return file.getOriginalFilename();
                }
            };
            body.add("file", fileResource);

            // 创建请求实体
            HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);

            // 发送请求并获取响应
            logger.info("发送请求到FastAPI服务...");
            
            // 直接使用Object类型接收，避免类型转换错误
            ResponseEntity<String> response = restTemplate.exchange(
                    uri,
                    HttpMethod.POST,
                    requestEntity,
                    String.class
            );
            
            logger.info("收到FastAPI响应，状态码: {}, 内容: {}", response.getStatusCode(), response.getBody());
            
            // 直接返回FastAPI的响应内容，不做额外处理
            HttpHeaders responseHeaders = new HttpHeaders();
            responseHeaders.setContentType(MediaType.APPLICATION_JSON);
            
            return ResponseEntity
                    .status(response.getStatusCode())
                    .headers(responseHeaders)
                    .body(response.getBody());
            
        } catch (RestClientException e) {
            logger.error("与FastAPI服务通信失败", e);
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body("无法连接到图像增强服务: " + e.getMessage());
        } catch (IOException e) {
            logger.error("文件处理错误", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("文件处理错误: " + e.getMessage());
        } catch (URISyntaxException e) {
            logger.error("URI语法错误", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("URI语法错误: " + e.getMessage());
        } catch (Exception e) {
            logger.error("图像增强处理未知错误", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("图像增强处理失败: " + e.getMessage());
        }
    }

    public ResponseEntity<byte[]> getImage(String imageName) {
        logger.info("获取增强后的图像: {}", imageName);
        
        try {
            // 构建请求URL - 假设图像是通过静态资源路径提供的
            String imageUrl = enhanceServiceUrl + "/static/images/enhanced/" + imageName;
            URI uri = new URI(imageUrl);
            logger.info("请求图像URL: {}", imageUrl);

            // 获取图像数据
            ResponseEntity<byte[]> response = restTemplate.getForEntity(uri, byte[].class);
            logger.info("图像获取成功，状态码: {}, 内容长度: {}", 
                    response.getStatusCode(), 
                    response.getBody() != null ? response.getBody().length : "unknown");

            // 设置响应头
            HttpHeaders headers = new HttpHeaders();
            // 根据图像名称后缀设置内容类型
            if (imageName.toLowerCase().endsWith(".png")) {
                headers.setContentType(MediaType.IMAGE_PNG);
            } else if (imageName.toLowerCase().endsWith(".jpg") || 
                      imageName.toLowerCase().endsWith(".jpeg")) {
                headers.setContentType(MediaType.IMAGE_JPEG);
            } else {
                headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);
            }
            
            // 返回带有图像的响应
            return new ResponseEntity<>(response.getBody(), headers, HttpStatus.OK);
            
        } catch (RestClientException e) {
            logger.error("获取图像失败", e);
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        } catch (URISyntaxException e) {
            logger.error("图像URI语法错误", e);
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        } catch (Exception e) {
            logger.error("获取图像未知错误", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
} 