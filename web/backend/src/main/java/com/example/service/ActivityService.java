package com.example.service;

import com.example.entity.Activity;
import com.github.pagehelper.PageInfo;

import java.util.List;

/**
 * 活动信息业务处理接口
 **/
public interface ActivityService {

    /**
     * 新增
     */
    void add(Activity activity);

    /**
     * 删除
     */
    void deleteById(Integer id);

    /**
     * 批量删除
     */
    void deleteBatch(List<Integer> ids);

    /**
     * 修改
     */
    void updateById(Activity activity);

    /**
     * 根据ID查询
     */
    Activity selectById(Integer id);

    /**
     * 查询所有
     */
    List<Activity> selectAll(Activity activity);

    /**
     * 分页查询
     */
    PageInfo<Activity> selectPage(Activity activity, Integer pageNum, Integer pageSize);
    
    /**
     * 根据状态筛选活动
     * @param activity 活动查询条件
     * @param status 活动状态 (ongoing, upcoming, ended)
     * @param pageNum 页码
     * @param pageSize 每页大小
     * @return 分页结果
     */
    PageInfo<Activity> selectByStatus(Activity activity, String status, Integer pageNum, Integer pageSize);
    
    /**
     * 获取即将开始的活动
     * @param limit 限制数量
     * @return 活动列表
     */
    List<Activity> getUpcomingActivities(Integer limit);
    
    /**
     * 热门活动
     */
    List<Activity> selectTop();

    /**
     * 更新阅读计数
     */
    void updateReadCount(Integer activityId);

    /**
     * 查询用户报名的活动列表
     */
    PageInfo<Activity> selectUser(Activity activity, Integer pageNum, Integer pageSize);

    /**
     * 查询用户点赞的活动列表
     */
    PageInfo<Activity> selectLike(Activity activity, Integer pageNum, Integer pageSize);

    /**
     * 查询用户收藏的活动列表
     */
    PageInfo<Activity> selectCollect(Activity activity, Integer pageNum, Integer pageSize);

    /**
     * 查询用户评论的活动列表
     */
    PageInfo<Activity> selectComment(Activity activity, Integer pageNum, Integer pageSize);
}