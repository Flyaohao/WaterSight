package com.example.service;

import org.springframework.http.ResponseEntity;
import org.springframework.web.multipart.MultipartFile;

public interface DetectionService {
    ResponseEntity<?> detectFish(MultipartFile file);
    ResponseEntity<?> detectCoral(MultipartFile file);
    ResponseEntity<?> getImage(String imagePath);
} 