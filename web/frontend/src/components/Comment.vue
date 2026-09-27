<template>
  <!--  评论开始  -->
  <div class="card comment-container" :class="themeClass">
    <div class="comment-header-wrap">
      <h2 class="comment-header">评论 {{ commentCount }}</h2>
      <div class="comment-sort">
        <el-dropdown @command="handleSort">
          <span class="el-dropdown-link">
            {{ currentSort.label }}
            <i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item
              v-for="item in sortOptions"
              :key="item.value"
              :command="item.value"
            >
              <i :class="item.icon"></i> {{ item.label }}
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>

    <!-- 评论输入框 -->
    <div class="comment-input-box" v-if="user.token">
      <el-input
        type="textarea"
        placeholder="请输入评论内容（最多500字）"
        v-model="commentContent"
        :maxlength="500"
        show-word-limit
        ref="commentInput"
      ></el-input>
      <div class="comment-toolbar">
        <div class="emoji-picker">
          <el-popover
            placement="bottom"
            trigger="click"
            popper-class="emoji-popper"
          >
            <div class="emoji-container">
              <span
                v-for="emoji in emojiList"
                :key="emoji"
                class="emoji-item"
                @click="insertEmoji(emoji)"
                >{{ emoji }}</span
              >
            </div>
            <div class="emoji-btn" slot="reference">
              <i class="el-icon-sunny"></i>
              <span class="emoji-text">表情</span>
            </div>
          </el-popover>
        </div>
        <el-button type="primary" @click="addComment">评 论</el-button>
      </div>
    </div>
    <div v-else class="login-tip">
      请<el-button type="text" @click="$router.push('/login')">登录</el-button
      >后发表评论
    </div>

    <!-- 评论列表 -->
    <div class="comment-list">
      <!-- 一级评论 -->
      <div
        class="comment-item"
        v-for="item in sortedCommentList"
        :key="item.id"
      >
        <div class="comment-avatar" @click="goToAuthorHome(item.userId)">
          <img
            :src="item.avatar || require('@/assets/imgs/bgc2.jpg')"
            @error="handleAvatarError($event)"
            alt=""
          />
        </div>
        <div class="comment-content" :data-comment-id="item.id">
          <div class="comment-main">
            <div class="comment-user" @click="goToAuthorHome(item.userId)">
              {{ item.userName || "匿名用户" }}
            </div>
            <div
              class="comment-text"
              v-html="formatContent(item.content)"
            ></div>
            <div class="comment-info">
              <span class="comment-time"
                ><i class="el-icon-time"></i> {{ item.time }}</span
              >
              <span
                class="comment-action"
                :class="{ active: item.showReplyInput }"
                @click="handleShowReplyInput(item)"
                v-if="user.token"
              >
                <i class="el-icon-s-comment"></i> 回复
              </span>
              <span
                class="comment-action delete"
                @click="del(item.id)"
                v-if="item.userId === user.id"
              >
                <i class="el-icon-delete"></i> 删除
              </span>
            </div>
            <!-- 回复输入框 -->
            <div class="reply-input" v-if="item.showReplyInput">
              <div class="reply-preview" v-if="item.content">
                <div class="preview-title">
                  回复 {{ item.userName }} 的评论：
                </div>
                <div class="preview-content">
                  {{ formatPreview(item.content) }}
                </div>
              </div>
              <el-input
                type="textarea"
                placeholder="请输入回复内容（最多500字）"
                v-model="item.replyContent"
                :maxlength="500"
                show-word-limit
                ref="replyInput"
              ></el-input>
              <div class="comment-toolbar">
                <div class="emoji-picker">
                  <el-popover
                    placement="bottom"
                    trigger="click"
                    popper-class="emoji-popper"
                  >
                    <div class="emoji-container">
                      <span
                        v-for="emoji in emojiList"
                        :key="emoji"
                        class="emoji-item"
                        @click="insertEmoji(emoji, item)"
                        >{{ emoji }}</span
                      >
                    </div>
                    <div class="emoji-btn" slot="reference">
                      <i class="el-icon-sunny"></i>
                      <span class="emoji-text">表情</span>
                    </div>
                  </el-popover>
                </div>
                <el-button type="primary" @click="addReplay(item)"
                  >回 复</el-button
                >
              </div>
            </div>
          </div>

          <!-- 子评论列表 -->
          <div class="reply-list" v-if="item.children && item.children.length">
            <div class="reply-count">{{ item.children.length }}条回复</div>
            <div class="reply-item" v-for="sub in item.children" :key="sub.id">
              <div class="comment-avatar" @click="goToAuthorHome(sub.userId)">
                <img
                  :src="sub.avatar || require('@/assets/imgs/bgc2.jpg')"
                  @error="handleAvatarError($event)"
                  alt=""
                />
              </div>
              <div class="reply-content" :data-comment-id="sub.id">
                <div class="reply-user">
                  <span class="user-name" @click="goToAuthorHome(sub.userId)">{{
                    sub.userName || "匿名用户"
                  }}</span>
                  <span class="reply-level">{{
                    sub.originalReplyChain ? "三级评论" : "二级评论"
                  }}</span>
                  <span class="reply-target">
                    <template v-if="sub.replyChain">
                      回复
                      <span
                        class="reply-name"
                        @click="scrollToComment(sub.replyChain.id)"
                        >@{{ sub.replyChain.userName }}</span
                      >
                      <span
                        class="reply-content-preview"
                        @click="scrollToComment(sub.replyChain.id)"
                        >「{{ formatPreview(sub.replyChain.content) }}」</span
                      >
                    </template>
                  </span>
                </div>
                <div
                  class="comment-text"
                  v-html="formatContent(sub.content)"
                ></div>
                <div class="comment-info">
                  <span class="comment-time">{{ sub.time }}</span>
                  <span
                    class="comment-action"
                    :class="{ active: sub.showReplyInput }"
                    @click="handleShowReplyInput(sub)"
                    v-if="user.token"
                  >
                    回复
                  </span>
                  <span
                    class="comment-action delete"
                    @click="del(sub.id)"
                    v-if="sub.userId === user.id"
                  >
                    删除
                  </span>
                </div>
                <!-- 子评论的回复输入框 -->
                <div class="reply-input" v-if="sub.showReplyInput">
                  <el-input
                    type="textarea"
                    :placeholder="'回复 @' + sub.userName"
                    v-model="sub.replyContent"
                    :maxlength="500"
                    show-word-limit
                    ref="subReplyInput"
                  ></el-input>
                  <div class="comment-toolbar">
                    <div class="emoji-picker">
                      <el-popover
                        placement="bottom"
                        trigger="click"
                        popper-class="emoji-popper"
                      >
                        <div class="emoji-container">
                          <span
                            v-for="emoji in emojiList"
                            :key="emoji"
                            class="emoji-item"
                            @click="insertEmoji(emoji, sub)"
                            >{{ emoji }}</span
                          >
                        </div>
                        <div class="emoji-btn" slot="reference">
                          <i class="el-icon-sunny"></i>
                          <span class="emoji-text">表情</span>
                        </div>
                      </el-popover>
                    </div>
                    <el-button
                      type="primary"
                      size="small"
                      @click="addReplay(sub)"
                      >发送</el-button
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!--  评论结束  -->
</template>

<script>
export default {
  name: "CommentComponent",
  props: {
    fid: null,
    module: null,
  },
  data() {
    return {
      commentCount: 0,
      commentContent: "",
      commentList: [],
      user: JSON.parse(localStorage.getItem("xm-user") || "{}"),
      allComments: {}, // 存储所有评论的映射，用于快速查找
      currentSort: { value: "newest", label: "最新", icon: "el-icon-time" },
      sortOptions: [
        { value: "newest", label: "最新", icon: "el-icon-time" },
        { value: "oldest", label: "最早", icon: "el-icon-time" },
        { value: "hot", label: "最热", icon: "el-icon-star-on" },
      ],
      emojiList: [
        "😊",
        "😂",
        "🤣",
        "❤️",
        "😍",
        "🤔",
        "😮",
        "😢",
        "😠",
        "🎉",
        "👍",
        "👎",
        "🙏",
        "💪",
        "🌹",
        "✨",
        "🎵",
        "🌈",
        "☀️",
        "��",
        "⭐",
        "🔥",
        "💯",
        "💕",
      ],
    };
  },
  computed: {
    sortedCommentList() {
      const list = [...this.commentList];
      switch (this.currentSort.value) {
        case "oldest":
          return list.sort((a, b) => new Date(a.time) - new Date(b.time));
        case "hot":
          return list.sort(
            (a, b) => (b.children?.length || 0) - (a.children?.length || 0)
          );
        case "newest":
        default:
          return list.sort((a, b) => new Date(b.time) - new Date(a.time));
      }
    },
    isDarkMode() {
      return document.body.classList.contains("dark");
    },
    themeClass() {
      return {
        "dark-theme": this.isDarkMode,
      };
    },
  },
  created() {
    this.loadComment();
  },
  methods: {
    // 处理排序
    handleSort(command) {
      this.currentSort = this.sortOptions.find(
        (item) => item.value === command
      );
    },
    // 插入表情
    insertEmoji(emoji, item) {
      if (item) {
        // 回复框插入表情
        const newContent = (item.replyContent || "") + emoji;
        this.$set(item, "replyContent", newContent);
      } else {
        // 评论框插入表情
        this.commentContent += emoji;
      }
    },
    // 格式化评论内容（转换表情）
    formatContent(content) {
      return content;
    },
    // 查找评论内容
    findReplyContent(pid) {
      const comment = this.findCommentById(pid);
      if (comment) {
        return comment.content.length > 20
          ? comment.content.substring(0, 20) + "..."
          : comment.content;
      }
      return "";
    },
    // 递归查找评论
    findCommentById(id) {
      for (const item of this.commentList) {
        if (item.id === id) return item;
        if (item.children) {
          for (const child of item.children) {
            if (child.id === id) return child;
          }
        }
      }
      return null;
    },
    del(id) {
      // 单个删除
      this.$confirm("您确定删除吗？", "确认删除", { type: "warning" })
        .then((response) => {
          this.$request.delete("/comment/delete/" + id).then((res) => {
            if (res.code === "200") {
              // 表示操作成功
              this.$message.success("操作成功");
              this.loadComment();
            } else {
              this.$message.error(res.msg); // 弹出错误的信息
            }
          });
        })
        .catch(() => {});
    },
    handleShowReplyInput(item) {
      this.$set(item, "showReplyInput", !item.showReplyInput);
    },
    addReplay(item) {
      if (!this.user.id) {
        this.$message.warning("请先登录");
        return;
      }
      if (!item.replyContent?.trim()) {
        this.$message.warning("请输入回复内容");
        return;
      }
      if (item.replyContent.length > 500) {
        this.$message.warning("回复内容不能超过500字");
        return;
      }

      // 构建回复数据
      const replyData = {
        content: item.replyContent,
        fid: this.fid,
        module: this.module,
        userId: this.user.id,
        pid: item.id,
        rootId: item.rootId || item.id,
      };

      // 如果是回复其他评论的评论，添加被回复用户ID
      if (item.replyToComment) {
        replyData.replyUserId = item.userId;
        replyData.replyToCommentId = item.id;
      }

      this.$request
        .post("/comment/add", replyData)
        .then((res) => {
          if (res.code === "200") {
            this.$message.success("回复成功");
            item.replyContent = "";
            item.showReplyInput = false;
            this.loadComment();
          } else {
            this.$message.error(res.msg || "回复失败");
          }
        })
        .catch((error) => {
          console.error("回复失败:", error);
          this.$message.error("回复失败");
        });
    },
    handleAvatarError(e) {
      e.target.src = require("@/assets/imgs/bgc2.jpg");
    },
    async loadComment() {
      if (!this.user.token) {
        this.commentList = [];
        this.commentCount = 0;
        return;
      }

      try {
        const res = await this.$request.get("/comment/selectPage", {
          params: {
            fid: this.fid,
            module: this.module,
            pageNum: 1,
            pageSize: 1000,
          },
        });
        if (res.code === "200") {
          // 处理评论数据，确保每条评论都有用户信息
          const list = res.data.list || res.data.records || [];
          this.commentList = await this.processCommentList(list);
          this.commentCount = res.data.total || list.length;
        } else {
          this.commentList = [];
          this.commentCount = 0;
        }
      } catch (error) {
        console.error("加载评论失败:", error);
        this.commentList = [];
        this.commentCount = 0;
      }
    },
    async processCommentList(list) {
      // 处理每条评论，添加用户信息
      const processedList = [];
      const commentMap = new Map(); // 用于存储所有评论的映射

      // 第一次遍历，建立评论映射和获取用户信息
      for (const comment of list) {
        const processedComment = {
          ...comment,
          children: [],
          replyToComment: null,
          userName: "匿名用户",
          avatar: null,
        };

        // 获取评论者信息
        if (comment.userId) {
          try {
            const userRes = await this.$request.get(
              `/user/selectById/${comment.userId}`
            );
            if (userRes.code === "200") {
              processedComment.userName = userRes.data.name || "匿名用户";
              processedComment.avatar = userRes.data.avatar;
            }
          } catch (error) {
            console.error("获取用户信息失败:", error);
          }
        }

        commentMap.set(comment.id, processedComment);
      }

      // 第二次遍历，构建二级评论结构
      for (const comment of list) {
        const processedComment = commentMap.get(comment.id);

        if (comment.pid) {
          // 这是一个回复评论，找到根评论
          let rootComment = commentMap.get(comment.rootId || comment.pid);
          if (rootComment) {
            // 找到直接回复的评论
            const replyToComment = commentMap.get(comment.pid);
            if (replyToComment) {
              processedComment.replyToComment = replyToComment;
              // 构建回复链，包含评论内容
              processedComment.replyChain = {
                id: replyToComment.id,
                userName: replyToComment.userName,
                content: replyToComment.content,
              };
              // 如果回复的不是一级评论，添加原始回复链
              if (replyToComment.pid) {
                processedComment.originalReplyChain = {
                  id: rootComment.id,
                  userName: rootComment.userName,
                  content: rootComment.content,
                };
              }
            }
            // 将评论添加到根评论的子评论列表中
            rootComment.children.push(processedComment);
          }
        } else {
          // 这是一个一级评论
          processedList.push(processedComment);
        }
      }

      return processedList;
    },
    addComment() {
      if (!this.user.id) {
        this.$message.warning("请先登录");
        return;
      }
      if (!this.commentContent.trim()) {
        this.$message.warning("请输入评论内容");
        return;
      }
      if (this.commentContent.length > 500) {
        this.$message.warning("评论内容不能超过500字");
        return;
      }
      this.$request
        .post("/comment/add", {
          content: this.commentContent,
          fid: this.fid,
          module: this.module,
          userId: this.user.id,
        })
        .then((res) => {
          if (res.code === "200") {
            this.$message.success("评论成功");
            this.commentContent = "";
            this.loadComment(); // 重新加载数据
          } else {
            this.$message.error(res.msg || "评论失败");
          }
        })
        .catch((error) => {
          console.error("评论失败:", error);
          this.$message.error("评论失败");
        });
    },
    formatReplyContent(content) {
      if (!content) return "";
      return content.length > 20 ? content.substring(0, 20) + "..." : content;
    },
    // 格式化回复链显示
    formatReplyChain(comment) {
      if (!comment.replyChain) return "";
      return comment.replyChain
        .map(
          (reply) =>
            `<span class="reply-chain-item">
          <span class="reply-name">${reply.userName}</span>
          <span class="reply-content">${this.formatReplyContent(
            reply.content
          )}</span>
        </span>`
        )
        .join(" > ");
    },
    scrollToComment(commentId) {
      const commentEl = document.querySelector(
        `[data-comment-id="${commentId}"]`
      );
      if (commentEl) {
        commentEl.scrollIntoView({ behavior: "smooth" });
        // 添加高亮效果
        commentEl.classList.add("highlight");
        setTimeout(() => {
          commentEl.classList.remove("highlight");
        }, 2000);
      }
    },
    // 添加新的格式化预览方法
    formatPreview(content) {
      if (!content) return "";
      // 移除HTML标签
      content = content.replace(/<[^>]+>/g, "");
      // 限制长度为30个字符
      return content.length > 30 ? content.substring(0, 30) + "..." : content;
    },
    goToAuthorHome(userId) {
      if (userId) {
        this.$router.push({
          path: "/front/authorHome",
          query: { authorId: userId },
        });
      }
    },
  },
  watch: {
    user: {
      handler(newVal) {
        this.loadComment();
      },
      deep: true,
    },
  },
};
</script>

<style lang="less" scoped>
.comment-container {
  padding: 24px;
  background: var(--bg-color-secondary);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;

  &.dark-theme {
    background-color: var(--bg-color-secondary);
    border-color: var(--border-color);
    box-shadow: var(--card-shadow);

    .comment-header {
      color: var(--text-color-primary);
    }

    .el-dropdown-link {
      color: var(--text-color-secondary);
    }

    .comment-input-box {
      /deep/ .el-textarea__inner {
        background-color: #d9d9d933 !important;
        border-color: var(--border-color);
        color: white;

        &::placeholder {
          color: var(--text-color-placeholder);
        }
      }
    }

    .emoji-btn {
      background-color: var(--bg-color-tertiary);
      color: var(--text-color-secondary);

      &:hover {
        background-color: var(--bg-color-hover);
        color: var(--primary-color);
      }
    }

    .emoji-container {
      background-color: var(--bg-color-secondary);
      border-color: var(--border-color);

      .emoji-item:hover {
        background-color: var(--bg-color-hover);
      }
    }

    .login-tip {
      background-color: var(--bg-color-tertiary);
      color: var(--text-color-secondary);
    }

    .comment-item {
      border-bottom-color: var(--border-color);

      .comment-user {
        color: var(--text-color-primary);

        &:hover {
          color: var(--primary-color);
        }
      }

      .comment-text {
        color: var(--text-color-primary);
      }

      .comment-info,
      .comment-time {
        color: var(--text-color-secondary);
      }

      .comment-action {
        color: var(--text-color-secondary);

        &:hover,
        &.active {
          color: var(--primary-color);
        }

        &.delete:hover {
          color: var(--danger-color);
        }
      }
    }

    .reply-list {
      background-color: var(--bg-color-tertiary);
      border-color: var(--border-color);

      .reply-count {
        color: var(--text-color-primary);
      }

      .reply-item {
        border-bottom-color: var(--border-color);
      }

      .user-name {
        color: var(--text-color-primary);

        &:hover {
          color: var(--primary-color);
        }
      }

      .reply-level {
        background: var(--primary-color);
        color: var(--white);
      }

      .reply-target {
        color: var(--text-color-secondary);

        .reply-name {
          color: var(--primary-color);
        }

        .reply-content-preview {
          background: var(--bg-color-tertiary);
          color: var(--text-color-secondary);

          &:hover {
            background: var(--bg-color-hover);
            color: var(--primary-color);
          }
        }
      }
    }

    .reply-input {
      background-color: var(--bg-color-tertiary);
      border-color: var(--border-color);
    }

    .reply-preview {
      background-color: var(--bg-color-tertiary);
      border-color: var(--border-color);

      .preview-title {
        color: var(--text-color-primary);
      }

      .preview-content {
        color: var(--text-color-secondary);
      }
    }
  }
}

.comment-header-wrap {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.comment-header {
  font-size: 22px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 24px;
}

.comment-sort {
  cursor: pointer;
}

.el-dropdown-link {
  color: #666;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.comment-input-box {
  margin-bottom: 30px;
}

.comment-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.emoji-picker {
  cursor: pointer;
  transition: color 0.3s;
}

.emoji-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 4px;
  background-color: #f5f7fa;
  transition: all 0.3s;
  color: #595959;
}

.emoji-btn:hover {
  background-color: #e6f7ff;
  color: #1890ff;
}

.emoji-btn i {
  font-size: 16px;
}

.emoji-text {
  font-size: 13px;
  color: #666;
}

.emoji-container {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 8px;
  padding: 8px;
  background: #fff;
  border-radius: 4px;
}

.emoji-item {
  cursor: pointer;
  font-size: 20px;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.3s;
  text-align: center;
}

.emoji-item:hover {
  background-color: #f0f0f0;
}

.comment-list {
  margin-top: 20px;
}

.comment-item {
  display: flex;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.comment-avatar {
  width: 40px;
  height: 40px;
  margin-right: 15px;
  flex-shrink: 0;
  cursor: pointer;
  transition: transform 0.3s;
}

.comment-avatar:hover {
  transform: scale(1.05);
}

.comment-avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.comment-content {
  flex: 1;
  min-width: 0;
}

.comment-main {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 10px;
  position: relative;
  border: 1px solid #f0f0f0;
}

.comment-user {
  font-weight: bold;
  font-size: 15px;
  color: #000;
  cursor: pointer;
  transition: color 0.3s;
}

.comment-user:hover {
  color: #1890ff;
  text-decoration: underline;
}

.comment-text {
  margin: 12px 0;
  color: #000000;
  line-height: 1.8;
  font-size: 14px;
  word-break: break-word;
}

.comment-info {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-top: 12px;
  color: #666;
  font-size: 13px;
}

.comment-time {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #8c8c8c;
}

.comment-time i {
  font-size: 14px;
}

.comment-action {
  cursor: pointer;
  transition: all 0.3s;
  color: #595959;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.comment-action:hover,
.comment-action.active {
  color: #1890ff;
}

.comment-action.delete:hover {
  color: #ff4d4f;
}

.comment-action i {
  font-size: 14px;
}

.reply-list {
  margin-top: 16px;
  margin-left: 55px;
  position: relative;
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

.reply-count {
  font-size: 14px;
  color: #000000;
  margin-bottom: 16px;
  font-weight: 500;
}

.reply-item {
  display: flex;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.reply-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.reply-content {
  flex: 1;
  min-width: 0;
  background: #fff;
  padding: 16px;
  border-radius: 8px;
  position: relative;
}

.reply-user {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 8px;
}

.user-name {
  font-weight: 600;
  color: #000000; /* 改为纯黑色 */
  font-size: 14px;
  cursor: pointer;
  transition: color 0.3s;
}

.user-name:hover {
  color: #1890ff;
  text-decoration: underline;
}

.reply-level {
  font-size: 12px;
  color: #fff;
  background: #1890ff;
  padding: 2px 6px;
  border-radius: 4px;
  margin-left: 8px;
}

.reply-target {
  color: #595959;
  font-size: 14px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-left: 8px;
}

.reply-name {
  color: #1890ff;
  cursor: pointer;
}

.reply-name:hover {
  opacity: 0.8;
}

.reply-separator {
  display: none;
}

.reply-content-preview {
  color: #666;
  font-size: 14px;
  background: #f5f7fa;
  padding: 4px 12px;
  border-radius: 4px;
  margin-left: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.reply-content-preview:hover {
  background: #e6f7ff;
  color: #1890ff;
}

.reply-input {
  margin-top: 12px;
  background: #fff;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

.comment-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

/* 优化表情选择器 */
.emoji-btn {
  padding: 4px 8px;
  font-size: 13px;
  color: #595959;
  background: #f5f7fa;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.emoji-btn:hover {
  background: #e6f7ff;
  color: #1890ff;
}

.login-tip {
  text-align: center;
  color: #595959;
  padding: 16px 0;
  margin-bottom: 20px;
  background: #f8f9fa;
  border-radius: 6px;
}

.reply-chain {
  color: #666;
  font-size: 13px;
}

.reply-chain-item {
  display: inline-flex;
  align-items: center;
}

.reply-chain-item .reply-name {
  color: #2a60c9;
  margin-right: 4px;
}

.reply-chain-item .reply-content {
  color: #999;
  font-size: 12px;
}

.reply-chain-item + .reply-chain-item::before {
  content: ">";
  margin: 0 4px;
  color: #999;
}

.highlight {
  animation: highlight 1s ease-out;
}

@keyframes highlight {
  0% {
    background-color: rgba(24, 144, 255, 0.1);
  }
  100% {
    background-color: transparent;
  }
}

.comment-item[data-comment-id] {
  scroll-margin-top: 60px;
}

.reply-preview {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 12px 16px;
  margin-bottom: 12px;
  font-size: 14px;
  border: 1px solid #f0f0f0;
}

.preview-title {
  color: #262626;
  margin-bottom: 6px;
  font-weight: 500;
}

.preview-content {
  color: #595959;
  font-style: normal;
  line-height: 1.6;
}

/* 修改输入框计数器样式 */
::v-deep .el-input__count {
  color: #8c8c8c;
  font-size: 12px;
  background: transparent !important;
  padding: 0 8px;
}

::v-deep .el-input__count-inner {
  background: transparent !important;
}

/* 添加超出字数限制时的样式 */
::v-deep .el-input__count.is-exceed {
  color: #f56c6c;
}

/* 优化回复链样式 */
.reply-target {
  line-height: 1.6;
}

.reply-name {
  cursor: pointer;
  transition: color 0.2s;
}

.reply-name:hover {
  color: #1890ff;
  text-decoration: underline;
}

/* 添加评论内容过长时的渐变效果 */
.comment-text {
  position: relative;
  max-height: 300px;
  overflow: hidden;
}

.comment-text.expanded {
  max-height: none;
}

.comment-text:not(.expanded)::after {
  display: none;
}

.expand-btn {
  color: #2a60c9;
  cursor: pointer;
  font-size: 13px;
  margin-top: 8px;
  display: inline-block;
}

.expand-btn:hover {
  text-decoration: underline;
}

/* 优化输入框样式 */
::v-deep .el-textarea__inner {
  padding: 12px;
  font-size: 14px;
  color: #262626;
  border-color: #e8e8e8;
}

::v-deep .el-textarea__inner:focus {
  border-color: #1890ff;
}

/* 登录提示样式优化 */
.login-tip {
  text-align: center;
  color: #595959;
  padding: 16px 0;
  margin-bottom: 20px;
  background: #f8f9fa;
  border-radius: 6px;
}

::v-deep .el-button--text {
  color: white;
  font-weight: 500;
  padding: 0 4px;
}

::v-deep .el-button--text:hover {
  color: orangered;
}

/* 添加跳转时的高亮动画效果 */
@keyframes highlight {
  0% {
    background-color: rgba(24, 144, 255, 0.2);
    transform: scale(1.01);
  }
  100% {
    background-color: transparent;
    transform: scale(1);
  }
}

.highlight {
  animation: highlight 1s ease-out;
}

/* 优化滚动定位 */
.comment-content[data-comment-id],
.reply-content[data-comment-id] {
  scroll-margin-top: 80px;
  transition: background-color 0.3s;
}
</style>
