package com.example.service;

import cn.hutool.core.util.ObjectUtil;
import com.example.common.Constants;
import com.example.common.enums.LikesModuleEnum;
import com.example.common.enums.ResultCodeEnum;
import com.example.common.enums.RoleEnum;
import com.example.entity.Account;
import com.example.entity.Admin;
import com.example.entity.Blog;
import com.example.entity.User;
import com.example.exception.CustomException;
import com.example.mapper.BlogMapper;
import com.example.mapper.UserMapper;
import com.example.utils.TokenUtils;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service
public class UserService {

    @Resource
    private UserMapper userMapper;
    
    @Resource
    private BlogMapper blogMapper;
    
    @Resource
    private LikesService likesService;
    
    @Resource
    private CollectService collectService;

    public void add(User user) {
        // 业务方法
        // 1. 判断用户账号是否重复
        User dbUser = userMapper.selectByUsername(user.getUsername());
        if (dbUser != null) {
            throw new CustomException(ResultCodeEnum.USER_EXIST_ERROR);
        }
        // 2. 判断用户密码是不是空
        if (ObjectUtil.isEmpty(user.getPassword())) {
            user.setPassword(Constants.USER_DEFAULT_PASSWORD); // 默认密码 123
        }
        // 3. 判断用户名称是不是空
        if (ObjectUtil.isEmpty(user.getName())) {
            user.setName(user.getUsername());
        }
        // 4. 默认用户角色
        user.setRole(RoleEnum.USER.name());
        userMapper.insert(user);
    }

    /**
     * 根据用户ID删除用户
     *
     * @param id 用户ID
     */
    public void deleteById(Integer id) {
        // 调用userMapper的deleteById方法，根据用户ID删除用户
        userMapper.deleteById(id);
    }


    /**
     * 批量删除用户
     *
     * @param ids 用户ID列表
     */
    public void deleteBatch(List<Integer> ids) {
        // 遍历用户ID列表
        for (Integer id : ids) {
            // 调用deleteById方法，根据用户ID删除单个用户
            this.deleteById(id);
        }
    }


    /**
     * 根据用户ID更新用户信息
     *
     * @param user 用户信息
     */
    public void updateById(User user) {
        System.out.println("UserService.updateById - 开始更新用户信息：" + user.getId());
        System.out.println("UserService.updateById - 用户信息：" + user);
        System.out.println("UserService.updateById - 浏览角色：" + user.getBrowseRole());
        try {
            userMapper.updateById(user);
            System.out.println("UserService.updateById - 用户信息更新成功");
        } catch (Exception e) {
            System.err.println("UserService.updateById - 更新用户信息时发生异常：");
            e.printStackTrace();
            throw e;
        }
    }


    /**
     * 根据用户ID查询用户信息
     *
     * @param id 用户ID
     * @return 用户信息
     */
    public User selectById(Integer id) {
        System.out.println("UserService.selectById - 开始查询用户信息：" + id);
        User user = userMapper.selectById(id);
        System.out.println("UserService.selectById - 查询结果：" + (user != null ? "找到用户，ID=" + user.getId() + ", 用户名=" + user.getUsername() : "未找到用户"));
        if (user != null) {
            System.out.println("UserService.selectById - 用户浏览角色：" + user.getBrowseRole());
        }
        return user;
    }

    /**
     * 查询所有用户信息
     *
     * @param user 用户信息
     * @return 用户信息列表
     */
    public List<User> selectAll(User user) {
        // 调用userMapper的selectAll方法，查询所有用户信息
        return userMapper.selectAll(user);
    }


    /**
     * 分页查询用户信息
     *
     * @param user 用户信息
     * @param pageNum 页码
     * @param pageSize 每页条数
     * @return 分页信息
     */
    public PageInfo<User> selectPage(User user, Integer pageNum, Integer pageSize) {
        // 设置分页参数
        PageHelper.startPage(pageNum, pageSize);
        // 查询所有用户信息
        List<User> list = userMapper.selectAll(user);
        // 封装分页信息
        return PageInfo.of(list);
    }


    /**
     * 用户登录
     *
     * @param account 用户账号信息
     * @return 登录成功的用户账号信息
     */
    public Account login(Account account) {
        // 根据用户名查询用户信息
        Account dbUser = userMapper.selectByUsername(account.getUsername());
        // 如果用户不存在，抛出用户不存在异常
        if (ObjectUtil.isNull(dbUser)) {
            throw new CustomException(ResultCodeEnum.USER_NOT_EXIST_ERROR);
        }
        // 如果用户密码不正确，抛出用户账号错误异常
        if (!account.getPassword().equals(dbUser.getPassword())) {
            throw new CustomException(ResultCodeEnum.USER_ACCOUNT_ERROR);
        }
        // 生成token
        String tokenData = dbUser.getId() + "-" + RoleEnum.USER.name();
        String token = TokenUtils.createToken(tokenData, dbUser.getPassword());
        // 将token设置到用户信息中
        dbUser.setToken(token);
        // 返回登录成功的用户账号信息
        return dbUser;
    }


    /**
     * 注册
     *
     * @param account 用户账号信息
     */
    public void register(Account account) {
        // 创建一个新的User对象
        User user = new User();
        // 将account对象的属性复制到user对象中
        BeanUtils.copyProperties(account, user);
        // 调用add方法，将新用户信息添加到数据库中
        this.add(user);
    }


    /**
     * 更新用户密码
     *
     * @param account 用户账号信息
     */
    public void updatePassword(Account account) {
        // 根据用户名查询用户信息
        User dbUser = userMapper.selectByUsername(account.getUsername());
        // 如果用户不存在，抛出用户不存在异常
        if (ObjectUtil.isNull(dbUser)) {
            throw new CustomException(ResultCodeEnum.USER_NOT_EXIST_ERROR);
        }
        // 如果用户输入的原密码不正确，抛出密码错误异常
        if (!account.getPassword().equals(dbUser.getPassword())) {
            throw new CustomException(ResultCodeEnum.PARAM_PASSWORD_ERROR);
        }
        // 更新用户密码为新密码
        dbUser.setPassword(account.getNewPassword());
        // 调用更新用户信息的方法
        this.updateById(dbUser);
    }

    /**
     * 增加用户博客数量
     * @param userId 用户ID
     */
    public void increaseBlogCount(Integer userId) {
        if (userId != null) {
            userMapper.increaseBlogCount(userId);
        }
    }

    /**
     * 减少用户博客数量
     * @param userId 用户ID
     */
    public void decreaseBlogCount(Integer userId) {
        if (userId != null) {
            userMapper.decreaseBlogCount(userId);
        }
    }

    /**
     * 增加用户获赞数量
     * @param userId 用户ID
     */
    public void increaseLikesCount(Integer userId) {
        if (userId != null) {
            userMapper.increaseLikesCount(userId);
        }
    }

    /**
     * 减少用户获赞数量
     * @param userId 用户ID
     */
    public void decreaseLikesCount(Integer userId) {
        if (userId != null) {
            userMapper.decreaseLikesCount(userId);
        }
    }

    /**
     * 增加用户被收藏数量
     * @param userId 用户ID
     */
    public void increaseCollectCount(Integer userId) {
        if (userId != null) {
            userMapper.increaseCollectCount(userId);
        }
    }

    /**
     * 减少用户被收藏数量
     * @param userId 用户ID
     */
    public void decreaseCollectCount(Integer userId) {
        if (userId != null) {
            userMapper.decreaseCollectCount(userId);
        }
    }

    /**
     * 刷新用户统计数据
     * @param userId 用户ID
     */
    public void refreshUserStats(Integer userId) {
        if (userId == null) {
            throw new CustomException(ResultCodeEnum.PARAM_ERROR);
        }
        
        User user = userMapper.selectById(userId);
        if (user == null) {
            throw new CustomException(ResultCodeEnum.USER_NOT_EXIST_ERROR);
        }
        
        // 计算用户的博客数量
        List<Blog> userBlogs = blogMapper.selectUserBlog(userId);
        user.setBlogCount(userBlogs.size());
        
        // 计算用户获得的点赞总数
        int totalLikes = 0;
        for (Blog blog : userBlogs) {
            int likesCount = likesService.selectByFidAndModule(blog.getId(), LikesModuleEnum.BLOG.getValue());
            totalLikes += likesCount;
        }
        user.setLikesCount(totalLikes);
        
        // 计算用户获得的收藏总数
        int totalCollects = 0;
        for (Blog blog : userBlogs) {
            int collectCount = collectService.selectByFidAndModule(blog.getId(), LikesModuleEnum.BLOG.getValue());
            totalCollects += collectCount;
        }
        user.setCollectCount(totalCollects);
        
        // 更新用户信息
        updateById(user);
    }

    /**
     * 根据用户真实姓名搜索
     * @param keyword 搜索关键词
     * @return 用户列表
     */
    public List<User> searchByName(String keyword) {
        return userMapper.searchByName(keyword);
    }

}
