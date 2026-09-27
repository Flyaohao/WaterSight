<template>
  <div class="activity-page" :class="themeClass">
    <!-- 页面标题区域 -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">海洋活动中心</h1>
        <p class="page-description">探索海洋，保护生态，参与我们的精彩活动</p>
      </div>
      <div class="wave-animation">
        <div class="wave wave1"></div>
        <div class="wave wave2"></div>
        <div class="wave wave3"></div>
      </div>
    </div>

    <!-- 活动筛选区域 -->
    <div class="filter-container">
      <div class="search-area">
        <div class="search-box">
          <i class="el-icon-search"></i>
          <input
            v-model="name"
            placeholder="搜索活动..."
            @keyup.enter="load(1)"
          />
        </div>
        <el-button
          type="primary"
          size="small"
          @click="load(1)"
          class="search-btn"
        >
          搜索
        </el-button>
        <el-button type="info" size="small" @click="reset" class="reset-btn">
          重置
        </el-button>
      </div>

      <div class="filter-tags">
        <span class="filter-label">快速筛选:</span>
        <el-tag
          v-for="tag in filterTags"
          :key="tag.value"
          :type="activeTag === tag.value ? 'primary' : ''"
          @click="filterByTag(tag.value)"
          effect="plain"
          class="filter-tag"
        >
          <i :class="tag.icon"></i> {{ tag.label }}
        </el-tag>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <div class="activity-container">
        <!-- 活动列表组件 -->
        <activity-list :span="6" ref="activityList" />
      </div>

      <!-- 分页控件 -->
      <div class="pagination-container">
        <el-pagination
          background
          layout="prev, pager, next"
          :total="total"
          :current-page.sync="pageNum"
          :page-size="pageSize"
          @current-change="handleCurrentChange"
        ></el-pagination>
      </div>

      <!-- 即将到来的活动提示 -->
      <div
        class="upcoming-activities-bottom"
        v-if="upcomingActivities.length > 0"
        v-show="!isUpcomingCollapsed"
      >
        <div class="upcoming-header">
          <i class="el-icon-time"></i>
          <span>即将开始的活动</span>
          <el-button type="text" class="collapse-btn" @click="toggleUpcoming">
            <i class="el-icon-close"></i>
          </el-button>
        </div>
        <div class="upcoming-list">
          <div
            v-for="(activity, index) in upcomingActivities"
            :key="index"
            class="upcoming-item"
            @click="goDetail(activity.id)"
          >
            <div class="activity-time">{{ formatDate(activity.start) }}</div>
            <div class="activity-info">
              <div class="activity-title">{{ activity.name }}</div>
              <div class="activity-location">
                <i class="el-icon-location"></i> {{ activity.address }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部装饰元素 - 在非暗黑模式下显示 -->
    <div class="fish-container" v-if="!isDarkMode">
      <Fish />
    </div>

    <!-- 添加展开按钮 -->
    <div
      v-if="isUpcomingCollapsed && upcomingActivities.length > 0"
      class="expand-button"
      @click="toggleUpcoming"
    >
      <i class="el-icon-time"></i>
      <span>查看即将开始的活动</span>
    </div>
  </div>
</template>

<script>
// 导入底部组件和活动列表组件
import ActivityList from "@/components/ActivityList";
import request from "@/utils/request";

export default {
  name: "Activity",
  components: {
    ActivityList,
  },
  data() {
    return {
      tableData: [], // 所有的数据
      pageNum: 1, // 当前的页码
      pageSize: 12, // 每页显示的个数
      total: 0, // 总数据数
      name: null, // 搜索活动的名称
      activeTag: "all", // 当前选中的标签
      filterTags: [
        { label: "全部活动", value: "all", icon: "el-icon-menu" },
        { label: "进行中", value: "ongoing", icon: "el-icon-video-play" },
        { label: "即将开始", value: "upcoming", icon: "el-icon-time" },
        { label: "已结束", value: "ended", icon: "el-icon-circle-check" },
      ],
      upcomingActivities: [],
      isUpcomingCollapsed: false, // 添加控制收起状态的变量
      user: JSON.parse(localStorage.getItem("xm-user") || "{}"),
    };
  },
  computed: {
    isResearchMode() {
      return this.user.browseRole === "RESEARCHER";
    },
    isHobbyistMode() {
      return this.user.browseRole === "HOBBYIST";
    },
    isDarkMode() {
      return document.body.classList.contains("dark");
    },
    themeClass() {
      return {
        "research-theme": this.isResearchMode,
        "hobbyist-theme": this.isHobbyistMode,
        "dark-theme": this.isDarkMode,
      };
    },
  },
  created() {
    // 在组件创建时加载第一页数据
    this.load(1);
    this.loadUpcomingActivities();
  },
  methods: {
    // 根据活动ID打开活动详情页面
    goDetail(id) {
      this.$router.push("/front/activityDetail?activityId=" + id);
    },

    // 分页查询活动数据
    load(pageNum) {
      this.pageNum = pageNum;

      // 将搜索条件传递给 ActivityList 组件
      if (this.$refs.activityList) {
        this.$refs.activityList.name = this.name;
        this.$refs.activityList.status =
          this.activeTag !== "all" ? this.activeTag : null;
        this.$refs.activityList.load(1);
      }
    },

    // 重置查询条件并重新加载第一页数据
    reset() {
      this.name = null;
      this.activeTag = "all";

      // 重置 ActivityList 组件的筛选条件
      if (this.$refs.activityList) {
        this.$refs.activityList.name = null;
        this.$refs.activityList.status = null;
        this.$refs.activityList.load(1);
      }
    },

    // 当前页码改变时加载对应页码的数据
    handleCurrentChange(pageNum) {
      this.load(pageNum);
    },

    // 根据标签筛选活动
    filterByTag(tagValue) {
      // console.log("筛选标签:", tagValue);
      this.activeTag = tagValue;

      // 将筛选条件传递给 ActivityList 组件
      if (this.$refs.activityList) {
        this.$refs.activityList.status = tagValue !== "all" ? tagValue : null;
        this.$refs.activityList.load(1);
      }
    },

    // 加载即将开始的活动
    loadUpcomingActivities() {
      // 获取API基础URL
      const apiBaseUrl = process.env.VUE_APP_BASE_API;
      
      // 使用 selectPage 接口获取即将开始的活动
      request
        .get("/activity/selectPage", {
          params: {
            pageNum: 1,
            pageSize: 3,
            status: "upcoming",
          },
          baseURL: apiBaseUrl,  // 使用配置的基础URL
        })
        .then((res) => {
          // console.log("即将开始的活动响应:", res);
          if (res.code === "200") {
            this.upcomingActivities = res.data.list || [];
          }
        })
        .catch((err) => {
          console.error("加载即将开始的活动出错:", err);
          this.upcomingActivities = [];
        });
    },

    // 格式化日期
    formatDate(dateStr) {
      if (!dateStr) return "";

      try {
        // 简单格式化，仅显示月日和时间
        const date = new Date(dateStr);
        const month = date.getMonth() + 1;
        const day = date.getDate();
        const hours = date.getHours().toString().padStart(2, "0");
        const minutes = date.getMinutes().toString().padStart(2, "0");

        return `${month}/${day} ${hours}:${minutes}`;
      } catch (e) {
        console.error("日期格式化错误:", e);
        return dateStr;
      }
    },

    // 切换即将开始活动的显示状态
    toggleUpcoming() {
      this.isUpcomingCollapsed = !this.isUpcomingCollapsed;
    },
  },
};
</script>

<style lang="less" scoped>
/* 科研模式主题变量 */
:root {
  --deep-blue: #003366;
  --tech-silver: #c0c0c0;
  --accent-blue: #0055a4;
  --light-silver: #e8e8e8;
}

.activity-page {
  padding: 0;
  min-height: calc(100vh - 60px);
  position: relative;
  width: 100%;
  overflow: hidden;
  margin-top: -67px;
  background-color: var(--bg-color);

  &.dark-theme {
    .page-title {
      color: var(--text-color-primary);
    }

    .page-description {
      color: var(--text-color-secondary);
    }

    .wave {
      opacity: 0.1;
    }

    .filter-container {
      background: var(--bg-color-secondary);
      border-color: var(--border-color);

      .search-box {
        background: var(--bg-color-tertiary);

        input {
          color: var(--text-color-primary);
          &::placeholder {
            color: var(--text-color-secondary);
          }
        }
      }
    }

    .main-content {
      background: var(--bg-color-secondary);
      border-color: var(--border-color);
    }

    .upcoming-activities-bottom {
      background: var(--bg-color-secondary);
      border-color: var(--border-color);

      .upcoming-header {
        background: var(--primary-gradient);
        color: var(--text-color-primary);
      }

      .upcoming-item {
        border-bottom-color: var(--border-color);

        &:hover {
          background: var(--bg-color-hover);
        }

        .activity-time {
          color: var(--primary-color);
        }

        .activity-title {
          color: var(--text-color-primary);
        }

        .activity-location {
          color: var(--text-color-secondary);
        }
      }
    }
  }

  // 新增的底部活动样式
  .upcoming-activities-bottom {
    margin-top: 30px;
    margin-bottom: 20px;
    background: var(--bg-color-secondary, white);
    border-radius: 12px;
    box-shadow: var(--card-shadow, 0 5px 15px rgba(0, 0, 0, 0.1));
    border: 1px solid var(--border-color, #eee);
    overflow: hidden;
    width: 100%;

    .upcoming-header {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 15px 20px;
      background: linear-gradient(135deg, #0e2028 0%, #005ca9 100%);
      color: white;
      font-weight: 600;
      font-size: 16px;
      position: relative;

      i {
        font-size: 20px;
      }

      .collapse-btn {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        padding: 0;
        color: white;

        i {
          font-size: 16px;
          transition: all 0.3s;
        }

        &:hover {
          i {
            transform: rotate(90deg);
          }
        }
      }
    }

    .upcoming-list {
      max-height: 300px;
      overflow-y: auto;

      &::-webkit-scrollbar {
        width: 5px;
      }

      &::-webkit-scrollbar-track {
        background: #f5f5f5;
      }

      &::-webkit-scrollbar-thumb {
        background: #005ca9;
        border-radius: 3px;
      }
    }

    .upcoming-item {
      display: flex;
      padding: 15px 20px;
      border-bottom: 1px solid rgba(0, 92, 169, 0.1);
      cursor: pointer;
      transition: all 0.3s ease;

      &:hover {
        background: rgba(0, 92, 169, 0.05);
        transform: translateX(5px);
      }

      &:last-child {
        border-bottom: none;
      }

      .activity-time {
        width: 75px;
        color: #005ca9;
        font-weight: 600;
        font-size: 15px;
      }

      .activity-info {
        flex: 1;

        .activity-title {
          font-weight: 500;
          margin-bottom: 8px;
          font-size: 15px;
        }

        .activity-location {
          color: #777;
          font-size: 13px;
          display: flex;
          align-items: center;
          gap: 5px;

          i {
            color: #005ca9;
          }
        }
      }
    }
  }

  /* 暗黑模式下的样式 */
  .dark-theme {
    .upcoming-activities-bottom {
      background-color: var(--bg-color-secondary);
      border-color: var(--border-color);

      .upcoming-header {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        color: var(--text-color-primary);
      }

      .upcoming-item {
        border-bottom-color: var(--border-color);

        &:hover {
          background-color: var(--bg-color-hover);
        }

        .activity-time {
          color: #45cafc;
        }

        .activity-title {
          color: var(--text-color-primary);
        }

        .activity-location {
          color: var(--text-color-secondary);

          i {
            color: #45cafc;
          }
        }
      }

      .upcoming-list {
        &::-webkit-scrollbar-track {
          background: var(--bg-color-tertiary);
        }

        &::-webkit-scrollbar-thumb {
          background: #45cafc;
        }
      }
    }
  }
}

.activity-container {
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
}

.filter-container {
  max-width: 1440px;
  margin: -50px auto 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  background: var(--bg-color-secondary);
  border-radius: 12px;
  box-shadow: var(--card-shadow);
  position: relative;
  z-index: 2;
  box-sizing: border-box;
}

.main-content {
  background: var(--bg-color-secondary);
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 40px;
  box-shadow: var(--card-shadow);
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1440px;
  margin-left: auto;
  margin-right: auto;
  box-sizing: border-box;
}

/* 页面标题区域 */
.page-header {
  transition: background 0.3s ease;
  position: relative;
  height: 200px;
  padding: 30px 0 120px; /* 增加顶部内边距以补偿负边距 */
  text-align: center;
  background: linear-gradient(135deg, #025452 0%, #7ad7ec 100%);
  overflow: hidden;
  margin-top: 65px;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 60px; /* 与导航栏高度相同 */
    background: inherit;
    z-index: 1;
  }

  .header-content {
    position: relative;
    z-index: 2;
    animation: fadeIn 1s ease-out;
  }

  .page-title {
    color: white;
    font-size: 42px;
    font-weight: 700;
    margin: 0 0 15px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .page-description {
    color: rgba(255, 255, 255, 0.9);
    font-size: 18px;
    max-width: 600px;
    margin: 0 auto;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  }

  .wave-animation {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 80px;
    z-index: 1;
  }

  .wave {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 100px;
    background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 120' preserveAspectRatio='none'%3E%3Cpath d='M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z' fill='%23e0f7fa' opacity='.25'%3E%3C/path%3E%3C/svg%3E")
      no-repeat;
    background-size: cover;
    background-position: center;
    z-index: 1;
  }

  .wave1 {
    animation: wave-animation 30s linear infinite;
    z-index: 3;
    opacity: 0.5;
  }

  .wave2 {
    animation: wave-animation 15s linear infinite;
    z-index: 2;
    opacity: 0.3;
  }

  .wave3 {
    animation: wave-animation-reverse 20s linear infinite;
    z-index: 1;
    opacity: 0.2;
  }

  @keyframes wave-animation {
    0% {
      background-position-x: 0;
    }
    100% {
      background-position-x: 1000px;
    }
  }

  @keyframes wave-animation-reverse {
    0% {
      background-position-x: 1000px;
    }
    100% {
      background-position-x: 0;
    }
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(-20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
}

/* 筛选区域样式 */
.filter-container {
  .search-area {
    display: flex;
    align-items: center;
    gap: 12px;

    .search-box {
      display: flex;
      align-items: center;
      background: var(--bg-color-tertiary);
      border-radius: 50px;
      padding: 8px 16px;
      width: 300px;
      transition: all 0.3s ease;

      i {
        color: var(--text-color-secondary);
        margin-right: 8px;
      }

      input {
        border: none;
        background: transparent;
        outline: none;
        width: 100%;
        color: var(--text-color-primary);

        &::placeholder {
          color: var(--text-color-secondary);
        }
      }

      &:hover,
      &:focus-within {
        background: var(--bg-color-hover);
        box-shadow: var(--hover-shadow);
      }
    }

    .search-btn {
      background: #005ca9;
      border-color: #005ca9;
      color: white;
      font-weight: 500;
      height: 36px;
      padding: 0 20px;
      border-radius: 50px;
      border: none;
      box-shadow: 0 4px 10px rgba(0, 92, 169, 0.3);
      transition: all 0.3s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      line-height: 1;

      &:hover {
        background: #004c8c;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 92, 169, 0.4);
      }
    }

    .reset-btn {
      background: #f5f5f5;
      height: 36px;
      border-color: transparent;
      color: #666;
      padding: 0 20px;
      border-radius: 50px;
      border: none;
      transition: all 0.3s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      line-height: 1;

      &:hover {
        background: #eee;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.05);
      }
    }
  }

  .filter-tags {
    display: flex;
    align-items: center;
    gap: 10px;

    .filter-label {
      color: #666;
      font-size: 15px;
      font-weight: 500;
    }

    .filter-tag {
      cursor: pointer;
      background: #f5f5f5;
      border: none;
      color: #666;
      padding: 8px 16px;
      border-radius: 50px;
      font-size: 14px;
      transition: all 0.3s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      line-height: 1;

      i {
        margin-right: 6px;
        font-size: 16px;
      }

      &:hover {
        background: #eee;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.05);
      }

      &.el-tag--primary {
        background: #005ca9;
        color: white;
        box-shadow: 0 4px 10px rgba(0, 92, 169, 0.3);
      }
    }
  }
}

/* 添加展开按钮样式 */
.expand-button {
  position: fixed;
  right: 25px;
  bottom: 25px;
  background: var(--primary-gradient);
  color: var(--white);
  padding: 12px 20px;
  border-radius: 50px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: var(--card-shadow);
  transition: all 0.3s ease;
  z-index: 100;

  i {
    font-size: 18px;
  }

  span {
    font-size: 14px;
    font-weight: 500;
  }

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 92, 169, 0.4);
  }
}

/* 鱼群容器 */
.fish-container {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  z-index: 50;
  pointer-events: none;
}

/* 响应式调整 */
@media (max-width: 1440px) {
  .activity-container,
  .filter-container,
  .main-content {
    max-width: 100%;
    padding: 20px 15px;
  }
}

@media (max-width: 992px) {
  .activity-container {
    padding: 15px;
  }

  .filter-container {
    margin-top: -30px;
    padding: 15px;
    flex-direction: column;
    gap: 15px;
  }

  .main-content {
    padding: 20px 15px;
  }
}

@media (max-width: 768px) {
  .activity-container {
    padding: 10px;
  }

  .filter-container {
    margin-top: -20px;
    padding: 10px;
  }

  .main-content {
    padding: 15px 10px;
  }

  .search-area {
    width: 100%;

    .search-box {
      width: 100%;
    }
  }
}

/* 业余爱好者模式主题 */
.hobbyist-theme {
  background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);

  .page-header {
    height: 300px;
    background: transparent;
    padding-top: 80px; /* 增加顶部内边距，避免被导航栏覆盖 */
    margin-top: 0; /* 移除负边距 */

    .page-title {
      font-size: 48px;
      text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }

    .wave-animation {
      opacity: 0.8;
    }
  }

  .filter-container {
    backdrop-filter: blur(10px);
    background: rgba(255, 255, 255, 0.9);
    border: none;
  }

  .main-content {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
  }

  .activity-card {
    transform: scale(1);
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);

    &:hover {
      transform: scale(1.05);
      z-index: 1;
    }
  }
}
</style>
