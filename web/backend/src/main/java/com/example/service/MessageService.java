package com.example.service;

import com.example.entity.Account;
import com.example.entity.Message;
import com.example.entity.Blog;
import com.example.mapper.MessageMapper;
import com.example.utils.TokenUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.Date;
import java.util.List;

@Service
public class MessageService {

    private static final Logger logger = LoggerFactory.getLogger(MessageService.class);

    @Resource
    private MessageMapper messageMapper;

    /**
     * 新增消息
     */
    public void add(Message message) {
        logger.info("开始创建新消息: type={}, userId={}, title={}", message.getType(), message.getUserId(), message.getTitle());
        message.setCreateTime(new Date());
        message.setIsRead(false);
        try {
            messageMapper.insert(message);
            logger.info("消息创建成功: id={}, type={}, userId={}", message.getId(), message.getType(), message.getUserId());
        } catch (Exception e) {
            logger.error("消息创建失败: type={}, userId={}, error={}", message.getType(), message.getUserId(), e.getMessage());
            throw e;
        }
    }

    /**
     * 获取用户的所有消息
     */
    public List<Message> selectByUserId(Integer userId) {
        System.out.println("开始查询用户消息，用户ID: " + userId);
        List<Message> messages = messageMapper.selectByUserId(userId);
        System.out.println("查询到消息数量: " + messages.size());
        return messages;
    }

    /**
     * 获取用户的未读消息数量
     */
    public int getUnreadCount(Integer userId) {
        System.out.println("开始查询未读消息数量，用户ID: " + userId);
        int count = messageMapper.selectUnreadCount(userId);
        System.out.println("未读消息数量: " + count);
        return count;
    }

    /**
     * 标记消息为已读
     */
    public void markAsRead(Integer id) {
        messageMapper.updateReadStatus(id, true);
    }

    /**
     * 标记用户的所有消息为已读
     */
    public void markAllAsRead(Integer userId) {
        messageMapper.updateAllReadStatus(userId, true);
    }

    /**
     * 删除消息
     */
    public void deleteById(Integer id) {
        messageMapper.deleteById(id);
    }

    /**
     * 创建系统通知
     */
    public void createSystemMessage(Integer userId, String title, String content) {
        Message message = new Message();
        message.setUserId(userId);
        message.setType("系统通知");
        message.setTitle(title);
        message.setContent(content);
        add(message);
    }

    /**
     * 创建被关注通知
     */
    public void createFollowMessage(Integer userId, String username, Integer followedId) {
        logger.info("开始创建关注消息: userId={}, username={}, followedId={}", userId, username, followedId);
        Message message = new Message();
        message.setUserId(followedId);
        message.setType("关注");
        message.setTitle("收到新的关注");
        message.setFromUserId(userId);
        message.setFromUser(username);
        message.setContent(username + " 关注了你");
        add(message);
    }

    /**
     * 创建被评论通知
     */
    public void createCommentMessage(Integer userId, String username, Blog blog, String commentContent) {
        logger.info("开始创建评论消息: userId={}, username={}, blogId={}, content={}", userId, username, blog.getId(), commentContent);
        Message message = new Message();
        message.setUserId(blog.getUserId());
        message.setType("评论");
        message.setTitle("收到新的评论");
        message.setFromUserId(userId);
        message.setFromUser(username);
        message.setTargetType("blog");
        message.setTargetId(blog.getId());
        message.setTargetTitle(blog.getTitle());
        message.setContent(username + " 评论了你的博客: " + commentContent);
        add(message);
    }

    /**
     * 创建被点赞通知
     */
    public void createLikeMessage(Integer userId, String username, Blog blog) {
        logger.info("开始创建点赞消息: userId={}, username={}, blogId={}", userId, username, blog.getId());
        Message message = new Message();
        message.setUserId(blog.getUserId());
        message.setType("点赞");
        message.setTitle("收到新的点赞");
        message.setFromUserId(userId);
        message.setFromUser(username);
        message.setTargetType("blog");
        message.setTargetId(blog.getId());
        message.setTargetTitle(blog.getTitle());
        message.setContent(username + " 点赞了你的博客");
        add(message);
    }

    /**
     * 创建被收藏通知
     */
    public void createCollectMessage(Integer userId, String username, Blog blog) {
        logger.info("开始创建收藏消息: userId={}, username={}, blogId={}", userId, username, blog.getId());
        Message message = new Message();
        message.setUserId(blog.getUserId());
        message.setType("收藏");
        message.setTitle("收到新的收藏");
        message.setFromUserId(userId);
        message.setFromUser(username);
        message.setTargetType("blog");
        message.setTargetId(blog.getId());
        message.setTargetTitle(blog.getTitle());
        message.setContent(username + " 收藏了你的博客");
        add(message);
    }
} 