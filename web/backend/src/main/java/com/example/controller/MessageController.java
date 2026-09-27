package com.example.controller;

import com.example.common.Result;
import com.example.entity.Account;
import com.example.entity.Message;
import com.example.service.MessageService;
import com.example.utils.TokenUtils;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/message")
public class MessageController {

    @Resource
    private MessageService messageService;

    /**
     * 获取未读消息数量
     */
    @GetMapping("/unread/count")
    public Result getUnreadCount() {
        System.out.println("收到获取未读消息数量请求");
        Account currentUser = TokenUtils.getCurrentUser();
        if (currentUser == null) {
            System.out.println("用户未登录");
            return Result.error("401", "未登录");
        }
        int count = messageService.getUnreadCount(currentUser.getId());
        System.out.println("返回未读消息数量: " + count);
        return Result.success(count);
    }

    /**
     * 获取消息列表
     */
    @GetMapping("/list")
    public Result getMessageList(@RequestParam(defaultValue = "1") Integer pageNum,
                               @RequestParam(defaultValue = "20") Integer pageSize) {
        System.out.println("收到获取消息列表请求");
        Account currentUser = TokenUtils.getCurrentUser();
        System.out.println("当前用户信息: " + currentUser);
        
        if (currentUser == null || currentUser.getId() == null) {
            System.out.println("用户未登录");
            return Result.error("401", "未登录");
        }
        
        try {
            PageHelper.startPage(pageNum, pageSize);
            List<Message> messages = messageService.selectByUserId(currentUser.getId());
            PageInfo<Message> pageInfo = new PageInfo<>(messages);
            System.out.println("查询到消息数量: " + pageInfo.getTotal());
            System.out.println("消息列表: " + messages);
            return Result.success(pageInfo);
        } catch (Exception e) {
            System.err.println("查询消息列表出错: " + e.getMessage());
            e.printStackTrace();
            return Result.error("500", "查询消息失败");
        }
    }

    /**
     * 标记消息为已读
     */
    @PutMapping("/read/{id}")
    public Result markAsRead(@PathVariable Integer id) {
        try {
            messageService.markAsRead(id);
            return Result.success();
        } catch (Exception e) {
            e.printStackTrace();
            return Result.error("500", "标记已读失败");
        }
    }

    /**
     * 标记所有消息为已读
     */
    @PostMapping("/read/all")
    public Result markAllAsRead() {
        Account currentUser = TokenUtils.getCurrentUser();
        messageService.markAllAsRead(currentUser.getId());
        return Result.success();
    }

    /**
     * 删除消息
     */
    @DeleteMapping("/delete/{id}")
    public Result deleteById(@PathVariable Integer id) {
        messageService.deleteById(id);
        return Result.success();
    }

    /**
     * 批量删除消息
     */
    @DeleteMapping("/delete")
    public Result batchDelete(@RequestBody Map<String, List<Integer>> params) {
        List<Integer> ids = params.get("ids");
        if (ids == null || ids.isEmpty()) {
            return Result.error("400", "参数错误");
        }
        try {
            for (Integer id : ids) {
                messageService.deleteById(id);
            }
            return Result.success();
        } catch (Exception e) {
            e.printStackTrace();
            return Result.error("500", "批量删除失败");
        }
    }

    /**
     * 批量标记消息为已读
     */
    @PostMapping("/batchRead")
    public Result batchRead(@RequestBody Map<String, List<Integer>> params) {
        List<Integer> ids = params.get("ids");
        if (ids == null || ids.isEmpty()) {
            return Result.error("400", "参数错误");
        }
        try {
            for (Integer id : ids) {
                messageService.markAsRead(id);
            }
            return Result.success();
        } catch (Exception e) {
            e.printStackTrace();
            return Result.error("500", "批量标记已读失败");
        }
    }
} 