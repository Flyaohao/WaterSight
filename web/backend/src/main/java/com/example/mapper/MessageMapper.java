package com.example.mapper;

import com.example.entity.Message;
import org.apache.ibatis.annotations.Param;
import java.util.List;

public interface MessageMapper {
    /**
     * 新增消息
     */
    void insert(Message message);

    /**
     * 根据ID查询消息
     */
    Message selectById(Integer id);

    /**
     * 查询用户的所有消息
     */
    List<Message> selectByUserId(Integer userId);

    /**
     * 查询用户的未读消息数量
     */
    int selectUnreadCount(Integer userId);

    /**
     * 标记消息为已读
     */
    void updateReadStatus(@Param("id") Integer id, @Param("isRead") Boolean isRead);

    /**
     * 标记用户的所有消息为已读
     */
    void updateAllReadStatus(@Param("userId") Integer userId, @Param("isRead") Boolean isRead);

    /**
     * 删除消息
     */
    void deleteById(Integer id);
} 