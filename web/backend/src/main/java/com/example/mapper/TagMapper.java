package com.example.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import java.util.List;
import java.util.Map;

@Mapper
public interface TagMapper {
    /**
    * 查询热门标签
    * @param limit 限制返回的标签数量
    * @return 热门标签列表及其对应的博客数量
    */
   List<Map<String, Object>> selectHotTags(@Param("limit") int limit);
}
