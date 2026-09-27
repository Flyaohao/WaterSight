package com.example.service;

import com.example.entity.Account;
import com.example.entity.Blog;
import com.example.entity.Likes;
import com.example.mapper.BlogMapper;
import com.example.mapper.LikesMapper;
import com.example.common.enums.LikesModuleEnum;
import com.example.utils.TokenUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;

@Service
public class LikesService {

    private static final Logger logger = LoggerFactory.getLogger(LikesService.class);

    @Resource
    private LikesMapper likesMapper;
    
    @Resource
    private BlogMapper blogMapper;
    
    @Resource
    private UserService userService;
    
    @Resource
    private MessageService messageService;

    public boolean set(Likes likes) {
        logger.info("开始处理点赞操作: fid={}, module={}", likes.getFid(), likes.getModule());
        Account currentUser = TokenUtils.getCurrentUser();
        likes.setUserId(currentUser.getId());
        
        // 获取作者ID
        Integer authorId = null;
        Blog blog = null;
        if ("博客".equals(likes.getModule())) {
            blog = blogMapper.selectById(likes.getFid());
            if (blog != null) {
                authorId = blog.getUserId();
            }
        }
        
        Likes dblLikes = likesMapper.selectUserLikes(likes);
        logger.info("查询现有点赞记录: {}", dblLikes);
        
        if (dblLikes == null) {
            logger.info("创建新点赞记录");
            likesMapper.insert(likes);
            
            // 如果是博客模块且作者ID不为空，增加作者的获赞数并发送消息通知
            if (authorId != null && !authorId.equals(currentUser.getId())) {
                userService.increaseLikesCount(authorId);
                // 发送点赞消息通知
                logger.info("准备发送点赞通知");
                messageService.createLikeMessage(currentUser.getId(), currentUser.getName(), blog);
            }
            
            return true;
        } else {
            logger.info("删除现有点赞记录");
            likesMapper.deleteById(dblLikes.getId());
            
            // 如果是博客模块且作者ID不为空，减少作者的获赞数
            if (authorId != null) {
                userService.decreaseLikesCount(authorId);
            }
            
            return false;
        }
    }

    /**
     * 查询当前用户是否点过赞
     */
    public Likes selectUserLikes(Integer fid, String module) {
        Account currentUser = TokenUtils.getCurrentUser();
        Likes likes = new Likes();
        likes.setUserId(currentUser.getId());
        likes.setFid(fid);
        likes.setModule(module);
        return likesMapper.selectUserLikes(likes);
    }

    public int selectByFidAndModule(Integer fid, String module) {
        return likesMapper.selectByFidAndModule(fid, module);
    }
}
