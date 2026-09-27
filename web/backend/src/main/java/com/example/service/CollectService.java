package com.example.service;

import com.example.entity.Account;
import com.example.entity.Blog;
import com.example.entity.Collect;
import com.example.mapper.BlogMapper;
import com.example.mapper.CollectMapper;
import com.example.common.enums.LikesModuleEnum;
import com.example.utils.TokenUtils;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;

@Service
public class CollectService {

    @Resource
    CollectMapper collectMapper;
    
    @Resource
    BlogMapper blogMapper;
    
    @Resource
    UserService userService;
    
    @Resource
    MessageService messageService;

    public boolean set(Collect collect) {
        Account currentUser = TokenUtils.getCurrentUser();
        collect.setUserId(currentUser.getId());
        
        // 获取作者ID
        Integer authorId = null;
        Blog blog = null;
        if ("博客".equals(collect.getModule())) {
            blog = blogMapper.selectById(collect.getFid());
            if (blog != null) {
                authorId = blog.getUserId();
            }
        }
        
        Collect dblCollect = collectMapper.selectUserCollect(collect);
        
        if (dblCollect == null) {
            collectMapper.insert(collect);
            
            // 如果是博客模块且作者ID不为空，增加作者的被收藏数并发送消息通知
            if (authorId != null && !authorId.equals(currentUser.getId())) {
                userService.increaseCollectCount(authorId);
                // 发送收藏消息通知
                messageService.createCollectMessage(currentUser.getId(), currentUser.getName(), blog);
            }
            
            return true;
        } else {
            collectMapper.deleteById(dblCollect.getId());
            
            // 如果是博客模块且作者ID不为空，减少作者的被收藏数
            if (authorId != null) {
                userService.decreaseCollectCount(authorId);
            }
            
            return false;
        }
    }

    /**
     * 查询当前用户是否收藏过
     */
    public Collect selectUserCollect(Integer fid, String module) {
        Account currentUser = TokenUtils.getCurrentUser();
        Collect collect = new Collect();
        collect.setUserId(currentUser.getId());
        collect.setFid(fid);
        collect.setModule(module);
        return collectMapper.selectUserCollect(collect);
    }

    public int selectByFidAndModule(Integer fid, String module) {
        return collectMapper.selectByFidAndModule(fid, module);
    }
}
