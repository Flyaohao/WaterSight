package com.example.service;

import cn.hutool.core.date.DateUtil;
import cn.hutool.core.util.ObjectUtil;
import cn.hutool.json.JSONArray;
import cn.hutool.json.JSONUtil;
import com.example.common.enums.LikesModuleEnum;
import com.example.common.enums.RoleEnum;
import com.example.entity.*;
import com.example.mapper.BlogMapper;
import com.example.utils.TokenUtils;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import javax.annotation.Resource;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

/**
 * 博客信息业务处理
 **/
@Service
public class BlogService {

    @Resource
    private BlogMapper blogMapper;

    @Resource
    UserService userService;

    @Resource
    LikesService likesService;

    @Resource
    CollectService collectService;

    /**
     * 新增
     */
    public void add(Blog blog) {
        blog.setDate(DateUtil.today());
        Account currentUser = TokenUtils.getCurrentUser();
        if (RoleEnum.USER.name().equals(currentUser.getRole())) {
            blog.setUserId(currentUser.getId());
        }
        blogMapper.insert(blog);
        
        // 增加用户的博客计数
        if (blog.getUserId() != null) {
            userService.increaseBlogCount(blog.getUserId());
        }
    }

    /**
     * 删除
     */
    public void deleteById(Integer id) {
        // 获取博客信息，以获取用户ID
        Blog blog = blogMapper.selectById(id);
        blogMapper.deleteById(id);
        
        // 如果博客存在且有用户ID，减少用户的博客计数
        if (blog != null && blog.getUserId() != null) {
            userService.decreaseBlogCount(blog.getUserId());
        }
    }

    /**
     * 批量删除
     */
    public void deleteBatch(List<Integer> ids) {
        for (Integer id : ids) {
            blogMapper.deleteById(id);
        }
    }

    /**
     * 修改
     */
    public void updateById(Blog blog) {
        blogMapper.updateById(blog);
    }

    /**
     * 根据ID查询
     */
    public Blog selectById(Integer id) {
        Blog blog = blogMapper.selectById(id);
        if (blog != null && blog.getUserId() != null) {
            User user = userService.selectById(blog.getUserId());
            if (user != null) {
                List<Blog> userBlogList = blogMapper.selectUserBlog(user.getId());
                user.setBlogCount(userBlogList.size());
                //  当前用户收到的点赞和收藏的数据
                int userLikesCount = 0;
                int userCollectCount = 0;
                for (Blog b : userBlogList) {
                    Integer fid = b.getId();
                    int likesCount = likesService.selectByFidAndModule(fid, LikesModuleEnum.BLOG.getValue());
                    userLikesCount += likesCount;

                    int collectCount = collectService.selectByFidAndModule(fid, LikesModuleEnum.BLOG.getValue());
                    userCollectCount += collectCount;
                }
                user.setLikesCount(userLikesCount);
                user.setCollectCount(userCollectCount);
                blog.setUser(user);  // 设置作者信息
            }
        }
        
        // 查询当前博客的点赞数据
        int likesCount = likesService.selectByFidAndModule(id, LikesModuleEnum.BLOG.getValue());
        blog.setLikesCount(likesCount);
        Likes userLikes = likesService.selectUserLikes(id, LikesModuleEnum.BLOG.getValue());
        blog.setUserLike(userLikes != null);

        // 查询当前博客的收藏数据
        int collectCount = collectService.selectByFidAndModule(id, LikesModuleEnum.BLOG.getValue());
        blog.setCollectCount(collectCount);
        Collect userCollect = collectService.selectUserCollect(id, LikesModuleEnum.BLOG.getValue());
        blog.setUserCollect(userCollect != null);

        return blog;
    }

    /**
     * 查询所有
     */
    public List<Blog> selectAll() {
        return blogMapper.selectAll();
    }

    /**
     * 分页查询
     */
    public PageInfo<Blog> selectPage(Blog blog, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum, pageSize);
        List<Blog> list = blogMapper.selectAllWithParams(blog);
        for (Blog b : list) {
            int likesCount = likesService.selectByFidAndModule(b.getId(), LikesModuleEnum.BLOG.getValue());
            b.setLikesCount(likesCount);
        }
        return PageInfo.of(list);
    }

    public List<Blog> selectTop() {
        List<Blog> blogList = this.selectAll();
        blogList = blogList.stream().sorted((b1, b2) -> b2.getReadCount().compareTo(b1.getReadCount()))
                .limit(20)
                .collect(Collectors.toList());
        return blogList;
    }


    public Set<Blog> selectRecommend(Integer blogId) {
        Blog blog = this.selectById(blogId);
        Set<Blog> blogSet = new HashSet<>();
        if (blog != null && ObjectUtil.isNotEmpty(blog.getTags())) {
            List<Blog> blogList = this.selectAll();
            JSONArray tagsArr = JSONUtil.parseArray(blog.getTags());
            for (Object tag : tagsArr) {
                // 筛选出包含当前博客标签的其他的博客列表
                Set<Blog> collect = blogList.stream().filter(b -> b.getTags() != null && b.getTags().contains(tag.toString()) && !blogId.equals(b.getId()))
                        .collect(Collectors.toSet());
                blogSet.addAll(collect);
            }
        }
        blogSet = blogSet.stream().limit(5).collect(Collectors.toSet());
        blogSet.forEach(b -> {
            int likesCount = likesService.selectByFidAndModule(b.getId(), LikesModuleEnum.BLOG.getValue());
            b.setLikesCount(likesCount);
        });
        return blogSet;
    }

    public void updateReadCount(Integer blogId) {
        blogMapper.updateReadCount(blogId);
    }

    public PageInfo<Blog> selectUser(Blog blog, Integer pageNum, Integer pageSize) {
        System.out.println("BlogService.selectUser - 传入参数:");
        System.out.println("  - 博客对象: " + blog);
        System.out.println("  - 用户ID: " + (blog != null ? blog.getUserId() : "null"));
        System.out.println("  - 页码: " + pageNum);
        System.out.println("  - 每页大小: " + pageSize);
        
        // 获取当前登录用户
        Account currentUser = TokenUtils.getCurrentUser();
        System.out.println("  - 当前登录用户: " + (currentUser != null ? currentUser.getId() : "null"));
        
        // URL传入的userId优先，只有在没有传递userId的情况下，才使用当前登录用户的ID
        if (blog.getUserId() == null && RoleEnum.USER.name().equals(currentUser.getRole())) {
            blog.setUserId(currentUser.getId());
            System.out.println("  - 使用当前登录用户ID: " + currentUser.getId());
        } else {
            System.out.println("  - 使用URL传入的用户ID: " + blog.getUserId());
        }
        
        PageInfo<Blog> result = this.selectPage(blog, pageNum, pageSize);
        System.out.println("  - 查询结果: " + (result != null ? result.getTotal() : 0) + " 条记录");
        return result;
    }

    // 查询用户点赞的数据
    public PageInfo<Blog> selectLike(Blog blog, Integer pageNum, Integer pageSize) {
        Account currentUser = TokenUtils.getCurrentUser();
        if (RoleEnum.USER.name().equals(currentUser.getRole())) {
            blog.setUserId(currentUser.getId());
        }
        PageHelper.startPage(pageNum, pageSize);
        List<Blog> list = blogMapper.selectLike(blog);
        PageInfo<Blog> pageInfo = PageInfo.of(list);
        List<Blog> blogList = pageInfo.getList();
        for (Blog b : blogList) {
            int likesCount = likesService.selectByFidAndModule(b.getId(), LikesModuleEnum.BLOG.getValue());
            b.setLikesCount(likesCount);
        }
        return pageInfo;
    }

    public PageInfo<Blog> selectCollect(Blog blog, Integer pageNum, Integer pageSize) {
        Account currentUser = TokenUtils.getCurrentUser();
        if (RoleEnum.USER.name().equals(currentUser.getRole())) {
            blog.setUserId(currentUser.getId());
        }
        PageHelper.startPage(pageNum, pageSize);
        List<Blog> list = blogMapper.selectCollect(blog);
        PageInfo<Blog> pageInfo = PageInfo.of(list);
        List<Blog> blogList = pageInfo.getList();
        for (Blog b : blogList) {
            int likesCount = likesService.selectByFidAndModule(b.getId(), LikesModuleEnum.BLOG.getValue());
            b.setLikesCount(likesCount);
        }
        return pageInfo;
    }

    public PageInfo<Blog> selectComment(Blog blog, Integer pageNum, Integer pageSize) {
        Account currentUser = TokenUtils.getCurrentUser();
        if (RoleEnum.USER.name().equals(currentUser.getRole())) {
            blog.setUserId(currentUser.getId());
        }
        PageHelper.startPage(pageNum, pageSize);
        List<Blog> list = blogMapper.selectComment(blog);
        PageInfo<Blog> pageInfo = PageInfo.of(list);
        List<Blog> blogList = pageInfo.getList();
        for (Blog b : blogList) {
            int likesCount = likesService.selectByFidAndModule(b.getId(), LikesModuleEnum.BLOG.getValue());
            b.setLikesCount(likesCount);
        }
        return pageInfo;
    }

    /**
     * 分页查询用户的博客
     */
    public PageInfo<Blog> selectUserBlogsByUsername(String username, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum, pageSize);
        List<Blog> list = blogMapper.selectByUsername(username);
        for (Blog b : list) {
            int likesCount = likesService.selectByFidAndModule(b.getId(), LikesModuleEnum.BLOG.getValue());
            b.setLikesCount(likesCount);
        }
        return PageInfo.of(list);
    }
}