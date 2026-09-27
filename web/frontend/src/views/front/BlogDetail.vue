<template>
  <div class="blog-detail-container" :class="themeClass">
    <!-- 返回按钮 -->
    <div class="back-button" @click="goBack">
      <i class="el-icon-arrow-left"></i>
      返回
    </div>

    <div class="blog-detail-wrapper">
      <!-- 主内容区 -->
      <div class="main-content-area">
        <!-- 博客标题和信息 -->
        <div class="blog-header">
          <h1 class="blog-title">{{ blog.title }}</h1>
          <div class="blog-meta">
            <div class="meta-item">
              <i class="el-icon-user"></i>
              <span class="author-link" @click="goToAuthorHome(blog.userId)">{{
                blog.userName
              }}</span>
            </div>
            <div class="meta-item">
              <i class="el-icon-date"></i>
              <span>{{ blog.date }}</span>
            </div>
            <div class="meta-item">
              <i class="el-icon-view"></i>
              <span>{{ blog.readCount }} 阅读</span>
            </div>
            <div class="meta-tags">
              <el-tag
                v-for="item in tagsArr"
                :key="item"
                type="primary"
                size="small"
                effect="plain"
              >
                {{ item }}
              </el-tag>
            </div>
          </div>
        </div>

        <!-- 博客内容 -->
        <div class="blog-content">
          <div
            class="content-wrapper w-e-text"
            v-html="formatContent(blog.content)"
          ></div>
        </div>

        <!-- 点赞和收藏 -->
        <div class="blog-actions">
          <div
            class="action-button"
            :class="{ active: blog.userLike }"
            @click="setLikes"
          >
            <i class="el-icon-thumb"></i>
            <span>{{ blog.likesCount }}</span>
            <div class="action-label">点赞</div>
          </div>
          <div
            class="action-button"
            :class="{ active: blog.userCollect }"
            @click="setCollect"
          >
            <i class="el-icon-star-on"></i>
            <span>{{ blog.collectCount }}</span>
            <div class="action-label">收藏</div>
          </div>
          <div class="action-button" @click="shareBlog">
            <i class="el-icon-share"></i>
            <div class="action-label">分享</div>
          </div>
        </div>

        <!-- 评论区 -->
        <div class="blog-comments">
          <h2 class="section-title">评论区</h2>
          <Comment :fid="blogId" module="博客" />
        </div>
      </div>

      <!-- 侧边栏 -->
      <div class="sidebar-area sidebar-fixed">
        <!-- 作者信息 -->
        <div class="sidebar-card author-card">
          <div class="author-header">
            <img
              :src="blog.user?.avatar || require('@/assets/imgs/bgc2.jpg')"
              @error="handleAvatarError($event)"
              alt="作者头像"
              class="author-avatar"
              @click="goToAuthorHome(blog.userId)"
            />
            <div class="author-info">
              <div class="author-name" @click="goToAuthorHome(blog.userId)">
                {{ blog.user?.name }}
              </div>
              <div class="author-bio">
                {{ blog.user?.info || "这个人很懒，什么都没留下" }}
              </div>
            </div>
          </div>

          <!-- 关注按钮 -->
          <div
            class="author-follow"
            v-if="blog.userId !== user.id && user.token"
          >
            <el-button
              type="primary"
              size="small"
              :loading="followLoading"
              :disabled="followLoading"
              @click="toggleFollow"
              :class="{ 'is-following': isFollowing }"
            >
              {{ isFollowing ? "已关注" : "关注作者" }}
            </el-button>
          </div>

          <div class="author-stats">
            <div class="stat-item" @click="goToAuthorHome(blog.userId)">
              <div class="stat-value">{{ blog.user?.blogCount || 0 }}</div>
              <div class="stat-label">文章</div>
            </div>
            <div class="stat-item" @click="goToAuthorHome(blog.userId)">
              <div class="stat-value">{{ blog.user?.likesCount || 0 }}</div>
              <div class="stat-label">获赞</div>
            </div>
            <div class="stat-item" @click="goToAuthorHome(blog.userId)">
              <div class="stat-value">{{ blog.user?.collectCount || 0 }}</div>
              <div class="stat-label">被收藏</div>
            </div>
          </div>
        </div>

        <!-- 目录卡片 -->
        <div class="sidebar-card toc-card" v-if="tocItems.length > 0">
          <h3 class="toc-title"><i class="el-icon-menu"></i> 文章目录</h3>
          <div class="toc-list">
            <div v-if="tocItems.length === 0" class="toc-empty">
              此文章没有目录
            </div>
            <div
              v-for="(item, index) in tocItems"
              :key="index"
              class="toc-item"
              :class="[
                `toc-level-${item.level}`,
                { active: index === activeIndex }
              ]"
              @click="scrollToHeading(item.id)"
            >
              <span class="toc-text">{{ item.text }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 鱼群动画 -->
  </div>
</template>

<script>
import Comment from "@/components/Comment";

export default {
  name: "BlogDetail",
  components: {
    Comment,
  },
  data() {
    return {
      blogId: this.$route.query.blogId,
      blog: {},
      tagsArr: [],
      recommendList: [],
      user: JSON.parse(localStorage.getItem("xm-user") || "{}"),
      loading: true,
      tocItems: [], // 存储目录项
      activeIndex: 0, // 当前激活的目录项索引
      observer: null, // 用于监听标题元素可见性的观察器
      isFollowing: false, // 是否已关注该作者
      followLoading: false, // 关注按钮加载状态
    };
  },
  created() {
    this.checkLogin();
    if (this.user.token) {
      this.fetchBlogDetail(this.blogId);
    } else {
      this.$router.push("/front/home");
    }
  },
  methods: {
    checkLogin() {
      if (!this.user.token) {
        this.$confirm("请先登录后再查看详情", "提示", {
          confirmButtonText: "去登录",
          cancelButtonText: "返回首页",
          type: "warning",
          closeOnClickModal: false,
          closeOnPressEscape: false,
          showClose: false,
        })
          .then(() => {
            this.$router.push("/login");
          })
          .catch(() => {
            this.$router.push("/front/home");
          });
      }
    },
    setLikes() {
      if (!this.user.token) {
        this.$message.warning("请先登录");
        return;
      }
      this.$request
        .post("/likes/set", { fid: this.blogId, module: "博客" })
        .then((res) => {
          const message1 = this.blog.userLike ? "取消点赞成功" : "点赞成功";
          if (res.code === "200") {
            this.$message.success(message1);
            this.fetchBlogDetail(this.blogId);
          }
        });
    },
    setCollect() {
      if (!this.user.token) {
        this.$message.warning("请先登录");
        return;
      }
      this.$request
        .post("/collect/set", { fid: this.blogId, module: "博客" })
        .then((res) => {
          const message2 = this.blog.userCollect ? "取消收藏成功" : "收藏成功";
          if (res.code === "200") {
            this.$message.success(message2);
            this.fetchBlogDetail(this.blogId);
          }
        });
    },
    fetchBlogDetail(blogId) {
      this.loading = true;
      this.$request
        .get(`/blog/selectById/${blogId}`)
        .then((res) => {
          if (res.code === "200") {
            this.blog = res.data || {};
            
            // 安全地解析博客标签
            try {
              // 尝试解析标签JSON
              if (typeof this.blog.tags === 'string') {
                // 标签可能是格式不正确的字符串，先尝试直接解析
                if (this.blog.tags.startsWith('[') && this.blog.tags.endsWith(']')) {
                  this.tagsArr = JSON.parse(this.blog.tags);
                } else {
                  // 如果标签是逗号分隔的字符串，将其转换为数组
                  this.tagsArr = this.blog.tags.split(',').map(tag => tag.trim()).filter(tag => tag);
                }
              } else if (Array.isArray(this.blog.tags)) {
                // 如果标签已经是数组，直接使用
                this.tagsArr = this.blog.tags;
              } else {
                // 其他情况使用空数组
                this.tagsArr = [];
              }
            } catch (e) {
              console.error('解析博客标签失败:', e);
              // 解析失败时，尝试作为逗号分隔的字符串处理
              if (typeof this.blog.tags === 'string') {
                this.tagsArr = this.blog.tags.split(',').map(tag => tag.trim()).filter(tag => tag);
              } else {
                this.tagsArr = [];
              }
            }
            
            // 设置浏览器标签页标题为博客标题
            document.title = `${this.blog.title || "博客详情"} - WaterSight`;

            // 如果博客有作者信息且当前用户已登录，检查当前用户是否关注了该作者
            if (
              this.blog.userId &&
              this.user.token &&
              this.blog.userId !== this.user.id
            ) {
              this.checkFollowStatus();
            }

            // 获取博客详情后，生成目录
            this.$nextTick(() => {
              this.generateToc();
            });
          } else {
            this.$message.error(res.msg || "获取博客详情失败");
            this.$router.push("/front/home");
          }
        })
        .catch((err) => {
          console.error("获取博客详情失败", err);
          this.$message.error("获取博客详情失败，请稍后重试");
          this.$router.push("/front/home");
        })
        .finally(() => {
          this.loading = false;
        });
    },
    handleAvatarError(e) {
      e.target.src = require("@/assets/imgs/bgc2.jpg");
    },
    formatContent(content) {
      if (!content) return "";
      // 处理图片加载失败的情况
      return content.replace(
        /<img/g,
        "<img onerror=\"this.src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg=='\""
      );
    },
    goBack() {
      if (window.history.length <= 1) {
        this.$message.info("没有上一页了哦");
        return;
      }
      this.$router.go(-1);
    },
    goToAuthorHome(userId) {
      if (userId) {
        this.$router.push({
          path: "/front/authorHome",
          query: { authorId: userId },
        });
      }
    },
    goBlogDetail(id) {
      this.$router.push(`/front/blogDetail?blogId=${id}`);
    },
    generateToc() {
      this.$nextTick(() => {
        // 获取文章内容区域
        const contentEl = document.querySelector(".content-wrapper");
        if (!contentEl) {
          console.log("找不到内容区域元素");
          return;
        }

        // 查找所有标题元素
        const headings = contentEl.querySelectorAll("h1, h2, h3, h4, h5, h6");
        if (headings.length === 0) {
          console.log("文章中没有找到标题元素");
          return;
        }

        // 清空现有目录
        this.tocItems = [];

        // 为每个标题添加ID并收集目录项
        headings.forEach((heading, index) => {
          // 获取标题级别
          const level = parseInt(heading.tagName.substring(1));

          // 生成唯一ID
          const id = `heading-${index}`;
          heading.id = id;
          
          // 不再添加点击事件和复制链接的功能
          // 仅收集目录项
          this.tocItems.push({
            id,
            text: heading.textContent.trim() || `[无标题 ${level}]`,
            level,
          });
        });

        // 设置目录项监听
        this.setupIntersectionObserver(headings);
      });
    },
    
    // 设置标题元素交叉观察器
    setupIntersectionObserver(headings) {
      // 如果已有观察器，先断开连接
      if (this.observer) {
        this.observer.disconnect();
      }
      
      // 配置观察器选项
      const options = {
        root: null, // 相对于视口
        rootMargin: '-100px 0px -70% 0px', // 上方偏移100px，下方偏移70%
        threshold: 0 // 元素出现在视口的任何部分都会触发回调
      };
      
      // 创建新的观察器
      this.observer = new IntersectionObserver((entries) => {
        // 记录所有可见的标题
        const visibleHeadings = entries
          .filter(entry => entry.isIntersecting)
          .map(entry => entry.target);
        
        // 如果有可见的标题
        if (visibleHeadings.length > 0) {
          // 找到最靠前的可见标题
          const firstVisibleHeading = visibleHeadings[0];
          const index = Array.from(headings).indexOf(firstVisibleHeading);
          
          // 更新活跃目录项
          if (index !== -1) {
            this.activeIndex = index;
            
            // 使活跃目录项在目录列表中可见
            this.$nextTick(() => {
              const activeItem = document.querySelector(`.toc-item.active`);
              if (activeItem && activeItem.scrollIntoView) {
                activeItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
              }
            });
          }
        }
      }, options);
      
      // 观察所有标题元素
      headings.forEach(heading => {
        this.observer.observe(heading);
      });
    },
    
    // 跳转到指定标题
    scrollToHeading(id) {
      const el = document.getElementById(id);
      if (el) {
        // 获取目标元素的索引
        const index = this.tocItems.findIndex(item => item.id === id);
        if (index !== -1) {
          this.activeIndex = index;
        }
        
        // 滚动到目标元素
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // 更新URL哈希
        history.pushState(null, null, `#${id}`);
      }
    },
    async checkFollowStatus() {
      try {
        // 确保ID是数字类型
        const followerId = Number(this.user.id);
        const followedId = Number(this.blog.userId);

        if (!followerId || !followedId || followerId === followedId) {
          this.isFollowing = false;
          return;
        }

        const res = await this.$request.get("/follow/checkStatus", {
          params: {
            followerId: followerId,
            followedId: followedId,
          },
        });

        if (res.code === "200") {
          this.isFollowing = res.data;
        }
      } catch (error) {
        console.error("检查关注状态失败:", error);
        this.isFollowing = false;
      }
    },
    async toggleFollow() {
      // 检查是否登录
      if (!this.user.token) {
        this.$message.warning("请先登录后再关注");
        return;
      }

      if (this.followLoading) return; // 防止重复点击
      this.followLoading = true;

      try {
        const action = this.isFollowing ? "unfollow" : "follow";

        // 确保ID是数字类型
        const followerId = parseInt(this.user.id);
        const followedId = parseInt(this.blog.userId);

        console.log("关注/取消关注参数:", {
          followerId: followerId,
          followedId: followedId,
        });

        // 实际API调用
        const res = await this.$request.post(`/follow/${action}`, {
          followerId: followerId,
          followedId: followedId,
        });

        if (res.code === "200") {
          this.isFollowing = !this.isFollowing;
          if (this.isFollowing) {
            this.$message.success("关注成功");
          } else {
            this.$message.success("已取消关注");
          }
        } else {
          this.$message.error(res.msg || "操作失败");
        }
      } catch (error) {
        console.error("操作关注失败", error);
        this.$message.error("操作失败，请稍后重试");
      } finally {
        this.followLoading = false;
      }
    },

    shareBlog() {
      // 获取当前页面URL
      const url = window.location.href;

      // 尝试使用现代浏览器API
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard
          .writeText(url)
          .then(() => {
            this.$message({
              message: "链接已复制到剪贴板",
              type: "success",
              duration: 2000,
            });
          })
          .catch(() => {
            this.fallbackCopy(url);
          });
      } else {
        this.fallbackCopy(url);
      }
    },

    fallbackCopy(text) {
      // 创建临时文本区域
      const textArea = document.createElement("textarea");
      textArea.value = text;
      textArea.style.position = "fixed";
      textArea.style.left = "-9999px";
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();

      try {
        const successful = document.execCommand("copy");
        if (successful) {
          this.$message({
            message: "链接已复制到剪贴板",
            type: "success",
            duration: 2000,
          });
        } else {
          this.$message.error("复制失败，请手动复制链接");
        }
      } catch (err) {
        this.$message.error("复制失败，请手动复制链接");
      }

      document.body.removeChild(textArea);
    },
  },
  watch: {
    user: {
      handler(newVal) {
        if (!newVal.token) {
          this.checkLogin();
        }
      },
      deep: true,
    },
  },
  // 组件销毁时清理观察器
  beforeDestroy() {
    if (this.observer) {
      this.observer.disconnect();
    }
  },
  computed: {
    isDarkMode() {
      return document.body.classList.contains("dark");
    },
    themeClass() {
      return {
        "dark-theme": this.isDarkMode,
      };
    },
  },
};
</script>

<style>
/* 修改基础样式 */
.w-e-text {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.8;
  word-break: break-word;
  overflow-wrap: break-word;
}

/* 重新规范化标题大小 */
.w-e-text h1 {
  font-size: 28px !important;
  line-height: 1.3 !important;
  margin-top: 40px !important;
  margin-bottom: 15px !important;
  font-weight: 600 !important;
  padding-bottom: 10px !important;
  border-bottom: 1px solid rgba(0,0,0,0.1) !important;
}

.w-e-text h2 {
  font-size: 24px !important;
  line-height: 1.3 !important;
  margin-top: 35px !important;
  margin-bottom: 15px !important;
  font-weight: 600 !important;
  padding-bottom: 8px !important;
  border-bottom: 1px solid rgba(0,0,0,0.05) !important;
}

.w-e-text h3 {
  font-size: 20px !important;
  line-height: 1.4 !important;
  margin-top: 30px !important;
  margin-bottom: 12px !important;
  font-weight: 600 !important;
}

.w-e-text h4 {
  font-size: 18px !important;
  line-height: 1.4 !important;
  margin-top: 25px !important;
  margin-bottom: 10px !important;
  font-weight: 600 !important;
}

.w-e-text h5 {
  font-size: 16px !important;
  line-height: 1.5 !important;
  margin-top: 20px !important;
  margin-bottom: 10px !important;
  font-weight: 600 !important;
}

.w-e-text h6 {
  font-size: 15px !important;
  line-height: 1.5 !important;
  margin-top: 18px !important;
  margin-bottom: 8px !important;
  font-weight: 600 !important;
  color: rgba(0,0,0,0.7) !important;
}

/* 修复段落和元素间距问题 */
.w-e-text p {
  margin: 0 0 16px 0 !important;
  font-size: 16px !important;
  line-height: 1.8 !important;
  color: rgba(0,0,0,0.85) !important;
}

/* 修复列表的显示 */
.w-e-text ul,
.w-e-text ol {
  padding-left: 2em !important;
  margin-bottom: 16px !important;
  margin-top: 8px !important;
}

.w-e-text li {
  margin-bottom: 8px !important;
  font-size: 16px !important;
  line-height: 1.6 !important;
}

/* 修复图片显示和间距 */
.w-e-text img {
  max-width: 100% !important;
  height: auto !important;
  display: block !important;
  margin: 20px auto !important;
  border-radius: 8px !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
}

/* 引用块样式优化 */
.w-e-text blockquote {
  border-left: 4px solid #0a4d68 !important;
  padding: 15px 15px 15px 20px !important;
  margin: 20px 0 !important;
  background-color: rgba(10, 77, 104, 0.05) !important;
  color: rgba(0, 0, 0, 0.7) !important;
  font-style: italic !important;
  border-radius: 0 4px 4px 0 !important;
}

/* 代码块样式优化 */
.w-e-text pre {
  background-color: #282c34 !important;
  border-radius: 6px !important;
  padding: 16px !important;
  overflow: auto !important;
  line-height: 1.45 !important;
  margin: 16px 0 !important;
  color: #abb2bf !important;
}

.w-e-text code {
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace !important;
  font-size: 14px !important;
  padding: 2px 4px !important;
  border-radius: 3px !important;
  background-color: rgba(27, 31, 35, 0.05) !important;
}

.w-e-text pre code {
  padding: 0 !important;
  background-color: transparent !important;
  color: inherit !important;
  display: block !important;
  overflow-x: auto !important;
}

/* 标题锚点修复 */
.w-e-text h1, .w-e-text h2, .w-e-text h3, .w-e-text h4, .w-e-text h5, .w-e-text h6 {
  scroll-margin-top: 100px;
  position: relative;
}

/* 添加标题锚点效果 */
.w-e-text h1:hover::after, 
.w-e-text h2:hover::after, 
.w-e-text h3:hover::after, 
.w-e-text h4:hover::after, 
.w-e-text h5:hover::after, 
.w-e-text h6:hover::after {
  content: "#";
  position: absolute;
  left: -20px;
  color: #0a4d68;
  opacity: 0.6;
  font-weight: normal;
}

/* 链接样式优化 */
.w-e-text a {
  color: #0a4d68 !important;
  text-decoration: none !important;
  border-bottom: 1px solid rgba(10, 77, 104, 0.3) !important;
  transition: all 0.2s ease !important;
}

.w-e-text a:hover {
  color: #05bfdb !important;
  border-bottom-color: #05bfdb !important;
}

/* 表格样式优化 */
.w-e-text table {
  border-collapse: collapse !important;
  width: 100% !important;
  margin: 20px 0 !important;
  overflow-x: auto !important;
  display: block !important;
}

.w-e-text table th {
  background-color: #f5f7fa !important;
  color: #333 !important;
  font-weight: 600 !important;
  padding: 12px !important;
  text-align: left !important;
  border: 1px solid #dcdfe6 !important;
}

.w-e-text table td {
  padding: 12px !important;
  border: 1px solid #dcdfe6 !important;
}

.w-e-text table tr:nth-child(even) {
  background-color: #fafafa !important;
}

/* 水平线样式优化 */
.w-e-text hr {
  height: 1px !important;
  background-color: #dcdfe6 !important;
  border: none !important;
  margin: 30px 0 !important;
}

/* 加粗文本增强 */
.w-e-text strong {
  font-weight: 600 !important;
  color: rgba(0,0,0,0.9) !important;
}
</style>

<style lang="less" scoped>
.blog-detail-container {
  position: relative;
  min-height: 100vh;
  background-color: #ffffff00;
  padding: 100px 0;

  &.dark-theme {
    .blog-header {
      background-color: var(--bg-color-secondary);
      color: var(--text-color-primary);
      border-color: var(--border-color);
      box-shadow: var(--card-shadow);

      .blog-title {
        color: var(--text-color-primary);
      }

      .blog-meta {
        color: var(--text-color-secondary);
      }

      .meta-item {
        i {
          color: var(--primary-color);
        }

        .author-link {
          color: var(--primary-color);
          &:hover {
            color: var(--primary-color-hover);
          }
        }
      }
    }

    .blog-content {
      background-color: var(--bg-color-secondary);
      color: var(--text-color-primary);
      border-color: var(--border-color);
      box-shadow: var(--card-shadow);

      .content-wrapper {
        color: var(--text-color-primary);

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
          color: var(--primary-color);
        }

        a {
          color: var(--primary-color);
          &:hover {
            color: var(--primary-color-hover);
          }
        }
      }
    }

    .blog-actions {
      .action-button {
        i {
          background: var(--bg-color-tertiary);
          color: var(--text-color-secondary);
        }

        span,
        .action-label {
          color: var(--text-color-secondary);
        }

        &:hover,
        &.active {
          i {
            background: var(--primary-color-alpha);
            color: var(--primary-color);
          }

          span,
          .action-label {
            color: var(--primary-color);
          }
        }
      }
    }

    .blog-comments {
      background-color: var(--bg-color-secondary);
      color: var(--text-color-primary);
      border-color: var(--border-color);
      box-shadow: var(--card-shadow);

      .section-title {
        color: var(--text-color-primary);
        &:before {
          background: linear-gradient(
            to bottom,
            var(--primary-color),
            var(--primary-color-hover)
          );
        }
      }
    }

    .sidebar-card {
      background-color: var(--bg-color-secondary);
      border-color: var(--border-color);
      box-shadow: var(--card-shadow);
    }

    .author-card {
      .author-avatar {
        border-color: var(--border-color);
        box-shadow: var(--card-shadow);
      }

      .author-name {
        color: var(--text-color-primary);
        &:hover {
          color: var(--primary-color);
        }
      }

      .author-bio {
        color: var(--text-color-secondary);
      }

      .author-stats {
        border-color: var(--border-color);

        .stat-value {
          color: var(--primary-color);
        }

        .stat-label {
          color: var(--text-color-secondary);
        }

        .stat-item:hover {
          .stat-value,
          .stat-label {
            color: var(--primary-color-hover);
          }
        }
      }
    }

    .recommend-card {
      .card-title {
        color: var(--text-color-primary);
        i {
          color: var(--primary-color);
        }
      }

      .recommend-title {
        color: var(--text-color-primary);
        &:hover {
          color: var(--primary-color);
        }
      }

      .recommend-stats {
        color: var(--text-color-secondary);
      }
    }

    .toc-card {
      background-color: var(--bg-color-secondary);
      border-color: var(--border-color);
      box-shadow: var(--card-shadow);

      .toc-item {
        color: var(--text-color-secondary);
        &:hover,
        &.active {
          color: var(--primary-color);
        }
        &.active::before {
          background-color: var(--primary-color);
        }
      }
    }

    .back-button {
      background-color: var(--bg-color-secondary);
      color: var(--text-color-primary);
      border-color: var(--border-color);
      box-shadow: var(--card-shadow);

      &:hover {
        background-color: var(--bg-color-hover);
        color: var(--primary-color);
      }
    }
  }
}

.blog-detail-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 30px;
  padding: 0 20px;
  position: relative;

  @media (max-width: 992px) {
    flex-direction: column;
  }
}

.main-content-area {
  flex: 1;
  padding: 20px;
  margin-right: 280px; /* 320px + 30px间隙 */
  margin-top: -50px;
  min-width: 0; /* 防止内容溢出 */
}

.sidebar-area {
  position: fixed;
  right: 120px;
  top: 100px;
  width: 300px;
  height: calc(100vh - 120px);
  overflow-y: auto; /* 允许内容滚动 */
  z-index: 10;
  transition: all 0.3s ease; /* 添加过渡效果 */

  /* 自定义滚动条样式 */
  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 3px;
  }

  &::-webkit-scrollbar-track {
    background: transparent;
  }

  @media (max-width: 992px) {
    position: static;
    width: 100%;
    height: auto;
    margin-top: 20px;
    overflow-y: visible;
  }
}

/* 博客标题和信息 */
.blog-header {
  background-color: #fff;
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.blog-title {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin-bottom: 20px;
  line-height: 1.4;
}

.blog-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  color: #666;
  font-size: 14px;
  align-items: center;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;

  i {
    font-size: 16px;
    color: #0a4d68;
  }

  .author-link {
    cursor: pointer;
    color: #0a4d68;
    transition: color 0.3s;

    &:hover {
      color: #05bfdb;
      text-decoration: underline;
    }
  }
}

.meta-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-left: auto;

  .el-tag {
    margin: 0;
  }
}

/* 博客内容 */
.blog-content {
  background-color: #fff;
  border-radius: 12px;
  padding: 40px;  /* 增加内边距，改善阅读体验 */
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden; /* 防止内容溢出 */
}

.content-wrapper {
  font-size: 16px;
  line-height: 1.8;
  color: #333;
  max-width: 100%;
  overflow-wrap: break-word;
  word-break: break-word;
}

/* 点赞和收藏 */
.blog-actions {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-bottom: 30px;
}

.action-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s;

  i {
    font-size: 24px;
    color: #666;
    background: #f0f2f5;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 5px;
    transition: all 0.3s;
  }

  span {
    font-size: 14px;
    color: #666;
    margin-bottom: 5px;
  }

  .action-label {
    font-size: 12px;
    color: #999;
  }

  &:hover {
    i {
      background: #e6f7ff;
      color: #05bfdb;
      transform: scale(1.1);
    }
  }

  &.active {
    i {
      background: #e6f7ff;
      color: #05bfdb;
    }

    span,
    .action-label {
      color: #05bfdb;
    }
  }
}

/* 评论区 */
.blog-comments {
  background-color: #fff;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  position: relative;
  padding-left: 15px;

  &:before {
    content: "";
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 4px;
    height: 20px;
    background: linear-gradient(to bottom, #0a4d68, #05bfdb);
    border-radius: 2px;
  }
}

/* 侧边栏卡片通用样式 */
.sidebar-card {
  background-color: #fff;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* 作者卡片 */
.author-card {
  text-align: center;
  padding: 25px 20px;
  margin-bottom: 20px;
}

.author-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.author-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #f0f2f5;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    transform: scale(1.05);
    border-color: #05bfdb;
  }
}

.author-info {
  flex: 1;
  text-align: left;
  margin-left: 15px;
}

.author-name {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
  cursor: pointer;
  transition: color 0.3s;

  &:hover {
    color: #05bfdb;
  }
}

.author-bio {
  font-size: 14px;
  color: #666;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 关注按钮样式 */
.author-follow {
  margin-top: 10px;
  margin-bottom: 15px;

  .el-button {
    width: 100%;
    border-radius: 20px;
    font-weight: 500;
    transition: all 0.3s;

    &.is-following {
      background-color: #f0f2f5;
      color: #0a4d68;
      border-color: #e0e0e0;

      &:hover {
        background-color: #f9d7d7;
        color: #e45649;
        border-color: #f9d7d7;
      }
    }
  }
}

.author-stats {
  display: flex;
  justify-content: space-around;
  text-align: center;
  border-top: 1px solid #f0f2f5;
  padding-top: 15px;
}

.stat-item {
  flex: 1;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    transform: translateY(-2px);
    .stat-value {
      color: #05bfdb;
    }
    .stat-label {
      color: #05bfdb;
    }
  }
}

.stat-value {
  font-size: 18px;
  font-weight: 600;
  color: #0a4d68;
  transition: color 0.3s;
}

.stat-label {
  font-size: 12px;
  color: #666;
  margin-top: 5px;
  transition: color 0.3s;
}

/* 推荐卡片 */
.recommend-card {
  padding: 20px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 15px;
  display: flex;
  align-items: center;

  i {
    color: #05bfdb;
    margin-right: 8px;
    font-size: 20px;
  }
}

.recommend-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.recommend-item {
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    .recommend-title {
      color: #05bfdb;
    }
  }
}

.recommend-title {
  font-size: 15px;
  font-weight: 500;
  color: #333;
  margin-bottom: 5px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.5;
  transition: color 0.3s;
}

.recommend-stats {
  display: flex;
  gap: 15px;
  font-size: 13px;
  color: #999;

  i {
    margin-right: 3px;
  }
}

/* 广告卡片 */
.ad-card {
  padding: 20px;
}

.ad-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.ad-text {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

.ad-image {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  object-fit: cover;
}

/* 返回按钮 */
.back-button {
  position: fixed;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  background-color: #fff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  color: #666;
  font-size: 14px;
  z-index: 10;

  i {
    margin-right: 5px;
    font-size: 16px;
  }

  &:hover {
    background-color: #f5f7fa;
    transform: translateY(-50%) translateX(5px);
    color: #05bfdb;
  }

  @media (max-width: 768px) {
    left: 10px;
    padding: 10px;

    span {
      display: none;
    }

    i {
      margin-right: 0;
    }
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .blog-detail-container {
    padding: 20px 0;
  }

  .blog-header,
  .blog-content,
  .blog-comments {
    padding: 20px;
  }

  .blog-title {
    font-size: 22px;
    line-height: 1.4;
  }

  .blog-meta {
    gap: 10px;
  }

  .meta-tags {
    margin-left: 0;
    margin-top: 10px;
    width: 100%;
  }

  .blog-actions {
    gap: 20px;
  }

  .blog-content {
    padding: 20px;
  }
  
  .content-wrapper {
    font-size: 15px;
  }
}

/* 目录卡片样式 */
.toc-card {
  background-color: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 100px;
}

.toc-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
  display: flex;
  align-items: center;
  
  i {
    margin-right: 8px;
    color: #0a4d68;
  }
}

.toc-list {
  max-height: 60vh;
  overflow-y: auto;
  padding-right: 10px;
  
  &::-webkit-scrollbar {
    width: 4px;
  }
  
  &::-webkit-scrollbar-thumb {
    background-color: rgba(10, 77, 104, 0.3);
    border-radius: 4px;
  }
  
  &::-webkit-scrollbar-track {
    background-color: transparent;
  }
}

.toc-item {
  padding: 8px 10px 8px 15px;
  border-radius: 6px;
  margin-bottom: 5px;
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
  font-size: 14px;
  display: flex;
  align-items: center;
  color: #666;
  
  &::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 3px;
    border-radius: 3px;
    opacity: 0;
    transition: all 0.2s;
  }
  
  &:hover {
    background-color: rgba(10, 77, 104, 0.05);
    color: #0a4d68;
    
    &::before {
      opacity: 0.5;
      background-color: #0a4d68;
    }
  }
  
  &.active {
    background-color: rgba(10, 77, 104, 0.1);
    color: #0a4d68;
    font-weight: 500;
    
    &::before {
      opacity: 1;
      background-color: #0a4d68;
    }
  }
}

.toc-level-1 {
  padding-left: 15px;
  font-weight: 500;
}

.toc-level-2 {
  padding-left: 25px;
}

.toc-level-3 {
  padding-left: 35px;
  font-size: 13px;
}

.toc-level-4,
.toc-level-5,
.toc-level-6 {
  padding-left: 45px;
  font-size: 13px;
  color: #888;
}

.toc-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.toc-empty {
  padding: 15px;
  color: #999;
  text-align: center;
  font-style: italic;
  background-color: rgba(0, 0, 0, 0.02);
  border-radius: 6px;
}
</style>
