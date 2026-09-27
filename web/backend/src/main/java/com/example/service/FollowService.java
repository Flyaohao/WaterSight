package com.example.service;

import com.example.entity.User;
import com.example.entity.Follow;
import com.example.utils.TokenUtils;
import com.example.service.MessageService;
import com.example.service.UserService;

import java.util.Date;
import java.util.List;
import java.util.Map;

public interface FollowService {

    /**
     * 关注用户
     *
     * @param followerId 关注者ID
     * @param followedId 被关注者ID
     * @return 是否成功
     */
    boolean follow(Integer followerId, Integer followedId);

    /**
     * 取消关注
     *
     * @param followerId 关注者ID
     * @param followedId 被关注者ID
     * @return 是否成功
     */
    boolean unfollow(Integer followerId, Integer followedId);

    /**
     * 检查是否已关注
     *
     * @param followerId 关注者ID
     * @param followedId 被关注者ID
     * @return 是否已关注
     */
    boolean checkFollowStatus(Integer followerId, Integer followedId);

    /**
     * 获取用户关注列表
     *
     * @param userId   用户ID
     * @param pageNum  页码
     * @param pageSize 每页数量
     * @return 关注列表和总数
     */
    Map<String, Object> getFollows(Integer userId, Integer pageNum, Integer pageSize);

    /**
     * 获取用户粉丝列表
     *
     * @param userId   用户ID
     * @param pageNum  页码
     * @param pageSize 每页数量
     * @return 粉丝列表和总数
     */
    Map<String, Object> getFans(Integer userId, Integer pageNum, Integer pageSize);
} 