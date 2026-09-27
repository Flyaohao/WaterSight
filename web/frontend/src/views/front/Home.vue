<template>
  <div class="front-home">
    <!-- 添加公告栏 -->
    <div class="announcement-bar">
      <div class="d-flex align-items-center">
        <i class="el-icon-bell"></i>
        <div class="notice-carousel">
          <transition name="notice-fade">
            <div class="notice-content" :key="activeNoticeIndex">
              <span class="fw-bold">管理员公告：</span>
              {{ activeNotice }}
            </div>
          </transition>
        </div>
        <div class="notice-controls">
          <el-button
            type="text"
            icon="el-icon-arrow-left"
            @click="prevNotice"
            :disabled="notice.length <= 1"
            class="notice-btn"
          ></el-button>
          <span class="notice-counter"
            >{{ activeNoticeIndex + 1 }}/{{ notice.length }}</span
          >
          <el-button
            type="text"
            icon="el-icon-arrow-right"
            @click="nextNotice"
            :disabled="notice.length <= 1"
            class="notice-btn"
          ></el-button>
        </div>
      </div>
    </div>

    <div class="container py-3">
      <div class="row">
        <!-- 左侧博客列表和搜索区域 -->
        <div class="col-lg-8">
          <!-- 搜索和过滤区域 -->
          <div class="card border-0 shadow-sm mb-3 overflow-hidden">
            <div class="card-body p-0">
              <div class="p-3 pb-2">
                <div class="input-group">
                  <span class="input-group-text bg-white border-end-0">
                    <i class="el-icon-search"></i>
                  </span>
                  <el-input
                    v-model="searchKeyword"
                    placeholder="搜索博客或用户..."
                    class="custom-input"
                    @keyup.enter.native="goToSearch"
                  ></el-input>
                  <el-button
                    class="search-btn"
                    type="primary"
                    @click="goToSearch"
                    >搜索</el-button
                  >
                </div>
              </div>

              <!-- 分类标签 -->
              <div class="px-3 pb-2 d-flex flex-wrap gap-2 category-tags">
                <el-button
                  v-for="item in filteredCategoryList"
                  :key="item.id"
                  :class="{ active: current === item.name }"
                  @click="handleCategorySelect(item)"
                  class="category-tag"
                  size="small"
                  round
                >
                  {{ item.name }}
                </el-button>
              </div>
            </div>
          </div>

          <!-- 博客列表 -->
          <blog-list
            :categoryName="current"
            ref="blogListRef"
            class="blog-list-container"
            @click-blog="handleBlogClick"
          />
        </div>

        <!-- 右侧功能侧边栏 -->
        <div class="col-lg-4">
          <!-- 实时热榜 -->
          <div class="card border-0 shadow-sm mb-3">
            <div class="card-header bg-transparent border-bottom-0 py-2">
              <div class="d-flex align-items-center">
                <i class="el-icon-data-analysis text-danger me-2"></i>
                <h5 class="card-title mb-0 trending-title">实时热榜</h5>
                <div class="ms-auto">
                  <span class="badge bg-danger">HOT</span>
                </div>
              </div>
            </div>
            <div class="card-body pt-0 pb-2">
              <div v-if="topBlogsLoading" class="text-center py-3">
                <i class="el-icon-loading"></i> 加载中...
              </div>
              <ul v-else class="list-group list-group-flush">
                <li
                  v-for="(item, index) in topBlogs"
                  :key="item.id"
                  class="list-group-item border-0 px-0 py-1"
                >
                  <div class="d-flex">
                    <div class="text-primary fw-bold me-2">{{ index + 1 }}</div>
                    <div
                      class="text-truncate hot-blog-title"
                      @click="handleBlogClick(item)"
                      style="cursor: pointer"
                    >
                      {{ item.title }}
                    </div>
                    <span v-if="index < 2" class="ms-2 badge bg-danger"
                      >热</span
                    >
                  </div>
                </li>
                <li
                  v-if="topBlogs.length === 0 && !topBlogsLoading"
                  class="list-group-item border-0 px-0 py-3 text-center text-muted"
                >
                  暂无热门博客
                </li>
              </ul>
            </div>
          </div>

          <!-- 近期活动 -->
          <div class="card border-0 shadow-sm mb-3" v-if="!isResearchMode">
            <div class="card-header bg-transparent border-bottom-0 py-2">
              <div class="d-flex align-items-center">
                <i class="el-icon-date text-success me-2"></i>
                <h5 class="card-title mb-0">近期活动</h5>
              </div>
            </div>
            <div class="card-body pt-0 pb-2">
              <div
                class="position-relative mb-2"
                v-if="latestActivity && latestActivity.id"
              >
                <img
                  :src="
                    latestActivity.cover || require('@/assets/imgs/bgc2.jpg')
                  "
                  class="rounded w-100"
                  style="height: 120px; object-fit: cover"
                  @error="handleImageError"
                />
                <div
                  class="position-absolute bottom-0 start-0 w-100 p-2"
                  style="
                    background: linear-gradient(
                      to top,
                      rgba(0, 0, 0, 0.7),
                      transparent
                    );
                  "
                ></div>
              </div>
              <div class="activity-info mt-3">
                <h6 class="text-white mb-0">
                  {{
                    latestActivity.title ||
                    latestActivity.name ||
                    "水下摄影大赛"
                  }}
                </h6>
                <div class="activity-date d-flex align-items-center">
                  <i class="el-icon-time me-2"></i>
                  <span class="text-primary">{{
                    formatActivityDate(latestActivity)
                  }}</span>
                </div>
              </div>
              <div class="d-grid">
                <el-button
                  type="success"
                  size="small"
                  @click="handleActivityClick(latestActivity)"
                  :disabled="!latestActivity || !latestActivity.id"
                >
                  {{
                    latestActivity && latestActivity.id
                      ? "立即报名"
                      : "暂无活动"
                  }}
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加登录对话框组件 -->
    <login-dialog ref="loginDialog" />
  </div>
</template>
<script>
import Footer from "@/components/Footer";
import BlogList from "@/components/BlogList";
import LoginDialog from "@/components/LoginDialog";
import request from "@/utils/request";

export default {
  name: "FrontHome",
  components: {
    BlogList,
    Footer,
    LoginDialog,
  },
  data() {
    return {
      current: "全部博客",
      categoryList: [],
      filteredCategoryList: [],
      topBlogs: [],
      hotBlogs: [],
      latestActivity: null,
      isLogin: false,
      sortType: "time",
      defaultCover: require("@/assets/imgs/bgc2.jpg"),
      hotTags: [],
      tagTypes: ["", "success", "warning", "danger", "info"],
      searchKeyword: "",
      trendingTags: [
        { name: "深海探索", size: 18, color: "#4ecdc4" },
        { name: "海洋生物", size: 16, color: "#6b8dd6" },
        { name: "科研发现", size: 20, color: "#9d7cbf" },
        { name: "水下摄影", size: 14, color: "#ff6b6b" },
        { name: "海洋保护", size: 17, color: "#ffd93d" },
        { name: "潜水技术", size: 15, color: "#4ecdc4" },
        { name: "海底地质", size: 16, color: "#6b8dd6" },
        { name: "海洋科技", size: 19, color: "#9d7cbf" },
        { name: "珊瑚礁", size: 15, color: "#ff6b6b" },
        { name: "海洋考古", size: 17, color: "#ffd93d" },
      ],
      totalBlogs: 100, // 示例总数
      pageSize: 12,
      currentPage: 1,
      topBlogsLoading: false,
      hotBlogsLoading: false,
      announcementText: [
        "欢迎使用WaterSight水下论坛，分享您的海洋探索经历！",
        "新功能上线：专业工具区提供珊瑚礁识别模型，基于YOLOv5深度学习框架，支持水下图像目标检测",
        "深度学习工具现已支持数据集预处理、模型训练和在线推理，助力水下科研工作",
        "专业区新增水下图像增强功能，改善水下拍摄的清晰度和色彩还原",
      ],
      activeNoticeIndex: 0,
      activeNotice: "",
      notice: [],
      customNotices: [
        "欢迎来到WaterSight水下论坛，一起探索，分享，成长！新版溶水点标记功能已上线，欢迎体验。",
        "新功能上线：专业工具区提供珊瑚礁识别模型，基于YOLOv5深度学习框架，支持水下图像目标检测",
        "深度学习工具现已支持数据集预处理、模型训练和在线推理，助力水下科研工作",
        "专业区新增水下图像增强功能，改善水下拍摄的清晰度和色彩还原",
      ],
    };
  },
  watch: {
    sortType(newVal) {
      if (this.$refs.blogListRef) {
        this.$refs.blogListRef.refreshList(this.current, newVal);
      }
    },
    userRole: {
      handler(newRole) {
        this.loadCategories();
      },
      immediate: true,
    },
  },
  created() {
    this.load();
    this.checkLoginStatus();
    this.loadHotTags();
    this.loadLatestActivity();
    this.loadNotice();
  },
  methods: {
    checkLoginStatus() {
      const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
      this.isLogin = !!user.role;
    },
    handleBlogClick(blog) {
      // 更新阅读量
      request
        .put(`/blog/updateReadCount/${blog.id}`)
        .then(() => {
          // 跳转到博客详情页
          this.$router.push(`/front/blogDetail?blogId=${blog.id}`);
        })
        .catch((error) => {
          console.error("更新阅读量失败", error);
          // 即使更新阅读量失败，也跳转到博客详情页
          this.$router.push(`/front/blogDetail?blogId=${blog.id}`);
        });
    },
    handleActivityClick(activity) {
      if (!activity || !activity.id) return;

      // 修改为正确的活动详情页路由格式
      this.$router.push({
        path: `/front/activityDetail`,
        query: { activityId: activity.id },
      });
    },
    load() {
      this.loadCategories();
      this.loadTopBlogs();
    },
    loadCategories() {
      const researcherCategories = [
        { name: "水下图像", role: "RESEARCHER" },
        { name: "水下机器人", role: "RESEARCHER" },
        { name: "海洋环境监测", role: "RESEARCHER" },
        { name: "水下通信与传感", role: "RESEARCHER" },
        { name: "深海生物学", role: "RESEARCHER" },
        { name: "海洋能源开发", role: "RESEARCHER" },
        { name: "水下考古与地质勘探", role: "RESEARCHER" },
      ];

      const hobbyistCategories = [
        { name: "摄影", role: "HOBBYIST" },
        { name: "潜水", role: "HOBBYIST" },
        { name: "游泳", role: "HOBBYIST" },
        { name: "水产养殖", role: "HOBBYIST" },
        { name: "美食", role: "HOBBYIST" },
      ];

      // 获取用户角色
      const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
      const userRole = user.browseRole || "";

      // 根据用户角色过滤分类
      if (userRole === "RESEARCHER") {
        this.filteredCategoryList = researcherCategories;
      } else if (userRole === "HOBBYIST" || userRole === "ALL") {
        this.filteredCategoryList = hobbyistCategories;
      } else {
        // 未登录用户显示所有分类
        this.filteredCategoryList = [
          ...researcherCategories,
          ...hobbyistCategories,
        ];
      }

      // 在分类列表开头添加"全部博客"选项
      this.filteredCategoryList.unshift({ name: "全部博客" });
    },

    loadTopBlogs() {
      console.log("开始加载热门博客");
      this.topBlogsLoading = true;

      // 直接获取所有博客，然后在前端排序
      request
        .get("/blog/selectPage", {
          params: {
            pageNum: 1,
            pageSize: 10,
          },
        })
        .then((res) => {
          console.log("热门博客响应:", res);
          this.topBlogsLoading = false;

          if (res.code === "200" && res.data) {
            let blogs = [];

            // 尝试从不同的数据结构中提取博客列表
            if (res.data.records && Array.isArray(res.data.records)) {
              blogs = res.data.records;
            } else if (Array.isArray(res.data)) {
              blogs = res.data;
            } else if (res.data.list && Array.isArray(res.data.list)) {
              blogs = res.data.list;
            }

            // 如果成功获取到博客列表
            if (blogs.length > 0) {
              // 在前端按阅读量排序
              blogs.sort((a, b) => (b.readCount || 0) - (a.readCount || 0));
              // 只取前5条
              this.topBlogs = blogs.slice(0, 5);
              console.log("加载热门博客成功:", this.topBlogs);
            } else {
              console.warn("未找到博客数据");
              this.topBlogs = [];
            }
          } else {
            console.warn("热门博客数据格式不正确:", res);
            this.topBlogs = [];
          }
        })
        .catch((error) => {
          console.error("加载热门博客失败:", error);
          this.topBlogsLoading = false;
          this.topBlogs = [];
        });
    },
    viewMoreHotBlogs() {
      // 设置排序方式为热门并刷新列表
      this.sortType = "fav";
      if (this.$refs.blogListRef) {
        this.$refs.blogListRef.refreshList(this.current, this.sortType);
      }
    },
    handleImageError(e) {
      e.target.src = this.defaultCover;
    },
    getRankMedal(index) {
      const medals = {
        1: "🥇",
        2: "🥈",
        3: "🥉",
      };
      return medals[index] || index;
    },
    handleCategorySelect(item) {
      console.log("选择分类:", item);

      // 如果是对象，获取name属性
      if (typeof item === "object" && item.name) {
        this.current = item.name;
      } else {
        this.current = item;
      }

      console.log("当前选中分类:", this.current);

      // 刷新博客列表
      this.$nextTick(() => {
        this.refreshBlogList();
      });
    },
    handleSort(type) {
      this.sortType = type;
    },
    refreshBlogList() {
      if (this.$refs.blogListRef) {
        console.log("刷新博客列表, 当前分类:", this.current);
        this.$refs.blogListRef.categoryName = this.current;
        this.$refs.blogListRef.refreshList();
      }
    },
    handleTagClick(tag) {
      this.current = typeof tag === "object" ? tag.name : tag;
    },
    goToSearch() {
      if (this.searchKeyword.trim()) {
        this.$router.push({
          path: "/front/search",
          query: {
            title: this.searchKeyword,
            type: "blog",
          },
        });
      }
    },
    searchByTag(tag) {
      this.searchKeyword = tag;
      this.goToSearch();
    },
    handlePageChange(page) {
      this.currentPage = page;
      // 这里添加分页加载逻辑
      if (this.$refs.blogListRef) {
        this.$refs.blogListRef.loadData(page);
      }
    },
    loadHotTags() {
      request
        .get("/tag/getHotTags?limit=5")
        .then((res) => {
          if (res.code === "200" && Array.isArray(res.data)) {
            this.hotTags = res.data.map((tag) => ({
              name: tag.name || "未知分类",
              count: tag.blogCount || 0,
            }));
          }
        })
        .catch((error) => {
          console.error("获取热门标签出错:", error);
          // 设置默认标签
          this.hotTags = [
            { name: "水下摄影", count: 0 },
            { name: "海洋生态", count: 0 },
            { name: "潜水装备", count: 0 },
            { name: "珊瑚保护", count: 0 },
            { name: "海洋科技", count: 0 },
          ];
        });
    },
    formatActivityDate(activity) {
      if (!activity) return "";

      if (activity.endTime) {
        return this.formatDate(activity.endTime) + " 截止";
      } else if (activity.end) {
        return activity.end;
      } else {
        return "时间待定";
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return "";

      const date = new Date(dateStr);
      if (isNaN(date.getTime())) return dateStr;

      const month = date.getMonth() + 1;
      const day = date.getDate();

      return `${month}月${day}日`;
    },
    loadLatestActivity() {
      // 首先尝试使用与 ActivityDetail.vue 相同的 API 格式
      this.$request
        .get("/activity/selectAll", {
          params: {
            pageNum: 1,
            pageSize: 1,
          },
        })
        .then((res) => {
          console.log("活动列表响应:", res);

          if (
            res &&
            res.code === "200" &&
            res.data &&
            Array.isArray(res.data) &&
            res.data.length > 0
          ) {
            this.latestActivity = res.data[0];
            console.log("加载最新活动成功:", this.latestActivity);
          } else if (
            res &&
            res.code === "200" &&
            res.data &&
            res.data.records &&
            res.data.records.length > 0
          ) {
            // 备选格式：如果返回的是分页格式
            this.latestActivity = res.data.records[0];
            console.log("加载最新活动成功(分页格式):", this.latestActivity);
          } else {
            console.log("没有找到活动");
            this.latestActivity = null;
          }
        })
        .catch((error) => {
          console.error("加载最新活动失败:", error);

          // 如果第一个 API 失败，尝试另一个可能的 API
          this.$request
            .get("/activity/selectPage", {
              params: {
                pageNum: 1,
                pageSize: 1,
              },
            })
            .then((res) => {
              console.log("备选 API 活动列表响应:", res);

              if (
                res &&
                res.code === "200" &&
                res.data &&
                res.data.records &&
                res.data.records.length > 0
              ) {
                this.latestActivity = res.data.records[0];
                console.log("备选 API 加载最新活动成功:", this.latestActivity);
              } else {
                console.log("备选 API 没有找到活动");
                this.latestActivity = null;
              }
            })
            .catch((err) => {
              console.error("备选 API 加载最新活动失败:", err);
              this.latestActivity = null;
            });
        });
    },
    loadNotice() {
      this.$request.get("/notice/selectAll").then((res) => {
        this.notice = [...this.customNotices, ...(res.data || [])];
        if (this.notice && this.notice.length) {
          this.startNoticeCarousel();
        }
      });
    },
    startNoticeCarousel() {
      // 初始化第一条公告
      const firstNotice = this.notice[0];
      this.activeNotice = firstNotice.content || firstNotice;

      // 设置轮播间隔
      setInterval(() => {
        this.nextNotice();
      }, 6000); // 6秒切换一次
    },
    prevNotice() {
      if (this.notice.length <= 1) return;

      this.activeNoticeIndex =
        this.activeNoticeIndex <= 0
          ? this.notice.length - 1
          : this.activeNoticeIndex - 1;

      const currentNotice = this.notice[this.activeNoticeIndex];
      this.activeNotice = currentNotice.content || currentNotice;
    },
    nextNotice() {
      if (this.notice.length <= 1) return;

      this.activeNoticeIndex =
        (this.activeNoticeIndex + 1) % this.notice.length;
      const currentNotice = this.notice[this.activeNoticeIndex];
      this.activeNotice = currentNotice.content || currentNotice;
    },
    toggleToolsMenu() {
      this.isToolsMenuCollapsed = !this.isToolsMenuCollapsed;
    },
    navigateToFeature(feature) {
      const routes = {
        enhance: "/profession/enhance",
        detect: "/profession/datasetPreprocessing",
        fish: "/profession/fishyolo",
        coral: "/profession/coralyolo",
      };

      if (routes[feature]) {
        this.$router.push(routes[feature]);
      }
    },
    userRole() {
      try {
        const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
        return user.browseRole || "";
      } catch (error) {
        return "";
      }
    },
  },
  computed: {
    filteredActivityList() {
      return this.topBlogs.filter((item) => item != null);
    },
    topThreeActivities() {
      return this.filteredActivityList.slice(0, 3);
    },
    isValidUser() {
      return this.isLogin;
    },
    isResearchMode() {
      const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
      return user.browseRole === "RESEARCHER";
    },
  },
};
</script>

<style lang="less" scoped>
/* 全局字体设置 */
.front-home {
  font-family: "Segoe UI", "Noto Sans SC", system-ui, -apple-system !important;
  margin-top: -18px;
  min-height: 100vh;
  background-color: var(--primary-bg);
  transition: background-color 0.3s ease;
}

/* 确保所有子元素继承字体 */
.front-home * {
  font-family: inherit;
}

/* 搜索框样式 */
.input-group {
  .input-group-text {
    font-size: 1rem !important;
  }

  .custom-input /deep/ input {
    font-size: 0.95rem !important;
    height: 40px !important;
  }

  .search-btn {
    font-size: 0.95rem !important;
    height: 40px !important;
    padding: 0 20px !important;
  }
}

/* 分类标签气泡上升效果 */
@keyframes bubble {
  0% {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
  50% {
    transform: translateY(-10px) scale(1.05);
    opacity: 0.9;
  }
  100% {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}

@keyframes rise {
  0% {
    transform: translateY(0) translateX(-50%);
    opacity: 0.7;
  }
  100% {
    transform: translateY(-20px) translateX(-50%);
    opacity: 0;
  }
}

/* 分类标签 - 修改为带边框样式 */
.category-tags {
  margin: 0.5rem 0 1rem !important;
}

.category-tag {
  position: relative !important;
  overflow: hidden !important;
  border: 1px solid #6c757d !important;
  font-size: 0.875rem !important;
  padding: 6px 15px !important;
  border-radius: 20px !important;
  background-color: white !important;
  color: #6c757d !important;
  margin-right: 0.5rem !important;
  margin-bottom: 0.5rem !important;
  transition: all 0.3s ease !important;

  &:hover {
    animation: bubble 0.6s ease-in-out !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 4px 8px rgba(5, 191, 219, 0.2) !important;

    &:before {
      content: "" !important;
      position: absolute !important;
      bottom: -10px !important;
      left: 50% !important;
      transform: translateX(-50%) !important;
      width: 8px !important;
      height: 8px !important;
      background-color: rgba(5, 191, 219, 0.6) !important;
      border-radius: 50% !important;
      opacity: 0 !important;
      animation: rise 0.6s ease-out forwards !important;
    }

    &:after {
      content: "" !important;
      position: absolute !important;
      bottom: -15px !important;
      left: 40% !important;
      width: 6px !important;
      height: 6px !important;
      background-color: rgba(5, 191, 219, 0.4) !important;
      border-radius: 50% !important;
      opacity: 0 !important;
      animation: rise 0.8s ease-out 0.1s forwards !important;
    }
  }

  &.active {
    background: linear-gradient(135deg, #0a4d68, #088395) !important;
    color: white !important;
    border-color: #0a4d68 !important;
    box-shadow: 0 4px 10px rgba(10, 77, 104, 0.3) !important;
    transform: translateY(-2px) !important;

    &:before {
      content: "" !important;
      position: absolute !important;
      top: 0 !important;
      left: 0 !important;
      width: 100% !important;
      height: 100% !important;
      background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.2),
        rgba(255, 255, 255, 0)
      ) !important;
      opacity: 0 !important;
      animation: shine 1.5s infinite !important;
    }
  }
}

@keyframes shine {
  0% {
    opacity: 0;
    transform: translateX(-100%);
  }
  20% {
    opacity: 0.5;
  }
  100% {
    opacity: 0;
    transform: translateX(100%);
  }
}

/* 排序按钮 */
.btn-text {
  font-size: 0.9rem !important;
  padding: 6px 10px !important;

  &.active {
    color: #0a4d68 !important;
    font-weight: 600 !important;
  }
}

/* 实时热榜 */
.card-header .card-title {
  font-size: 1.2rem !important;
  font-weight: 700 !important;
  margin-bottom: 0 !important;
}

/* 热榜项目 */
.list-group-item {
  padding: 8px 0 !important;

  .text-primary.fw-bold {
    font-size: 0.8rem !important;
    margin-right: 10px !important;
  }

  .text-truncate {
    font-size: 0.95rem !important;
    max-width: 75% !important;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .badge {
    font-size: 75% !important;
    padding: 0.25em 0.5em !important;
    margin-top: 4px;
  }
}

/* 近期活动 */
.position-relative h6 {
  font-size: 1rem !important;
  font-weight: 600 !important;
}

.text-white-50 {
  font-size: 0.8rem !important;
}

/* 按钮样式 */
.btn-sm {
  font-size: 0.875rem !important;
  padding: 0.375rem 0.75rem !important;
}

/* 保留原有样式 */
.front-home {
  padding: 20px 0;
}

.container {
  width: 100%;
  max-width: 1320px;
  margin: 0 auto;
}

.row {
  display: flex;
  flex-wrap: wrap;
  margin-right: -15px;
  margin-left: -15px;
}

.col-lg-8 {
  flex: 0 0 66.666667%;
  max-width: 66.666667%;
  padding-right: 15px;
  padding-left: 15px;
}

.col-lg-4 {
  flex: 0 0 33.333333%;
  max-width: 33.333333%;
  padding-right: 15px;
  padding-left: 15px;
}

/* 卡片样式 */
.card {
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: var(--card-bg) !important;
  background-clip: border-box;
  border-radius: 8px;
  box-shadow: var(--card-shadow) !important;
}

.border-0 {
  border: 0 !important;
}

.shadow-sm {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
}

.mb-3 {
  margin-bottom: 0.75rem;
}

.overflow-hidden {
  overflow: hidden;
}

.card-body {
  flex: 1 1 auto;
  padding: 1rem;
  color: var(--primary-text);
}

.p-0 {
  padding: 0 !important;
}

.p-3 {
  padding: 0.75rem !important;
}

.pb-2 {
  padding-bottom: 0.5rem !important;
}

.px-3 {
  padding-left: 0.75rem !important;
  padding-right: 0.75rem !important;
}

.py-2 {
  padding-top: 0.5rem !important;
  padding-bottom: 0.5rem !important;
}

.card-header {
  padding: 0.75rem 1rem;
  margin-bottom: 0;
  background-color: var(--card-bg) !important;
  border-bottom: 1px solid var(--border-color) !important;
  color: var(--primary-text);
}

.bg-transparent {
  background-color: transparent !important;
}

.border-bottom-0 {
  border-bottom: 0 !important;
}

/* 输入组样式 */
.input-group {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  align-items: stretch;
  width: 100%;
}

.input-group-text {
  display: flex;
  align-items: center;
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  color: var(--secondary-text);
  text-align: center;
  white-space: nowrap;
  background-color: var(--card-bg) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: 0.25rem;
}

.bg-white {
  background-color: #fff !important;
}

.border-end-0 {
  border-right: 0 !important;
}

.custom-input {
  flex: 1 1 auto;
  width: 1%;
  min-width: 0;

  /deep/ .el-input__inner {
    border-radius: 0;
    border-left: 0;
    background-color: var(--card-bg) !important;
    border-color: var(--border-color) !important;
    color: var(--primary-text) !important;

    &:focus {
      border-color: var(--link-color) !important;
    }
  }
}

.search-btn {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}

/* 对齐和间距 */
.d-flex {
  display: flex !important;
}

.align-items-center {
  align-items: center !important;
}

.me-2 {
  margin-right: 0.5rem !important;
}

.me-auto {
  margin-right: auto !important;
}

.ms-auto {
  margin-left: auto !important;
}

.ms-2 {
  margin-left: 0.5rem !important;
}

.mt-2 {
  margin-top: 0.5rem !important;
}

.mb-0 {
  margin-top: -10px !important;
  font-size: 1rem !important;
  margin-bottom: 0 !important;
}

.mb-2 {
  margin-bottom: 0.5rem !important;
}

.w-100 {
  width: 100% !important;
}

.position-relative {
  position: relative !important;
}

.position-absolute {
  position: absolute !important;
}

.bottom-0 {
  bottom: 0 !important;
}

.start-0 {
  left: 0 !important;
}

.d-grid {
  display: grid !important;
}

.gap-2 {
  gap: 0.5rem !important;
}

.flex-wrap {
  flex-wrap: wrap !important;
}

/* 分类标签样式 */
.category-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 8px;
}

.category-tag {
  border-radius: 20px;
  font-size: 12px;
  padding: 4px 12px;
  background-color: var(--secondary-bg) !important;
  color: var(--primary-text) !important;
  border: 1px solid var(--border-color) !important;
  margin-right: 0;

  &:hover {
    background-color: var(--hover-bg) !important;
    color: var(--link-color) !important;
  }

  &.active {
    background-color: var(--link-color) !important;
    color: #ffffff !important;
    border-color: var(--link-color) !important;
  }
}

/* 按钮样式 */
.btn-text {
  padding: 4px 8px;
  font-size: 13px;

  &.active {
    color: #0a4d68;
    font-weight: 600;
  }
}

/* 列表样式 */
.list-group {
  display: flex;
  flex-direction: column;
  padding-left: 0;
  margin-bottom: 0;
}

.list-group-item {
  position: relative;
  display: block;
  padding: 0.4rem 0;
  background-color: transparent !important;
  color: var(--primary-text) !important;
  border-bottom: 1px solid var(--border-color) !important;

  &:last-child {
    border-bottom: none;
  }

  &:hover {
    background-color: var(--hover-bg) !important;
  }

  .text-primary {
    color: var(--link-color) !important;
  }

  .text-muted {
    color: var(--secondary-text) !important;
  }
}

.list-group-flush {
  border-radius: 0;
}

.badge {
  display: inline-block;
  padding: 0.25em 0.4em;
  font-size: 75%;
  font-weight: 700;
  line-height: 1;
  text-align: center;
  white-space: nowrap;
  vertical-align: baseline;
  border-radius: 0.25rem;

  &.bg-danger {
    background-color: var(--danger-color) !important;
  }

  &.bg-primary {
    background-color: var(--link-color) !important;
  }
}

.text-danger {
  color: var(--danger-color) !important;
}

.text-primary {
  color: var(--link-color) !important;
}

.text-muted {
  color: var(--secondary-text) !important;
}

.fw-bold {
  font-weight: 700 !important;
}

.text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
  transition: color 0.2s;

  &:hover {
    color: #0a4d68;
  }
}

.rounded {
  border-radius: 0.25rem !important;
}

/* 博客列表容器 */
.blog-list-container {
  margin-top: 0;
}

/* 响应式调整 */
@media (max-width: 992px) {
  .col-lg-8,
  .col-lg-4 {
    flex: 0 0 100%;
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .d-flex {
    flex-direction: column;
  }

  .me-auto {
    margin-right: 0;
    margin-bottom: 10px;
  }
}

/* 右侧边栏卡片样式美化 */
.col-lg-4 .card {
  margin-bottom: 20px !important;
  border: none !important;
  border-radius: 12px !important;
  overflow: hidden !important;
  transition: transform 0.3s, box-shadow 0.3s !important;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08) !important;

  &:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 12px 20px rgba(0, 0, 0, 0.12) !important;
  }
}

/* 卡片头部样式 */
.col-lg-4 .card-header {
  background: linear-gradient(
    135deg,
    rgba(10, 77, 104, 0.08),
    rgba(5, 191, 219, 0.08)
  ) !important;
  border-bottom: none !important;
  padding: 15px !important;
  position: relative !important;
  overflow: hidden !important;

  &:before {
    content: "" !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 4px !important;
    height: 100% !important;
    background: linear-gradient(to bottom, #0a4d68, #05bfdb) !important;
  }

  .card-title {
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    margin-left: 8px !important;
    background: linear-gradient(90deg, #0a4d68, #05bfdb) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    position: relative !important;
  }

  i {
    font-size: 1.3rem !important;
    background: linear-gradient(135deg, #0a4d68, #05bfdb) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin-right: 8px !important;
  }
}

/* 实时热榜样式 */
.col-lg-4 .list-group-item {
  padding: 10px 15px !important;
  border-left: none !important;
  border-right: none !important;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05) !important;
  transition: background-color 0.2s !important;

  &:hover {
    background-color: rgba(5, 191, 219, 0.05) !important;
  }

  &:last-child {
    border-bottom: none !important;
  }

  .text-primary.fw-bold {
    font-size: 1.2rem !important;
    font-weight: 800 !important;
    width: 28px !important;
    height: 28px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: linear-gradient(135deg, #0a4d68, #05bfdb) !important;
    color: white !important;
    border-radius: 50% !important;
    margin-right: 12px !important;
  }

  .text-truncate {
    font-size: 1.1rem !important;
    font-weight: 500 !important;
    // color: #49c7ba !important;
    transition: color 0.2s !important;

    &:hover {
      color: #05bfdb !important;
    }
  }

  .badge.bg-danger {
    background: linear-gradient(135deg, #dc3545, #ff6b6b) !important;
    padding: 0.3em 0.6em !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 4px rgba(220, 53, 69, 0.3) !important;
  }
}

/* 近期活动样式 */
.col-lg-4 .position-relative {
  border-radius: 8px !important;
  overflow: hidden !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
  margin-bottom: 15px !important;

  img {
    transition: transform 0.5s !important;
    filter: brightness(0.9) !important;

    &:hover {
      transform: scale(1.05) !important;
      filter: brightness(1) !important;
    }
  }

  .position-absolute {
    background: linear-gradient(
      to top,
      rgba(0, 0, 0, 0.8),
      rgba(0, 0, 0, 0)
    ) !important;
    padding: 15px 12px 10px !important;
  }

  h6 {
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
    margin-bottom: 5px !important;
  }

  .text-white-50 {
    font-size: 0.85rem !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
  }
}

/* 热门标签样式 */
.col-lg-4 .el-tag {
  margin: 0 5px 8px 0 !important;
  border-radius: 20px !important;
  padding: 0 12px !important;
  height: 28px !important;
  line-height: 26px !important;
  font-size: 0.85rem !important;
  transition: all 0.3s !important;
  border: 1px solid rgba(5, 191, 219, 0.3) !important;
  background-color: rgba(5, 191, 219, 0.05) !important;

  &:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 8px rgba(5, 191, 219, 0.2) !important;
    background-color: rgba(5, 191, 219, 0.1) !important;
    border-color: rgba(5, 191, 219, 0.5) !important;
  }
}

/* 按钮样式 */
.col-lg-4 .btn-success {
  background: linear-gradient(135deg, #28a745, #20c997) !important;
  border: none !important;
  border-radius: 50px !important;
  padding: 8px 16px !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  box-shadow: 0 4px 10px rgba(40, 167, 69, 0.3) !important;
  transition: all 0.3s !important;

  &:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 15px rgba(40, 167, 69, 0.4) !important;
    background: linear-gradient(135deg, #218838, #1ca38b) !important;
  }

  &:active {
    transform: translateY(0) !important;
  }
}

/* 查看更多按钮 */
.col-lg-4 .btn-outline-primary {
  border: none !important;
  background: linear-gradient(
    to right,
    rgba(10, 77, 104, 0.05),
    rgba(5, 191, 219, 0.05)
  ) !important;
  color: #0a4d68 !important;
  font-weight: 600 !important;
  border-radius: 50px !important;
  padding: 8px 0 !important;
  transition: all 0.3s !important;
  position: relative !important;
  overflow: hidden !important;

  &:before {
    content: "" !important;
    position: absolute !important;
    bottom: 0 !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 0 !important;
    height: 2px !important;
    background: linear-gradient(to right, #0a4d68, #05bfdb) !important;
    transition: width 0.3s !important;
  }

  &:hover {
    background: linear-gradient(
      to right,
      rgba(10, 77, 104, 0.08),
      rgba(5, 191, 219, 0.08)
    ) !important;

    &:before {
      width: 80% !important;
    }
  }
}

/* 公告栏样式 */
.announcement-bar {
  width: 80%;
  margin: 45px auto 12px;
  background: var(--card-bg);
  border-left: 4px solid #05bfdb;
  border-radius: 0 8px 8px 0;
  padding: 10px 20px;
  box-shadow: var(--card-shadow);
  position: relative;
  overflow: hidden;
  color: var(--primary-text);

  .notice-content {
    color: var(--primary-text);
  }

  .notice-btn {
    color: var(--secondary-text);
    &:hover {
      color: var(--link-color);
    }
  }

  .notice-counter {
    color: var(--secondary-text);
  }
}

.announcement-bar i {
  color: #05bfdb;
  margin-right: 10px;
  font-size: 2.5rem !important;
  animation: bell-ring 2s infinite;
}

.announcement-bar .d-flex {
  justify-content: space-between;
}

.notice-controls {
  display: flex;
  align-items: center;
  margin-left: auto;
  padding-left: 15px;
}

.notice-counter {
  font-size: 0.85rem;
  color: var(--secondary-text);
  margin: 0 5px;
  min-width: 40px;
  text-align: center;
}

.notice-btn {
  padding: 2px 5px !important;
  color: var(--secondary-text);
  transition: all 0.3s ease;

  &:hover:not([disabled]) {
    color: var(--link-color);
    transform: scale(1.2);
  }
}

.notice-btn[disabled] {
  color: #c0c4cc !important;
  cursor: not-allowed;
}

@keyframes bell-ring {
  0%,
  100% {
    transform: rotate(0);
  }
  10%,
  30%,
  50%,
  70% {
    transform: rotate(10deg);
  }
  20%,
  40%,
  60% {
    transform: rotate(-10deg);
  }
  80% {
    transform: rotate(5deg);
  }
  90% {
    transform: rotate(-5deg);
  }
}

.notice-carousel {
  width: 100%;
  overflow: hidden;
  position: relative;
  height: 24px; /* 固定高度防止跳动 */
  flex: 1;
}

.notice-content {
  font-size: 0.95rem !important;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
  position: absolute;
  top: 0;
  left: 0;
}

/* 更平滑的过渡效果 */
.notice-fade-enter-active,
.notice-fade-leave-active {
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.notice-fade-enter {
  opacity: 0;
  transform: translateY(20px);
}

.notice-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.fw-bold {
  font-weight: 700;
  color: var(--primary-text);
}

.notice-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 5px;
}

.notice-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--secondary-text);
  cursor: pointer;
  margin: 0 5px;
}

.notice-counter {
  margin: 0 10px;
}

/* 专业工具区域样式优化 */
.tools-section {
  width: 85%;
  margin: 12px auto 20px;
  background: #ffffff;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 10px 25px rgba(31, 38, 135, 0.08);
  border: 1px solid rgba(226, 232, 240, 0.8);
  position: relative;
  overflow: hidden;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 12px;
  position: relative;
  z-index: 1;
}

.tool-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 14px;
  min-height: 72px;
  display: flex;
  align-items: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid #e2e8f0;
  position: relative;
  overflow: hidden;
}

.tool-icon {
  width: 42px;
  height: 42px;
  background: linear-gradient(
    135deg,
    rgba(5, 191, 219, 0.12),
    rgba(10, 77, 104, 0.08)
  );
  border-radius: 10px;
  margin-right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(5, 191, 219, 0.08);
}

.tool-icon i {
  font-size: 20px;
  color: #05bfdb;
  transition: all 0.3s ease;
  z-index: 1;
}

.tool-card span {
  font-size: 0.9rem;
  font-weight: 500;
  color: #334155;
  flex: 1;
  transition: all 0.3s ease;
}

/* 悬停效果优化 */
.tool-card:hover {
  transform: translateY(-3px);
  background: linear-gradient(135deg, #0a4d68, #088395);
  border-color: transparent;
  box-shadow: 0 8px 20px rgba(10, 77, 104, 0.15);
}

.tool-card:hover .tool-icon {
  background: rgba(255, 255, 255, 0.15);
  transform: scale(1.05);
}

.tool-card:hover .tool-icon i {
  color: #ffffff;
  transform: scale(1.05);
}

.tool-card:hover span {
  color: #ffffff;
  transform: translateX(3px);
}

/* 工具区域装饰效果 */
.tools-section::before {
  content: "";
  position: absolute;
  width: 200px;
  height: 200px;
  background: radial-gradient(
    circle,
    rgba(5, 191, 219, 0.06) 0%,
    transparent 70%
  );
  top: -100px;
  left: -100px;
  border-radius: 50%;
  z-index: 0;
  animation: float 6s ease-in-out infinite;
}

.tools-section::after {
  content: "";
  position: absolute;
  width: 180px;
  height: 180px;
  background: radial-gradient(
    circle,
    rgba(10, 77, 104, 0.05) 0%,
    transparent 70%
  );
  bottom: -90px;
  right: -90px;
  border-radius: 50%;
  z-index: 0;
  animation: float 6s ease-in-out infinite reverse;
}

@keyframes float {
  0%,
  100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.4;
  }
  50% {
    transform: translate(15px, -15px) scale(1.05);
    opacity: 0.2;
  }
}

/* 响应式布局优化 */
@media (max-width: 1200px) {
  .tools-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
}

@media (max-width: 768px) {
  .tools-section {
    padding: 15px;
  }

  .tools-grid {
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .tool-card {
    min-height: 60px;
    padding: 12px;
  }

  .tool-icon {
    width: 36px;
    height: 36px;
    margin-right: 10px;
  }

  .tool-icon i {
    font-size: 18px;
  }

  .tool-card span {
    font-size: 0.85rem;
  }
}

/* 添加暗色模式样式增强 */
:root {
  --dark-text-primary: #ffffff;
  --dark-text-secondary: #e0e0e0;
  --dark-card-bg: #1c1c1c;
  --dark-border-color: #333333;
}

/* 暗色模式下热门博客和标签样式加强 */
.el-dark {
  .card {
    background-color: var(--dark-card-bg);
    border-color: var(--dark-border-color);
  }

  .card-title,
  .trending-title {
    color: var(--dark-text-primary) !important;
    font-weight: 600;
  }

  .hot-blog-title,
  .text-primary {
    color: var(--dark-text-primary) !important;
  }

  .list-group-item {
    color: var(--dark-text-secondary) !important;
    background-color: transparent !important;
  }

  .el-tag {
    background-color: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    color: var(--dark-text-primary);
  }
}

/* 通过body类适配暗色模式 */
body.dark-theme {
  .card {
    background-color: var(--dark-card-bg);
    border-color: var(--dark-border-color);
  }

  .card-title,
  .trending-title {
    color: var(--dark-text-primary) !important;
    font-weight: 600;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
  }

  .hot-blog-title {
    color: var(--dark-text-primary) !important;
  }

  .text-primary {
    color: #4ecdc4 !important; /* 使用亮青色作为强调色 */
  }

  .list-group-item {
    color: var(--dark-text-secondary) !important;
    background-color: transparent !important;
  }

  .el-tag {
    background-color: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    color: var(--dark-text-primary);

    &:hover {
      background-color: rgba(255, 255, 255, 0.2);
      color: #ffffff;
    }
  }

  /* 增强暗色模式下的标签对比度 */
  .badge {
    &.bg-danger {
      background-color: #ff6b6b !important;
    }

    &.bg-primary {
      background-color: #4ecdc4 !important;
    }
  }
}
</style>
