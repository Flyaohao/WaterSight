package com.example.service.impl;

import com.example.service.DetectionService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.util.HashMap;
import java.util.Map;

@Service
public class DetectionServiceImpl implements DetectionService {
    
    @Value("${fastapi.url}")
    private String FASTAPI_URL;
    
    private final RestTemplate restTemplate;

    public DetectionServiceImpl(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @Override
    public ResponseEntity<Map<String, Object>> detectFish(MultipartFile file) {
        return forwardDetectionRequest(file, "/detect/fish");
    }

    @Override
    public ResponseEntity<Map<String, Object>> detectCoral(MultipartFile file) {
        return forwardDetectionRequest(file, "/detect/shanhu");
    }

    @Override
    public ResponseEntity<byte[]> getImage(String imagePath) {
        try {
            // 从FastAPI获取图片
            byte[] imageBytes = restTemplate.getForObject(FASTAPI_URL + imagePath, byte[].class);
            return ResponseEntity.ok()
                .contentType(MediaType.IMAGE_JPEG)
                .body(imageBytes);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
    }

    private ResponseEntity<Map<String, Object>> forwardDetectionRequest(MultipartFile file, String endpoint) {
        try {
            // 构建MultipartFile请求
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.MULTIPART_FORM_DATA);
            
            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            body.add("file", new ByteArrayResource(file.getBytes()) {
                @Override
                public String getFilename() {
                    return file.getOriginalFilename();
                }
            });

            HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
            
            // 发送请求到FastAPI
            ResponseEntity<Map<String, Object>> response = restTemplate.exchange(
                FASTAPI_URL + endpoint,
                HttpMethod.POST,
                requestEntity,
                new ParameterizedTypeReference<Map<String, Object>>() {},
                (Object[]) null
            );

            // 打印FastAPI返回的原始数据
            System.out.println("FastAPI返回数据: " + response.getBody());

            // 确保返回的数据结构正确
            Map<String, Object> responseBody = response.getBody();
            if (responseBody != null) {
                Map<String, Object> result = new HashMap<>();
                result.put("detections", responseBody.get("detections"));
                result.put("details", responseBody.get("details"));
                result.put("original", responseBody.get("original"));
                result.put("result", responseBody.get("result"));
                return ResponseEntity.ok(result);
            } else {
                throw new RuntimeException("FastAPI返回的数据为空");
            }
        } catch (Exception e) {
            e.printStackTrace();
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("error", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(errorResponse);
        }
    }
} 