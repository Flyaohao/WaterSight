package com.example.service.impl;

import com.example.entity.Follow;
import com.example.entity.User;
import com.example.mapper.FollowMapper;
import com.example.mapper.UserMapper;
import com.example.service.FollowService;
import com.example.service.MessageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class FollowServiceImpl implements FollowService {

    @Autowired
    private FollowMapper followMapper;

    @Autowired
    private UserMapper userMapper;

    @Autowired
    private MessageService messageService;

    @Override
    @Transactional
    public boolean follow(Integer followerId, Integer followedId) {
        System.out.println("开始执行关注操作: followerId=" + followerId + ", followedId=" + followedId);
        
        try {
            // 检查是否已经关注
            int checkResult = followMapper.checkFollow(followerId, followedId);
            System.out.println("检查是否已关注结果: " + checkResult);
            
            if (checkResult > 0) {
                System.out.println("已经关注过，不能重复关注");
                return false; // 已经关注了，不能重复关注
            }

            // 创建关注关系
            Follow follow = new Follow();
            follow.setFollowerId(followerId);
            follow.setFollowedId(followedId);

            try {
                // 插入关注记录
                System.out.println("准备插入关注记录...");
                followMapper.insert(follow);
                System.out.println("关注记录插入成功");
                
                // 更新关注者的关注计数
                System.out.println("准备更新关注者的关注计数...");
                followMapper.increaseFollowCount(followerId);
                System.out.println("更新关注者计数成功");
                
                // 更新被关注者的粉丝计数
                System.out.println("准备更新被关注者的粉丝计数...");
                followMapper.increaseFansCount(followedId);
                System.out.println("更新被关注者计数成功");
                
                // 发送关注消息通知
                User follower = userMapper.selectById(followerId);
                if (follower != null) {
                    messageService.createFollowMessage(followerId, follower.getName(), followedId);
                }
                
                System.out.println("关注操作全部完成，返回成功");
                return true;
            } catch (Exception e) {
                System.err.println("关注操作过程中发生异常: " + e.getMessage());
                e.printStackTrace();
                throw e; // 重新抛出异常，让事务回滚
            }
        } catch (Exception e) {
            System.err.println("关注操作的外层捕获到异常: " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }

    @Override
    @Transactional
    public boolean unfollow(Integer followerId, Integer followedId) {
        System.out.println("开始执行取消关注操作: followerId=" + followerId + ", followedId=" + followedId);
        
        try {
            // 检查是否已关注
            int checkResult = followMapper.checkFollow(followerId, followedId);
            System.out.println("检查是否已关注结果: " + checkResult);
            
            if (checkResult == 0) {
                System.out.println("未关注，不能取消关注");
                return false; // 未关注，不能取消关注
            }

            // 创建关注关系对象用于删除
            Follow follow = new Follow();
            follow.setFollowerId(followerId);
            follow.setFollowedId(followedId);

            try {
                // 删除关注记录
                System.out.println("准备删除关注记录...");
                followMapper.delete(follow);
                System.out.println("关注记录删除成功");
                
                // 更新关注者的关注计数
                System.out.println("准备更新关注者的关注计数...");
                followMapper.decreaseFollowCount(followerId);
                System.out.println("更新关注者计数成功");
                
                // 更新被关注者的粉丝计数
                System.out.println("准备更新被关注者的粉丝计数...");
                followMapper.decreaseFansCount(followedId);
                System.out.println("更新被关注者计数成功");
                
                System.out.println("取消关注操作全部完成，返回成功");
                return true;
            } catch (Exception e) {
                System.err.println("取消关注操作过程中发生异常: " + e.getMessage());
                e.printStackTrace();
                throw e; // 重新抛出异常，让事务回滚
            }
        } catch (Exception e) {
            System.err.println("取消关注操作的外层捕获到异常: " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }

    @Override
    public boolean checkFollowStatus(Integer followerId, Integer followedId) {
        return followMapper.checkFollow(followerId, followedId) > 0;
    }

    @Override
    public Map<String, Object> getFollows(Integer userId, Integer pageNum, Integer pageSize) {
        // 计算偏移量
        int offset = (pageNum - 1) * pageSize;
        
        // 获取关注列表
        List<User> follows = followMapper.getFollows(userId, offset, pageSize);
        
        // 获取总数
        int total = followMapper.countFollows(userId);
        
        // 封装结果
        Map<String, Object> result = new HashMap<>();
        result.put("records", follows);
        result.put("total", total);
        
        return result;
    }

    @Override
    public Map<String, Object> getFans(Integer userId, Integer pageNum, Integer pageSize) {
        // 计算偏移量
        int offset = (pageNum - 1) * pageSize;
        
        // 获取粉丝列表
        List<User> fans = followMapper.getFans(userId, offset, pageSize);
        
        // 获取总数
        int total = followMapper.countFans(userId);
        
        // 封装结果
        Map<String, Object> result = new HashMap<>();
        result.put("records", fans);
        result.put("total", total);
        
        return result;
    }
} 