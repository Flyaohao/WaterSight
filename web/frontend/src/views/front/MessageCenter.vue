<template>
  <div class="message-center">
    <div class="message-header">
      <h2>消息中心</h2>
      <div class="message-actions">
        <el-button
          type="danger"
          size="small"
          @click="handleBatchDelete"
          :disabled="selectedMessages.length === 0"
        >
          批量删除
        </el-button>
        <el-button
          type="primary"
          size="small"
          @click="handleBatchRead"
          :disabled="selectedMessages.length === 0"
        >
          标记已读
        </el-button>
      </div>
    </div>

    <el-tabs v-model="activeTab" @tab-click="handleTabClick">
      <el-tab-pane label="全部消息" name="all">
        <span slot="label">
          全部消息
          <el-badge
            v-if="unreadCounts.all > 0"
            :value="unreadCounts.all"
            class="badge"
            type="danger"
          ></el-badge>
        </span>
      </el-tab-pane>
      <el-tab-pane label="系统通知" name="system">
        <span slot="label">
          系统通知
          <el-badge
            v-if="unreadCounts.system > 0"
            :value="unreadCounts.system"
            class="badge"
            type="danger"
          ></el-badge>
        </span>
      </el-tab-pane>
      <el-tab-pane label="点赞" name="like">
        <span slot="label">
          点赞
          <el-badge
            v-if="unreadCounts.like > 0"
            :value="unreadCounts.like"
            class="badge"
            type="danger"
          ></el-badge>
        </span>
      </el-tab-pane>
      <el-tab-pane label="收藏" name="collect">
        <span slot="label">
          收藏
          <el-badge
            v-if="unreadCounts.collect > 0"
            :value="unreadCounts.collect"
            class="badge"
            type="danger"
          ></el-badge>
        </span>
      </el-tab-pane>
      <el-tab-pane label="关注" name="follow">
        <span slot="label">
          关注
          <el-badge
            v-if="unreadCounts.follow > 0"
            :value="unreadCounts.follow"
            class="badge"
            type="danger"
          ></el-badge>
        </span>
      </el-tab-pane>
      <el-tab-pane label="评论" name="comment">
        <span slot="label">
          评论
          <el-badge
            v-if="unreadCounts.comment > 0"
            :value="unreadCounts.comment"
            class="badge"
            type="danger"
          ></el-badge>
        </span>
      </el-tab-pane>
    </el-tabs>

    <!-- 消息列表 -->
    <template v-if="loading">
      <div class="loading-container">
        <i class="el-icon-loading"></i>
        <p>加载中...</p>
      </div>
    </template>
    <template v-else>
      <div class="message-list">
        <el-table
          ref="messageTable"
          :data="filteredMessages"
          @selection-change="handleSelectionChange"
          style="width: 100%"
        >
          <el-table-column type="selection" width="55"></el-table-column>
          <el-table-column label="消息内容" min-width="300">
            <template slot-scope="scope">
              <div
                class="message-content"
                :class="{ unread: !scope.row.isRead }"
              >
                <div
                  class="message-icon"
                  :class="getMessageTypeClass(scope.row.type)"
                >
                  <i :class="getMessageIcon(scope.row.type)"></i>
                </div>
                <div class="message-body">
                  <div class="message-text">
                    <template v-if="scope.row.fromUser">
                      <span
                        class="interactive-text username"
                        @click="goToUserProfile(scope.row.fromUserId)"
                      >
                        {{ scope.row.fromUser }}
                      </span>
                    </template>
                    <span class="message-action">{{
                      getMessageAction(scope.row.type)
                    }}</span>
                    <template v-if="scope.row.targetTitle">
                      <span
                        class="interactive-text target-title"
                        @click="goToTarget(scope.row)"
                      >
                        《{{ scope.row.targetTitle }}》
                      </span>
                    </template>
                    <template v-if="scope.row.content">
                      <div class="message-detail-content">
                        {{ scope.row.content }}
                      </div>
                    </template>
                  </div>
                  <div class="message-meta">
                    <span class="message-time">{{
                      formatDate(scope.row.createTime)
                    }}</span>
                    <span v-if="!scope.row.isRead" class="unread-tag"
                      >未读</span
                    >
                  </div>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180" align="center">
            <template slot-scope="scope">
              <el-button
                type="text"
                size="small"
                @click="viewDetail(scope.row)"
              >
                查看详情
              </el-button>
              <el-button
                type="text"
                size="small"
                @click="markAsRead(scope.row)"
                v-if="!scope.row.isRead"
              >
                标记已读
              </el-button>
              <el-button
                type="text"
                size="small"
                class="delete-btn"
                @click="deleteMessage(scope.row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination-container">
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-sizes="[10, 20, 50, 100]"
            :page-size="pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
          >
          </el-pagination>
        </div>
      </div>
    </template>

    <!-- 消息详情对话框 -->
    <el-dialog
      title="消息详情"
      :visible.sync="detailDialogVisible"
      width="500px"
    >
      <div class="message-detail">
        <div class="detail-item">
          <label>发送时间：</label>
          <span>{{ formatDate(currentMessage.createTime) }}</span>
        </div>
        <div class="detail-item">
          <label>消息类型：</label>
          <span>{{ getMessageType(currentMessage.type) }}</span>
        </div>
        <div class="detail-item" v-if="currentMessage.fromUser">
          <label>发送者：</label>
          <span
            class="username"
            @click="
              goToUserProfile(
                currentMessage.fromUserId,
                currentMessage.fromUser
              )
            "
          >
            {{ currentMessage.fromUser }}
          </span>
        </div>
        <div class="detail-item">
          <label>消息内容：</label>
          <div class="detail-content">{{ currentMessage.content }}</div>
        </div>
        <div class="detail-item" v-if="currentMessage.targetContent">
          <label>相关内容：</label>
          <div class="detail-target">{{ currentMessage.targetContent }}</div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import request from "@/utils/request";
import { mapMutations } from "vuex";

export default {
  name: "MessageCenter",
  data() {
    return {
      activeTab: "all",
      allMessages: [],
      loading: false,
      currentPage: 1,
      pageSize: 20,
      total: 0,
      selectedMessages: [],
      detailDialogVisible: false,
      currentMessage: {},
      unreadCounts: {
        all: 0,
        system: 0,
        like: 0,
        collect: 0,
        follow: 0,
        comment: 0,
      },
      _pollTimer: null,
    };
  },
  computed: {
    filteredMessages() {
      if (this.activeTab === "all") {
        return this.allMessages;
      }

      const typeMap = {
        system: "系统通知",
        like: "点赞",
        collect: "收藏",
        follow: "关注",
        comment: "评论",
      };

      return this.allMessages.filter(
        (msg) => msg.type === typeMap[this.activeTab]
      );
    },
  },
  created() {
    this.fetchMessages();
  },
  methods: {
    ...mapMutations(["setUnreadMessageCount"]),

    async fetchMessages() {
      this.loading = true;
      try {
        const res = await request.get("/message/list", {
          params: {
            pageNum: this.currentPage,
            pageSize: this.pageSize,
          },
        });

        if (res.code === "200" && res.data) {
          this.allMessages = res.data.list || [];
          this.total = res.data.total || 0;

          this.updateUnreadCounts();
        }
      } catch (error) {
        console.error("获取消息失败:", error);
        this.$message.error("获取消息失败");
      } finally {
        this.loading = false;
      }
    },

    updateUnreadCounts() {
      // 重置所有计数
      Object.keys(this.unreadCounts).forEach((key) => {
        this.unreadCounts[key] = 0;
      });

      // 统计未读消息
      this.allMessages.forEach((msg) => {
        if (!msg.isRead) {
          this.unreadCounts.all++;
          switch (msg.type) {
            case "系统通知":
              this.unreadCounts.system++;
              break;
            case "点赞":
              this.unreadCounts.like++;
              break;
            case "收藏":
              this.unreadCounts.collect++;
              break;
            case "关注":
              this.unreadCounts.follow++;
              break;
            case "评论":
              this.unreadCounts.comment++;
              break;
          }
        }
      });

      // 更新全局未读消息数
      this.setUnreadMessageCount(this.unreadCounts.all);

      // 定期轮询未读消息数
      if (!this._pollTimer) {
        this._pollTimer = setInterval(() => {
          this.fetchUnreadCount();
        }, 30000); // 每30秒轮询一次
      }
    },

    async fetchUnreadCount() {
      try {
        const res = await request.get("/message/unread/count");
        if (res.code === "200") {
          this.setUnreadMessageCount(res.data);
        }
      } catch (error) {
        console.error("获取未读消息数失败:", error);
      }
    },

    // 组件销毁时清理定时器
    beforeDestroy() {
      if (this._pollTimer) {
        clearInterval(this._pollTimer);
        this._pollTimer = null;
      }
    },

    handleTabClick() {
      this.currentPage = 1;
      this.fetchMessages();
    },

    goToUserProfile(userId) {
      if (userId) {
        this.$router.push({
          path: "/front/authorHome",
          query: { authorId: userId },
        });
      }
    },

    formatDate(timestamp) {
      if (!timestamp) return "";
      const date = new Date(timestamp);
      const now = new Date();
      const diff = now - date;

      // 小于1分钟
      if (diff < 60000) {
        return "刚刚";
      }
      // 小于1小时
      if (diff < 3600000) {
        return Math.floor(diff / 60000) + "分钟前";
      }
      // 小于24小时
      if (diff < 86400000) {
        return Math.floor(diff / 3600000) + "小时前";
      }
      // 小于7天
      if (diff < 604800000) {
        return Math.floor(diff / 86400000) + "天前";
      }

      // 超过7天显示完整日期
      return date.toLocaleString();
    },

    handleSelectionChange(val) {
      this.selectedMessages = val;
    },

    async handleBatchDelete() {
      try {
        await this.$confirm("确定要删除选中的消息吗？", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        });

        const ids = this.selectedMessages.map((msg) => msg.id);
        const res = await request.delete("/message/delete", {
          data: { ids },
        });

        if (res.code === "200") {
          this.$message.success("删除成功");
          this.fetchMessages();
        }
      } catch (error) {
        if (error !== "cancel") {
          console.error("批量删除失败:", error);
          this.$message.error("删除失败");
        }
      }
    },

    async handleBatchRead() {
      try {
        const ids = this.selectedMessages.map((msg) => msg.id);
        const res = await request.post("/message/batchRead", { ids });

        if (res.code === "200") {
          this.selectedMessages.forEach((msg) => {
            const message = this.allMessages.find((m) => m.id === msg.id);
            if (message) {
              message.isRead = true;
            }
          });

          this.updateUnreadCounts();
          this.$message.success("标记成功");
        }
      } catch (error) {
        console.error("批量标记已读失败:", error);
        this.$message.error("操作失败");
      }
    },

    viewDetail(message) {
      this.currentMessage = message;
      this.detailDialogVisible = true;
      if (!message.isRead) {
        this.markAsRead(message);
      }
    },

    async deleteMessage(message) {
      try {
        await this.$confirm("确定要删除这条消息吗？", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        });

        const res = await request.delete(`/message/${message.id}`);
        if (res.code === "200") {
          this.$message.success("删除成功");
          this.fetchMessages();
        }
      } catch (error) {
        if (error !== "cancel") {
          this.$message.error("删除失败");
        }
      }
    },

    handleSizeChange(val) {
      this.pageSize = val;
      this.currentPage = 1;
    },

    handleCurrentChange(val) {
      this.currentPage = val;
    },

    getMessageType(type) {
      const types = {
        system: "系统通知",
        like: "点赞",
        collect: "收藏",
        follow: "关注",
        comment: "评论",
      };
      return types[type] || "未知类型";
    },

    async markAsRead(message) {
      try {
        const res = await request.put(`/message/read/${message.id}`);
        if (res.code === "200") {
          message.isRead = true;
          this.updateUnreadCounts();
          this.$message.success("已标记为已读");
        }
      } catch (error) {
        console.error("标记已读失败:", error);
        this.$message.error("操作失败");
      }
    },

    getMessageIcon(type) {
      const icons = {
        系统通知: "el-icon-bell",
        点赞: "el-icon-star-on",
        收藏: "el-icon-collection",
        关注: "el-icon-user",
        评论: "el-icon-chat-dot-round",
      };
      return icons[type] || "el-icon-message";
    },

    getMessageAction(type) {
      const actions = {
        系统通知: "发来通知",
        点赞: "点赞了你的",
        收藏: "收藏了你的",
        关注: "关注了你",
        评论: "评论了你的",
      };
      return actions[type] || "";
    },

    getMessageTypeClass(type) {
      const typeMap = {
        系统通知: "system",
        点赞: "like",
        收藏: "collect",
        关注: "follow",
        评论: "comment",
      };
      return typeMap[type] || "system";
    },

    goToTarget(message) {
      if (!message.targetType || !message.targetId) return;

      switch (message.targetType) {
        case "blog":
          this.$router.push({
            path: "/front/blogDetail",
            query: { blogId: message.targetId },
          });
          break;
        case "activity":
          this.$router.push({
            path: "/front/activityDetail",
            query: { id: message.targetId },
          });
          break;
        default:
          break;
      }
    },
  },
};
</script>

<style lang="less" scoped>
.message-center {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: var(--bg-color);
  min-height: calc(100vh - 60px);
}

.message-header {
  background: var(--bg-color-secondary);
  padding: 20px;
  border-radius: 8px;
  box-shadow: var(--card-shadow);
  margin-bottom: 20px;

  h2 {
    margin: 0;
    font-size: 24px;
    color: var(--text-color-primary);
    display: flex;
    align-items: center;

    &::before {
      content: "";
      width: 4px;
      height: 20px;
      background: var(--primary-color);
      margin-right: 10px;
      border-radius: 2px;
    }
  }
}

.message-list {
  background: var(--bg-color-secondary);
  border-radius: 8px;
  padding: 20px;
  box-shadow: var(--card-shadow);

  .message-item {
    background: var(--bg-color-tertiary);
    border: 1px solid var(--border-color);
    box-shadow: var(--card-shadow);

    &:hover {
      background: var(--bg-color-hover);
    }

    .message-header {
      border-bottom: 1px solid var(--border-color);

      .message-title {
        color: var(--text-color-primary);
      }

      .message-link {
        color: var(--primary-color);
        &:hover {
          text-decoration: underline;
        }
      }

      .message-detail-content {
        color: var(--text-color-regular);
      }
    }

    .message-meta {
      color: var(--text-color-secondary);
    }

    .unread-tag {
      background: var(--danger-color);
      color: #ffffff;
    }

    .interactive-text {
      color: var(--primary-color);

      &:hover {
        color: var(--primary-color-hover);
        background-color: var(--primary-color-light);
      }
    }

    .message-action {
      color: var(--text-color-regular);
    }
  }
}

/deep/ .el-tabs__nav-wrap::after {
  background-color: var(--border-color);
}

/deep/ .el-tabs__item {
  color: var(--text-color-regular);

  &.is-active {
    color: var(--primary-color);
  }
}

.pagination-container {
  margin-top: 20px;
  padding: 20px 0;
  display: flex;
  justify-content: center;
  background: var(--bg-color-secondary);
  border-radius: 8px;
  box-shadow: var(--card-shadow);
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: var(--text-color-secondary);

  i {
    font-size: 24px;
    margin-bottom: 10px;
  }
}

/deep/ .el-dialog__body {
  .message-detail {
    .detail-item {
      margin-bottom: 15px;

      label {
        font-weight: 500;
        color: var(--text-color-regular);
        margin-right: 10px;
      }

      .username {
        color: var(--primary-color);
        &:hover {
          color: var(--primary-color-hover);
          background-color: var(--primary-color-light);
        }
      }

      .detail-content {
        margin-top: 10px;
        padding: 10px;
        background: var(--bg-color-tertiary);
        border-radius: 4px;
        line-height: 1.6;
      }

      .detail-target {
        margin-top: 10px;
        padding: 10px;
        background: var(--bg-color-tertiary);
        border-radius: 4px;
        color: var(--text-color-secondary);
      }
    }
  }
}

.badge {
  margin-left: 5px;
  transform: scale(0.8);
}
</style>
