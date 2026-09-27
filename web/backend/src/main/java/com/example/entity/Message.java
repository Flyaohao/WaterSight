package com.example.entity;

import java.util.Date;

/**
 * 消息通知实体类
 */
public class Message {
    private Integer id;
    private Integer userId;        // 接收消息的用户ID
    private String type;           // 消息类型：system(系统通知)、follow(被关注)、comment(被评论)、like(被点赞)、collect(被收藏)
    private String title;          // 消息标题
    private String content;        // 消息内容
    private Integer relatedId;     // 相关ID（如博客ID、评论ID等）
    private Boolean isRead;        // 是否已读
    private Date createTime;       // 创建时间
    private Integer fromUserId;    // 发送者ID
    private String fromUser;       // 发送者用户名
    private String targetType;     // 目标类型（blog/activity）
    private Integer targetId;      // 目标ID
    private String targetTitle;    // 目标标题

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getUserId() {
        return userId;
    }

    public void setUserId(Integer userId) {
        this.userId = userId;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public Integer getRelatedId() {
        return relatedId;
    }

    public void setRelatedId(Integer relatedId) {
        this.relatedId = relatedId;
    }

    public Boolean getIsRead() {
        return isRead;
    }

    public void setIsRead(Boolean isRead) {
        this.isRead = isRead;
    }

    public Date getCreateTime() {
        return createTime;
    }

    public void setCreateTime(Date createTime) {
        this.createTime = createTime;
    }

    public Integer getFromUserId() {
        return fromUserId;
    }

    public void setFromUserId(Integer fromUserId) {
        this.fromUserId = fromUserId;
    }

    public String getFromUser() {
        return fromUser;
    }

    public void setFromUser(String fromUser) {
        this.fromUser = fromUser;
    }

    public String getTargetType() {
        return targetType;
    }

    public void setTargetType(String targetType) {
        this.targetType = targetType;
    }

    public Integer getTargetId() {
        return targetId;
    }

    public void setTargetId(Integer targetId) {
        this.targetId = targetId;
    }

    public String getTargetTitle() {
        return targetTitle;
    }

    public void setTargetTitle(String targetTitle) {
        this.targetTitle = targetTitle;
    }
} 