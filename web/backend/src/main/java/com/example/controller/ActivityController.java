package com.example.controller;

import com.example.common.Result;
import com.example.entity.Activity;
import com.example.entity.Blog;
import com.example.service.ActivityService;
import com.github.pagehelper.PageInfo;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;
import javax.annotation.Resource;
import java.util.Date;
import java.util.List;

/**
 * 活动前端操作接口
 **/
@RestController
@RequestMapping("/activity")
public class ActivityController {

    private static final Logger logger = LoggerFactory.getLogger(ActivityController.class);

    @Resource
    private ActivityService activityService;

    /**
     * 新增
     */
    @PostMapping("/add")
    public Result add(@RequestBody Activity activity) {
        activityService.add(activity);
        return Result.success();
    }

    /**
     * 删除
     */
    @DeleteMapping("/delete/{id}")
    public Result deleteById(@PathVariable Integer id) {
        activityService.deleteById(id);
        return Result.success();
    }

    /**
     * 批量删除
     */
    @DeleteMapping("/delete/batch")
    public Result deleteBatch(@RequestBody List<Integer> ids) {
        activityService.deleteBatch(ids);
        return Result.success();
    }

    /**
     * 修改
     */
    @PutMapping("/update")
    public Result updateById(@RequestBody Activity activity) {
        activityService.updateById(activity);
        return Result.success();
    }

    @PutMapping("/updateReadCount/{activityId}")
    public Result updateReadCount(@PathVariable Integer activityId) {
        activityService.updateReadCount(activityId);
        return Result.success();
    }

    /**
     * 根据ID查询
     */
    @GetMapping("/selectById/{id}")
    public Result selectById(@PathVariable Integer id) {
        Activity activity = activityService.selectById(id);
        return Result.success(activity);
    }

    /**
     * 查询所有
     */
    @GetMapping("/selectAll")
    public Result selectAll(Activity activity) {
        List<Activity> list = activityService.selectAll(activity);
        return Result.success(list);
    }

    /**
     * 分页查询活动列表
     * 支持按名称和状态筛选
     */
    @GetMapping("/selectPage")
    public Result<PageInfo<Activity>> selectPage(
            @RequestParam(defaultValue = "1") Integer pageNum,
            @RequestParam(defaultValue = "10") Integer pageSize,
            @RequestParam(required = false) String name,
            @RequestParam(required = false) String status) {
        
        Activity activity = new Activity();
        activity.setName(name);
        
        try {
            PageInfo<Activity> pageInfo;
            
            // 根据状态筛选
            if (status != null && !status.equals("all")) {
                pageInfo = activityService.selectByStatus(activity, status, pageNum, pageSize);
            } else {
                pageInfo = activityService.selectPage(activity, pageNum, pageSize);
            }
            
            return Result.success(pageInfo);
        } catch (Exception e) {
            e.printStackTrace();
            return Result.error("500", "获取活动列表失败: " + e.getMessage());
        }
    }

    /**
     * 查询用户报名的活动列表
     */
    @GetMapping("/selectUser")
    public Result selectUser(Activity activity,
                             @RequestParam(defaultValue = "1") Integer pageNum,
                             @RequestParam(defaultValue = "10") Integer pageSize) {
        try {
            System.out.println("===== 活动查询参数 =====");
            System.out.println("接收到的userId: " + activity.getUserId() + ", 类型: " + (activity.getUserId() != null ? activity.getUserId().getClass().getName() : "null"));
            System.out.println("pageNum: " + pageNum);
            System.out.println("pageSize: " + pageSize);
            
            PageInfo<Activity> page = activityService.selectUser(activity, pageNum, pageSize);
            
            System.out.println("查询到的活动数量: " + (page != null ? page.getTotal() : 0));
            if (page != null && page.getList() != null && !page.getList().isEmpty()) {
                System.out.println("第一个活动ID: " + page.getList().get(0).getId() + ", 名称: " + page.getList().get(0).getName());
            }
            
            return Result.success(page);
        } catch (Exception e) {
            logger.error("查询用户报名的活动列表失败", e);
            return Result.error("500", "查询用户报名的活动列表失败: " + e.getMessage());
        }
    }

    /**
     * 查询用户点赞的活动列表
     */
    @GetMapping("/selectLike")
    public Result selectLike(Activity activity,
                             @RequestParam(defaultValue = "1") Integer pageNum,
                             @RequestParam(defaultValue = "10") Integer pageSize) {
        try {
            PageInfo<Activity> page = activityService.selectLike(activity, pageNum, pageSize);
            return Result.success(page);
        } catch (Exception e) {
            logger.error("查询用户点赞的活动列表失败", e);
            return Result.error("500", "查询用户点赞的活动列表失败: " + e.getMessage());
        }
    }

    /**
     * 查询用户收藏的活动列表
     */
    @GetMapping("/selectCollect")
    public Result selectCollect(Activity activity,
                             @RequestParam(defaultValue = "1") Integer pageNum,
                             @RequestParam(defaultValue = "10") Integer pageSize) {
        try {
            PageInfo<Activity> page = activityService.selectCollect(activity, pageNum, pageSize);
            return Result.success(page);
        } catch (Exception e) {
            logger.error("查询用户收藏的活动列表失败", e);
            return Result.error("500", "查询用户收藏的活动列表失败: " + e.getMessage());
        }
    }

    /**
     * 查询用户评论的活动列表
     */
    @GetMapping("/selectComment")
    public Result selectComment(Activity activity,
                             @RequestParam(defaultValue = "1") Integer pageNum,
                             @RequestParam(defaultValue = "10") Integer pageSize) {
        try {
            PageInfo<Activity> page = activityService.selectComment(activity, pageNum, pageSize);
            return Result.success(page);
        } catch (Exception e) {
            logger.error("查询用户评论的活动列表失败", e);
            return Result.error("500", "查询用户评论的活动列表失败: " + e.getMessage());
        }
    }

    /**
     * 热门活动
     */
    @GetMapping("/selectTop")
    public Result selectTop() {
        List<Activity> list = activityService.selectTop();
        return Result.success(list);
    }

    /**
     * 获取即将开始的活动
     */
    @GetMapping("/getUpcoming")
    public Result<List<Activity>> getUpcoming(@RequestParam(defaultValue = "3") Integer limit) {
        try {
            List<Activity> upcomingActivities = activityService.getUpcomingActivities(limit);
            return Result.success(upcomingActivities);
        } catch (Exception e) {
            e.printStackTrace();
            return Result.error("500", "获取即将开始的活动失败: " + e.getMessage());
        }
    }

}