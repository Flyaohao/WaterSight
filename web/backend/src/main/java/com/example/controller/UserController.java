package com.example.controller;

import com.example.common.Result;
import com.example.common.enums.ResultCodeEnum;
import com.example.entity.Admin;
import com.example.entity.User;
import com.example.service.UserService;
import com.github.pagehelper.PageInfo;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/user")
public class UserController {

    @Resource
    private UserService userService;

    @PostMapping("/add")
    public Result add(@RequestBody User user) {
        userService.add(user);
        return Result.success();
    }

    /**
     * 删除
     */
    @DeleteMapping("/delete/{id}")
    public Result deleteById(@PathVariable Integer id) {
        userService.deleteById(id);
        return Result.success();
    }

    /**
     * 批量删除
     */
    @DeleteMapping("/delete/batch")
    public Result deleteBatch(@RequestBody List<Integer> ids) {  //  [1,2,3]
        userService.deleteBatch(ids);
        return Result.success();
    }

    /**
     * 修改
     */
    @PutMapping("/update")
    public Result updateById(@RequestBody User user) {
        userService.updateById(user);
        return Result.success();
    }

    /**
     * 根据ID查询
     */
    @GetMapping("/selectById/{id}")
    public Result selectById(@PathVariable Integer id) {
        User user = userService.selectById(id);
        return Result.success(user);
    }

    /**
     * 查询所有
     */
    @GetMapping("/selectAll")
    public Result selectAll(User user) {
        List<User> list = userService.selectAll(user);
        return Result.success(list);
    }

    /**
     * 分页查询
     */
    @GetMapping("/selectPage")
    public Result selectPage(User user,
                             @RequestParam(defaultValue = "1") Integer pageNum,
                             @RequestParam(defaultValue = "10") Integer pageSize) {
        PageInfo<User> page = userService.selectPage(user, pageNum, pageSize);
        return Result.success(page);
    }

    /**
     * 刷新所有用户的统计数据
     */
    @GetMapping("/refreshStats")
    public Result refreshAllUserStats() {
        // 通过SQL脚本执行统计数据刷新
        try {
            // 查询所有用户
            List<User> users = userService.selectAll(new User());
            for (User user : users) {
                // 计算并更新每个用户的统计数据
                userService.refreshUserStats(user.getId());
            }
            return Result.success("所有用户统计数据刷新成功");
        } catch (Exception e) {
            return Result.error("500", "统计数据刷新失败: " + e.getMessage());
        }
    }

    /**
     * 刷新指定用户的统计数据
     */
    @GetMapping("/refreshStats/{userId}")
    public Result refreshUserStats(@PathVariable Integer userId) {
        try {
            userService.refreshUserStats(userId);
            return Result.success("用户统计数据刷新成功");
        } catch (Exception e) {
            return Result.error("500", "统计数据刷新失败: " + e.getMessage());
        }
    }

    /**
     * 更新用户浏览角色
     */
    @PutMapping("/updateBrowseRole")
    public Result updateBrowseRole(@RequestBody Map<String, Object> params) {
        try {
            // 获取参数
            Integer userId = (Integer) params.get("userId");
            String browseRole = (String) params.get("browseRole");

            // 验证参数
            if (userId == null || browseRole == null) {
                return Result.error("400", "参数错误");
            }

            // 验证角色值
            if (!Arrays.asList("RESEARCHER", "HOBBYIST", "ALL").contains(browseRole)) {
                return Result.error("400", "无效的角色值");
            }

            // 更新用户角色
            User user = userService.selectById(userId);
            if (user == null) {
                return Result.error("404", "用户不存在");
            }

            user.setBrowseRole(browseRole);
            userService.updateById(user);
            
            return Result.success("更新成功");
        } catch (Exception e) {
            System.err.println("更新浏览角色时发生异常：");
            e.printStackTrace();
            return Result.error("500", "更新浏览角色失败: " + e.getMessage());
        }
    }

    /**
     * 根据用户真实姓名搜索
     */
    @GetMapping("/search")
    public Result searchByName(@RequestParam String keyword) {
        List<User> users = userService.searchByName(keyword);
        return Result.success(users);
    }

}
