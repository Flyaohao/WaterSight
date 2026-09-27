package com.example.service.impl;

import cn.hutool.core.date.DateUtil;
import com.example.common.enums.LikesModuleEnum;
import com.example.common.enums.RoleEnum;
import com.example.entity.*;
import com.example.mapper.ActivityMapper;
import com.example.service.ActivityService;
import com.example.service.ActivitySignService;
import com.example.service.CollectService;
import com.example.service.LikesService;
import com.example.utils.TokenUtils;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.Date;
import java.util.List;
import java.util.stream.Collectors;
import java.util.ArrayList;

/**
 * 活动信息业务处理实现类
 **/
@Service
public class ActivityServiceImpl implements ActivityService {

    private static final Logger logger = LoggerFactory.getLogger(ActivityServiceImpl.class);

    @Resource
    private ActivityMapper activityMapper;

    @Resource
    private ActivitySignService activitySignService;

    @Resource
    private LikesService likesService;

    @Resource
    private CollectService collectService;

    /**
     * 新增
     */
    public void add(Activity activity) {
        activityMapper.insert(activity);
    }

    /**
     * 删除
     */
    public void deleteById(Integer id) {
        activityMapper.deleteById(id);
    }

    /**
     * 批量删除
     */
    public void deleteBatch(List<Integer> ids) {
        for (Integer id : ids) {
            activityMapper.deleteById(id);
        }
    }

    /**
     * 修改
     */
    public void updateById(Activity activity) {
        activityMapper.updateById(activity);
    }

    /**
     * 根据ID查询
     */
    public Activity selectById(Integer id) {
        Activity activity = activityMapper.selectById(id);
        this.setAct(activity, TokenUtils.getCurrentUser());

        int likesCount = likesService.selectByFidAndModule(id, LikesModuleEnum.ACTIVITY.getValue());
        int collectCount = collectService.selectByFidAndModule(id, LikesModuleEnum.ACTIVITY.getValue());
        activity.setLikesCount(likesCount);
        activity.setCollectCount(collectCount);

        Likes likes = likesService.selectUserLikes(id, LikesModuleEnum.ACTIVITY.getValue());
        activity.setIsLike(likes != null);

        Collect collect = collectService.selectUserCollect(id, LikesModuleEnum.ACTIVITY.getValue());
        activity.setIsCollect(collect != null);
        return activity;
    }

    /**
     * 查询所有
     */
    public List<Activity> selectAll(Activity activity) {
        return activityMapper.selectAll(activity);
    }

    /**
     * 分页查询
     */
    @Override
    public PageInfo<Activity> selectPage(Activity activity, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum, pageSize);
        List<Activity> list = activityMapper.selectAll(activity);
        PageInfo<Activity> pageInfo = PageInfo.of(list);
        List<Activity> activityList = pageInfo.getList();
        Account currentUser = TokenUtils.getCurrentUser();
        for (Activity act : activityList) {
            this.setAct(act, currentUser);
        }
        return pageInfo;
    }
    
    /**
     * 根据状态筛选活动
     */
    @Override
    public PageInfo<Activity> selectByStatus(Activity activity, String status, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum, pageSize);
        
        Date currentDate = new Date();
        List<Activity> list;
        
        switch (status) {
            case "ongoing":
                list = activityMapper.selectOngoing(activity, currentDate);
                break;
            case "upcoming":
                list = activityMapper.selectUpcoming(activity, currentDate);
                break;
            case "ended":
                list = activityMapper.selectEnded(activity, currentDate);
                break;
            default:
                list = activityMapper.selectAll(activity);
                break;
        }
        
        PageInfo<Activity> pageInfo = PageInfo.of(list);
        List<Activity> activityList = pageInfo.getList();
        Account currentUser = TokenUtils.getCurrentUser();
        for (Activity act : activityList) {
            this.setAct(act, currentUser);
        }
        
        return pageInfo;
    }
    
    /**
     * 获取即将开始的活动
     */
    @Override
    public List<Activity> getUpcomingActivities(Integer limit) {
        Date currentDate = new Date();
        return activityMapper.selectUpcomingLimit(currentDate, limit);
    }
    
    /**
     * 热门活动
     */
    public List<Activity> selectTop() {
        List<Activity> activityList = this.selectAll(null);
        activityList = activityList.stream().sorted((b1, b2) -> b2.getReadCount().compareTo(b1.getReadCount()))
                .limit(2)
                .collect(Collectors.toList());
        return activityList;
    }

    /**
     * 更新阅读计数
     */
    public void updateReadCount(Integer activityId) {
        activityMapper.updateReadCount(activityId);
    }

    /**
     * 查询用户报名的活动列表
     */
    public PageInfo<Activity> selectUser(Activity activity, Integer pageNum, Integer pageSize) {
        try {
            System.out.println("ActivityService.selectUser - 传入参数:");
            System.out.println("  - 活动对象: " + activity);
            System.out.println("  - 用户ID: " + (activity != null ? activity.getUserId() : "null"));
            System.out.println("  - 页码: " + pageNum);
            System.out.println("  - 每页大小: " + pageSize);
            
            // 获取当前登录用户
            Account currentUser = TokenUtils.getCurrentUser();
            System.out.println("  - 当前登录用户: " + (currentUser != null ? currentUser.getId() : "null"));
            
            // URL传入的userId优先，只有在没有传递userId的情况下，才使用当前登录用户的ID
            if (activity.getUserId() == null && currentUser != null && RoleEnum.USER.name().equals(currentUser.getRole())) {
                activity.setUserId(currentUser.getId());
                System.out.println("  - 使用当前登录用户ID: " + currentUser.getId());
            } else {
                System.out.println("  - 使用URL传入的用户ID: " + activity.getUserId());
            }
            
            PageHelper.startPage(pageNum, pageSize);
            List<Activity> list = activityMapper.selectUser(activity);
            PageInfo<Activity> pageInfo = PageInfo.of(list);
            List<Activity> activityList = pageInfo.getList();
            
            System.out.println("  - 查询结果: " + (pageInfo != null ? pageInfo.getTotal() : 0) + " 条记录");
            
            if (activityList != null) {
                for (Activity act : activityList) {
                    if (act != null) {
                        this.setAct(act, currentUser);
                    }
                }
            }
            
            return pageInfo;
        } catch (Exception e) {
            logger.error("查询用户报名的活动列表失败", e);
            e.printStackTrace();
            return new PageInfo<>(new ArrayList<>());
        }
    }

    /**
     * 查询用户点赞的活动列表
     */
    public PageInfo<Activity> selectLike(Activity activity, Integer pageNum, Integer pageSize) {
        try {
            System.out.println("ActivityService.selectLike - 传入参数:");
            System.out.println("  - 活动对象: " + activity);
            System.out.println("  - 用户ID: " + (activity != null ? activity.getUserId() : "null"));
            
            // 获取当前登录用户
            Account currentUser = TokenUtils.getCurrentUser();
            System.out.println("  - 当前登录用户: " + (currentUser != null ? currentUser.getId() : "null"));
            
            // URL传入的userId优先，只有在没有传递userId的情况下，才使用当前登录用户的ID
            if (activity.getUserId() == null && currentUser != null && RoleEnum.USER.name().equals(currentUser.getRole())) {
                activity.setUserId(currentUser.getId());
                System.out.println("  - 使用当前登录用户ID: " + currentUser.getId());
            } else {
                System.out.println("  - 使用URL传入的用户ID: " + activity.getUserId());
            }
            
            PageHelper.startPage(pageNum, pageSize);
            List<Activity> list = activityMapper.selectLike(activity);
            PageInfo<Activity> pageInfo = PageInfo.of(list);
            List<Activity> activityList = pageInfo.getList();
            
            System.out.println("  - 查询结果: " + (pageInfo != null ? pageInfo.getTotal() : 0) + " 条记录");
            
            if (activityList != null) {
                for (Activity act : activityList) {
                    if (act != null) {
                        this.setAct(act, currentUser);
                    }
                }
            }
            
            return pageInfo;
        } catch (Exception e) {
            logger.error("查询用户点赞的活动列表失败", e);
            e.printStackTrace();
            return new PageInfo<>(new ArrayList<>());
        }
    }

    /**
     * 查询用户收藏的活动列表
     */
    public PageInfo<Activity> selectCollect(Activity activity, Integer pageNum, Integer pageSize) {
        try {
            System.out.println("ActivityService.selectCollect - 传入参数:");
            System.out.println("  - 活动对象: " + activity);
            System.out.println("  - 用户ID: " + (activity != null ? activity.getUserId() : "null"));
            
            // 获取当前登录用户
            Account currentUser = TokenUtils.getCurrentUser();
            System.out.println("  - 当前登录用户: " + (currentUser != null ? currentUser.getId() : "null"));
            
            // URL传入的userId优先，只有在没有传递userId的情况下，才使用当前登录用户的ID
            if (activity.getUserId() == null && currentUser != null && RoleEnum.USER.name().equals(currentUser.getRole())) {
                activity.setUserId(currentUser.getId());
                System.out.println("  - 使用当前登录用户ID: " + currentUser.getId());
            } else {
                System.out.println("  - 使用URL传入的用户ID: " + activity.getUserId());
            }
            
            PageHelper.startPage(pageNum, pageSize);
            List<Activity> list = activityMapper.selectCollect(activity);
            PageInfo<Activity> pageInfo = PageInfo.of(list);
            List<Activity> activityList = pageInfo.getList();
            
            System.out.println("  - 查询结果: " + (pageInfo != null ? pageInfo.getTotal() : 0) + " 条记录");
            
            if (activityList != null) {
                for (Activity act : activityList) {
                    if (act != null) {
                        this.setAct(act, currentUser);
                    }
                }
            }
            
            return pageInfo;
        } catch (Exception e) {
            logger.error("查询用户收藏的活动列表失败", e);
            e.printStackTrace();
            return new PageInfo<>(new ArrayList<>());
        }
    }

    /**
     * 查询用户评论的活动列表
     */
    public PageInfo<Activity> selectComment(Activity activity, Integer pageNum, Integer pageSize) {
        try {
            System.out.println("ActivityService.selectComment - 传入参数:");
            System.out.println("  - 活动对象: " + activity);
            System.out.println("  - 用户ID: " + (activity != null ? activity.getUserId() : "null"));
            
            // 获取当前登录用户
            Account currentUser = TokenUtils.getCurrentUser();
            System.out.println("  - 当前登录用户: " + (currentUser != null ? currentUser.getId() : "null"));
            
            // URL传入的userId优先，只有在没有传递userId的情况下，才使用当前登录用户的ID
            if (activity.getUserId() == null && currentUser != null && RoleEnum.USER.name().equals(currentUser.getRole())) {
                activity.setUserId(currentUser.getId());
                System.out.println("  - 使用当前登录用户ID: " + currentUser.getId());
            } else {
                System.out.println("  - 使用URL传入的用户ID: " + activity.getUserId());
            }
            
            PageHelper.startPage(pageNum, pageSize);
            List<Activity> list = activityMapper.selectComment(activity);
            PageInfo<Activity> pageInfo = PageInfo.of(list);
            List<Activity> activityList = pageInfo.getList();
            
            System.out.println("  - 查询结果: " + (pageInfo != null ? pageInfo.getTotal() : 0) + " 条记录");
            
            if (activityList != null) {
                for (Activity act : activityList) {
                    if (act != null) {
                        this.setAct(act, currentUser);
                    }
                }
            }
            
            return pageInfo;
        } catch (Exception e) {
            logger.error("查询用户评论的活动列表失败", e);
            e.printStackTrace();
            return new PageInfo<>(new ArrayList<>());
        }
    }

    // 设置活动额外信息
    private void setAct(Activity act, Account currentUser) {
        if (act == null) return;
        
        try {
            act.setIsEnd(DateUtil.parseDate(act.getEnd()).isBefore(new Date()));
            
            if (currentUser == null || currentUser.getId() == null) {
                act.setIsSign(false);
                return;
            }
            
            ActivitySign activitySign = activitySignService.selectByActivityIdAndUserId(act.getId(), currentUser.getId());
            act.setIsSign(activitySign != null);
        } catch (Exception e) {
            logger.error("设置活动额外信息失败", e);
            act.setIsSign(false);
            act.setIsEnd(false);
        }
    }
} 