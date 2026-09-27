package com.example.controller;

import com.example.common.Result;
import com.example.common.enums.ResultCodeEnum;
import com.example.service.FollowService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/follow")
public class FollowController {

    @Autowired
    private FollowService followService;

    /**
     * 关注用户
     * @param params 包含 followerId(关注者ID) 和 followedId(被关注者ID)
     * @return 操作结果
     */
    @PostMapping("/follow")
    public Result follow(@RequestBody Map<String, Object> params) {
        try {
            // 打印原始参数和类型
            System.out.println("关注请求原始参数: " + params);
            if (params.get("followerId") != null) {
                System.out.println("followerId类型: " + params.get("followerId").getClass().getName());
                System.out.println("followerId值: " + params.get("followerId"));
            }
            if (params.get("followedId") != null) {
                System.out.println("followedId类型: " + params.get("followedId").getClass().getName());
                System.out.println("followedId值: " + params.get("followedId"));
            }
            
            // 尝试获取并转换参数
            Integer followerId = null;
            Integer followedId = null;
            
            try {
                Object followerIdObj = params.get("followerId");
                Object followedIdObj = params.get("followedId");
                
                // 处理followerId
                if (followerIdObj instanceof Integer) {
                    followerId = (Integer) followerIdObj;
                } else if (followerIdObj instanceof String) {
                    followerId = Integer.parseInt((String) followerIdObj);
                } else if (followerIdObj instanceof Number) {
                    followerId = ((Number) followerIdObj).intValue();
                } else if (followerIdObj != null) {
                    followerId = Integer.valueOf(followerIdObj.toString());
                }
                
                // 处理followedId
                if (followedIdObj instanceof Integer) {
                    followedId = (Integer) followedIdObj;
                } else if (followedIdObj instanceof String) {
                    followedId = Integer.parseInt((String) followedIdObj);
                } else if (followedIdObj instanceof Number) {
                    followedId = ((Number) followedIdObj).intValue();
                } else if (followedIdObj != null) {
                    followedId = Integer.valueOf(followedIdObj.toString());
                }
            } catch (NumberFormatException e) {
                System.err.println("参数类型转换错误: " + e.getMessage());
                return Result.error("400", "参数类型错误: " + e.getMessage());
            }
            
            System.out.println("转换后的参数: followerId=" + followerId + ", followedId=" + followedId);

            if (followerId == null || followedId == null) {
                return Result.error("400", "缺少必要参数");
            }

            // 不能关注自己
            if (followerId.equals(followedId)) {
                return Result.error("400", "不能关注自己");
            }

            boolean success = followService.follow(followerId, followedId);
            if (success) {
                return Result.success();
            } else {
                return Result.error("400", "关注失败，可能已经关注过");
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.err.println("关注操作发生异常: " + e.getMessage());
            return Result.error("500", "系统异常: " + e.getMessage());
        }
    }

    /**
     * 取消关注
     * @param params 包含 followerId(关注者ID) 和 followedId(被关注者ID)
     * @return 操作结果
     */
    @PostMapping("/unfollow")
    public Result unfollow(@RequestBody Map<String, Object> params) {
        try {
            // 打印原始参数
            System.out.println("取消关注请求原始参数: " + params);
            
            // 尝试获取并转换参数
            Integer followerId = null;
            Integer followedId = null;
            
            try {
                Object followerIdObj = params.get("followerId");
                Object followedIdObj = params.get("followedId");
                
                // 处理followerId
                if (followerIdObj instanceof Integer) {
                    followerId = (Integer) followerIdObj;
                } else if (followerIdObj instanceof String) {
                    followerId = Integer.parseInt((String) followerIdObj);
                } else if (followerIdObj instanceof Number) {
                    followerId = ((Number) followerIdObj).intValue();
                } else if (followerIdObj != null) {
                    followerId = Integer.valueOf(followerIdObj.toString());
                }
                
                // 处理followedId
                if (followedIdObj instanceof Integer) {
                    followedId = (Integer) followedIdObj;
                } else if (followedIdObj instanceof String) {
                    followedId = Integer.parseInt((String) followedIdObj);
                } else if (followedIdObj instanceof Number) {
                    followedId = ((Number) followedIdObj).intValue();
                } else if (followedIdObj != null) {
                    followedId = Integer.valueOf(followedIdObj.toString());
                }
            } catch (NumberFormatException e) {
                System.err.println("参数类型转换错误: " + e.getMessage());
                return Result.error("400", "参数类型错误: " + e.getMessage());
            }

            if (followerId == null || followedId == null) {
                return Result.error("400", "缺少必要参数");
            }

            boolean success = followService.unfollow(followerId, followedId);
            if (success) {
                return Result.success();
            } else {
                return Result.error("400", "取消关注失败，可能未关注过");
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.err.println("取消关注操作发生异常: " + e.getMessage());
            return Result.error("500", "系统异常: " + e.getMessage());
        }
    }

    /**
     * 检查关注状态
     * @param followerId 关注者ID
     * @param followedId 被关注者ID
     * @return 是否已关注
     */
    @GetMapping("/checkStatus")
    public Result checkStatus(@RequestParam Integer followerId, @RequestParam Integer followedId) {
        if (followerId == null || followedId == null) {
            return Result.error("400", "缺少必要参数");
        }

        boolean isFollowing = followService.checkFollowStatus(followerId, followedId);
        return Result.success(isFollowing);
    }

    /**
     * 获取用户关注列表
     * @param userId 用户ID
     * @param pageNum 页码
     * @param pageSize 每页数量
     * @return 关注列表
     */
    @GetMapping("/getFollows")
    public Result getFollows(@RequestParam Integer userId,
                            @RequestParam(defaultValue = "1") Integer pageNum,
                            @RequestParam(defaultValue = "10") Integer pageSize) {
        if (userId == null) {
            return Result.error("400", "缺少必要参数");
        }

        Map<String, Object> follows = followService.getFollows(userId, pageNum, pageSize);
        return Result.success(follows);
    }

    /**
     * 获取用户粉丝列表
     * @param userId 用户ID
     * @param pageNum 页码
     * @param pageSize 每页数量
     * @return 粉丝列表
     */
    @GetMapping("/getFans")
    public Result getFans(@RequestParam Integer userId,
                         @RequestParam(defaultValue = "1") Integer pageNum,
                         @RequestParam(defaultValue = "10") Integer pageSize) {
        if (userId == null) {
            return Result.error("400", "缺少必要参数");
        }

        Map<String, Object> fans = followService.getFans(userId, pageNum, pageSize);
        return Result.success(fans);
    }

    /**
     * 测试关注功能，用于前端调试
     * @return 测试结果
     */
    @GetMapping("/test")
    public Result test() {
        System.out.println("测试关注功能API");
        return Result.success("关注API测试成功");
    }
} 