package com.example.mapper;

import com.example.entity.User;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface UserMapper {

    void insert(User user);

    User selectByUsername(String username);

    void deleteById(Integer id);

    void updateById(User user);

    User selectById(Integer id);

    List<User> selectAll(User user);

    // 增加用户的博客数量
    void increaseBlogCount(@Param("userId") Integer userId);

    // 减少用户的博客数量
    void decreaseBlogCount(@Param("userId") Integer userId);

    // 增加用户的点赞数量
    void increaseLikesCount(@Param("userId") Integer userId);

    // 减少用户的点赞数量
    void decreaseLikesCount(@Param("userId") Integer userId);

    // 增加用户的收藏数量
    void increaseCollectCount(@Param("userId") Integer userId);

    // 减少用户的收藏数量
    void decreaseCollectCount(@Param("userId") Integer userId);

    // 根据用户真实姓名搜索
    List<User> searchByName(@Param("keyword") String keyword);
}
