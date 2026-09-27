package com.example.controller;

import com.example.common.Result;
import com.example.service.DatasetService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/dataset")
public class DatasetController {

    private final DatasetService datasetService;

    public DatasetController(DatasetService datasetService) {
        this.datasetService = datasetService;
    }

    @PostMapping("/preprocess")
    public ResponseEntity<Result<?>> preprocessDataset(@RequestParam("file") MultipartFile file, @RequestParam(value = "options", required = false) String options) {
        return datasetService.preprocessDataset(file, options);
    }

    @PostMapping("/datasetprocess")
    public Result<?> processDataset(@RequestParam("file") MultipartFile file, @RequestParam(value = "environment", required = false) String environment) {
        ResponseEntity<?> response = datasetService.processDataset(file, environment);
        if (response.getStatusCode().is2xxSuccessful()) {
            return Result.success(response.getBody());
        } else {
            return Result.error("500", "数据集处理失败");
        }
    }

    @GetMapping("/image/{imageName}")
    public ResponseEntity<byte[]> getImage(@PathVariable String imageName) {
        return datasetService.getImage(imageName);
    }
} 