package com.example.controller;

import com.example.common.Result;
import com.example.service.TagService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/tag")
public class TagController {
    @Autowired
    private TagService tagService;
    
    @GetMapping("/getHotTags")
    public Result<List<Map<String, Object>>> getHotTags(@RequestParam(defaultValue = "5") int limit) {
        List<Map<String, Object>> hotTags = tagService.findHotTags(limit);
        return Result.success(hotTags);
    }
}
