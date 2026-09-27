package com.example.service.impl;

import com.example.mapper.TagMapper;
import com.example.service.TagService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Map;

@Service
public class TagServiceImpl implements TagService {
    @Autowired
    private TagMapper tagMapper;
    
    @Override
    public List<Map<String, Object>> findHotTags(int limit) {
        return tagMapper.selectHotTags(limit);
    }
}
