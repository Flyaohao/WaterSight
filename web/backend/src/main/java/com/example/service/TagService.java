package com.example.service;

import java.util.List;
import java.util.Map;

public interface TagService {
   
   /**
    * 查找热门标签
    * @param limit 限制返回的标签数量
    * @return 热门标签列表及其对应的博客数量
    */
   List<Map<String, Object>> findHotTags(int limit);
   
   // 其他标签相关服务方法...
}
   
