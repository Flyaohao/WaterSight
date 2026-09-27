<template>
  <transition name="page">
    <div class="search-page">
      <!-- 返回首页按钮 -->
      <div class="back-home-button" @click="goBackHome">
        <i class="el-icon-back"></i>
        <span>返回首页</span>
      </div>

      <!-- 改进的搜索框 -->
      <div class="search-container">
        <div class="search-box">
          <i class="el-icon-search search-icon"></i>
          <input
            v-model="searchTitle"
            class="search-input"
            :placeholder="
              searchType === 'blog' ? '搜索博客标题...' : '搜索用户名...'
            "
            @input="handleRealTimeSearch"
            @keyup.enter="handleSearch"
          />
          <div class="search-type-selector">
            <div
              v-for="tab in tabs"
              :key="tab.value"
              class="type-item"
              :class="{ active: searchType === tab.value }"
              @click="changeSearchType(tab.value)"
            >
              <i :class="tab.icon"></i>
              <span>{{ tab.label }}</span>
            </div>
          </div>
          <el-button
            type="primary"
            class="search-button"
            @click="handleSearch"
            :loading="loading"
          >
            搜索
          </el-button>
        </div>
      </div>

      <!-- 搜索结果 -->
      <div class="search-results">
        <div v-if="searchTitle" class="search-info">
          <span>搜索 "{{ searchTitle }}" 的结果</span>
          <span v-if="total > 0" class="result-count"
            >找到 {{ total }} 条结果</span
          >
        </div>

        <!-- 博客搜索结果 -->
        <blog-list
          v-if="searchType === 'blog'"
          :searchTitle="searchTitle"
          categoryName="全部博客"
          @height-change="handleHeightChange"
          ref="blogList"
        />

        <!-- 用户搜索结果 -->
        <div v-if="searchType === 'user'" class="user-list">
          <div v-if="loading" class="loading-container">
            <el-skeleton :rows="5" animated />
          </div>
          <div v-else-if="users.length === 0" class="no-results">
            <i class="el-icon-warning-outline"></i>
            <p>未找到相关用户</p>
          </div>
          <div v-else class="users-container">
            <div v-for="user in users" :key="user.id" class="user-card">
              <div class="user-avatar" @click="goToUserProfile(user.id)">
                <img
                  :src="user.avatar || require('@/assets/imgs/bgc2.jpg')"
                  @error="handleAvatarError($event)"
                  alt="用户头像"
                />
              </div>
              <div class="user-info">
                <div class="user-name" @click="goToUserProfile(user.id)">
                  {{ user.name }}
                </div>
                <div class="user-bio">
                  {{ user.info || "这个人很懒，什么都没留下" }}
                </div>
                <div class="user-stats">
                  <span
                    ><i class="el-icon-document"></i>
                    {{ user.blogCount || 0 }} 博客</span
                  >
                  <span
                    ><i class="el-icon-star-on"></i>
                    {{ user.likesCount || 0 }} 获赞</span
                  >
                  <span
                    ><i class="el-icon-user"></i>
                    {{ user.fansCount || 0 }} 粉丝</span
                  >
                </div>
              </div>
              <div class="user-actions">
                <el-button
                  v-if="currentUser.id !== user.id"
                  size="small"
                  type="primary"
                  :loading="user.followLoading"
                  @click="toggleFollow(user)"
                  :class="{ 'is-following': user.isFollowing }"
                >
                  {{ user.isFollowing ? "已关注" : "关注" }}
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import BlogList from "@/components/BlogList";
import request from "@/utils/request";
import { formatDate } from "@/utils/date";

export default {
  name: "Search",
  components: {
    BlogList,
  },
  data() {
    return {
      searchTitle: this.$route.query.title || "",
      searchType: this.$route.query.type || "blog",
      loading: false,
      total: 0,
      tabs: [
        { label: "博客", value: "blog", icon: "el-icon-document" },
        { label: "用户", value: "user", icon: "el-icon-user" },
      ],
      users: [],
      currentUser: JSON.parse(localStorage.getItem("xm-user") || "{}"),
      searchTimeout: null, // 添加防抖延时器
    };
  },
  watch: {
    // 监听路由变化
    $route(to, from) {
      if (to.path !== from.path && to.path === "/front/home") {
        // 当路由切换到首页时，触发博客列表刷新
        this.$bus.$emit("refreshBlogList");
      }
    },
  },
  created() {
    // 初始加载
    if (this.searchTitle && this.searchType === "user") {
      this.handleSearch();
    }
  },
  methods: {
    formatDate,
    handleSearch() {
      // 只在点击搜索按钮且输入为空时显示提示
      if (!this.searchTitle.trim() && event && event.type === "click") {
        this.$message.warning("请输入搜索内容");
        return;
      }

      this.loading = true;

      // 更新路由参数
      this.$router.push({
        path: "/front/search",
        query: {
          title: this.searchTitle,
          type: this.searchType,
          _t: Date.now(),
        },
      });

      if (this.searchType === "user") {
        this.checkUserExists();
      } else {
        if (this.$refs.blogList) {
          this.$refs.blogList.reset();
          this.$refs.blogList.load();
        }
        setTimeout(() => {
          this.loading = false;
        }, 500);
      }
    },

    // 检查用户是否存在
    checkUserExists() {
      request
        .get("/user/search", {
          params: {
            keyword: this.searchTitle,
          },
        })
        .then((res) => {
          if (res.code === "200") {
            this.users = (res.data || []).map((user) => ({
              ...user,
              followLoading: false,
              isFollowing: false,
            }));
            this.total = this.users.length;

            // 检查关注状态
            if (this.currentUser.token) {
              this.checkFollowStatus();
            }
          } else {
            this.$message.error(res.msg || "搜索失败");
          }
        })
        .catch((err) => {
          console.error("检查用户失败", err);
          this.$message.error("搜索失败，请稍后重试");
        })
        .finally(() => {
          this.loading = false;
        });
    },

    // 检查关注状态
    async checkFollowStatus() {
      for (const user of this.users) {
        if (user.id === this.currentUser.id) continue;

        try {
          const res = await request.get("/follow/checkStatus", {
            params: {
              followerId: this.currentUser.id,
              followedId: user.id,
            },
          });
          if (res.code === "200") {
            this.$set(user, "isFollowing", res.data);
          }
        } catch (error) {
          console.error("获取关注状态失败", error);
        }
      }
    },

    // 切换关注状态
    async toggleFollow(user) {
      if (!this.currentUser.token) {
        this.$message.warning("请先登录");
        return;
      }

      this.$set(user, "followLoading", true);
      try {
        const action = user.isFollowing ? "unfollow" : "follow";
        const res = await request.post(`/follow/${action}`, {
          followerId: this.currentUser.id,
          followedId: user.id,
        });

        if (res.code === "200") {
          this.$set(user, "isFollowing", !user.isFollowing);
          this.$message.success(user.isFollowing ? "关注成功" : "已取消关注");
        }
      } catch (error) {
        console.error("操作关注失败", error);
        this.$message.error("操作失败，请稍后重试");
      } finally {
        this.$set(user, "followLoading", false);
      }
    },

    // 跳转到用户主页
    goToUserProfile(userId) {
      this.$router.push({
        path: "/front/authorHome",
        query: { authorId: userId },
      });
    },

    // 处理头像加载失败
    handleAvatarError(e) {
      e.target.src = require("@/assets/imgs/bgc2.jpg");
    },

    // 返回首页
    goBackHome() {
      // 添加过渡动画
      this.loading = true;
      setTimeout(() => {
        this.$router.push("/front/home");
      }, 300);
    },

    // 处理搜索结果容器高度变化
    handleHeightChange(height) {
      // 可以根据需要处理高度变化
    },

    // 切换搜索类型
    changeSearchType(type) {
      this.searchType = type;
      if (this.searchTitle) {
        this.handleSearch();
      }
    },

    // 添加实时搜索处理函数
    handleRealTimeSearch() {
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout);
      }

      this.searchTimeout = setTimeout(() => {
        if (this.searchType === "blog") {
          this.$router.push({
            path: "/front/search",
            query: {
              title: this.searchTitle,
              type: this.searchType,
              _t: Date.now(),
            },
          });

          if (this.$refs.blogList) {
            this.$refs.blogList.reset();
            this.$refs.blogList.load();
          }
        } else {
          this.handleSearch();
        }
      }, 300);
    },
  },
  beforeRouteLeave(to, from, next) {
    // 路由离开时的过渡动画
    this.loading = true;
    setTimeout(() => {
      next();
    }, 300);
  },
};
</script>

<style lang="less" scoped>
// 添加页面过渡动画
.page-enter-active,
.page-leave-active {
  transition: all 0.3s ease;
}

.page-enter,
.page-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.search-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: var(--bg-color);
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.back-home-button {
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  margin-bottom: 20px;
  color: var(--primary-color);

  &:hover {
    color: var(--primary-color-hover);
  }

  i {
    margin-right: 5px;
  }
}

.search-container {
  margin-bottom: 30px;

  .search-box {
    display: flex;
    align-items: center;
    background-color: var(--bg-color-secondary);
    border-radius: 8px;
    box-shadow: 0 2px 12px var(--shadow-color);
    padding: 10px 20px;

    .search-icon {
      color: var(--text-color-secondary);
      font-size: 20px;
      margin-right: 10px;
    }

    .search-input {
      flex: 1;
      border: none;
      outline: none;
      font-size: 16px;
      padding: 10px 0;
      background-color: transparent;
      color: var(--text-color-primary);

      &::placeholder {
        color: var(--text-color-placeholder);
      }
    }

    .search-type-selector {
      display: flex;
      margin: 0 15px;

      .type-item {
        padding: 5px 15px;
        cursor: pointer;
        border-radius: 4px;
        display: flex;
        align-items: center;
        margin-right: 10px;
        color: var(--text-color-regular);

        i {
          margin-right: 5px;
        }

        &.active {
          background-color: var(--primary-color-light);
          color: var(--primary-color);
        }

        &:hover {
          background-color: var(--bg-color-hover);
        }
      }
    }

    .search-button {
      min-width: 80px;
    }
  }
}

.search-results {
  .search-info {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
    font-size: 16px;
    color: var(--text-color-primary);

    .result-count {
      color: var(--text-color-secondary);
    }
  }
}

.user-list {
  .loading-container {
    padding: 20px;
    background-color: var(--bg-color-secondary);
    border-radius: 8px;
  }

  .no-results {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 50px 0;
    color: var(--text-color-secondary);

    i {
      font-size: 48px;
      margin-bottom: 10px;
    }

    p {
      font-size: 16px;
    }
  }
}

.users-container {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

.user-card {
  background: var(--bg-color-secondary);
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 2px 12px var(--shadow-color);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px var(--shadow-color-hover);
  }
}

.user-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color-primary);
  margin-bottom: 5px;
  cursor: pointer;
  transition: color 0.3s;

  &:hover {
    color: var(--primary-color);
  }
}

.user-bio {
  font-size: 13px;
  color: var(--text-color-regular);
  margin-bottom: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-stats {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: var(--text-color-secondary);

  span {
    display: flex;
    align-items: center;
    gap: 4px;
  }

  i {
    font-size: 14px;
  }
}

.user-actions {
  .el-button {
    &.is-following {
      background-color: var(--bg-color-tertiary);
      border-color: var(--border-color);
      color: var(--text-color-secondary);

      &:hover {
        background-color: var(--danger-color-light);
        border-color: var(--danger-color);
        color: var(--danger-color);
      }
    }
  }
}
</style>
