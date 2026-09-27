package com.example.service;

import com.example.common.Result;
import org.springframework.http.ResponseEntity;
import org.springframework.web.multipart.MultipartFile;

import java.util.Map;

public interface DatasetService {
    ResponseEntity<Result<?>> preprocessDataset(MultipartFile file, String options);
    ResponseEntity<Result<?>> processDataset(MultipartFile file, String environment);
    ResponseEntity<byte[]> getImage(String imagePath);
} 