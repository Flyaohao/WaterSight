<template>
  <div class="front-container">
    <!-- 导航栏 -->
    <nav
      class="navbar nav-fixed"
      :class="[
        themeClass,
        {
          'logged-in': isValidUser,
          'amateur-theme': !isResearchMode,
          'dark-theme': isDarkTheme,
        },
      ]"
    >
      <div class="navbar-content">
        <!-- Logo和标题 -->
        <div class="navbar-brand">
          <img
            src="@/assets/imgs/logo1.png"
            alt="WaterSight Logo"
            class="brand-logo"
          />
          <div class="liquid-title">
            <h1 data-text="WaterSight">
              WaterSight <span class="subtitle">水下研究平台</span>
            </h1>
          </div>
        </div>

        <!-- 导航菜单 -->
        <div class="navbar-menu">
          <el-menu
            :default-active="$route.path"
            mode="horizontal"
            router
            :class="[
              themeClass,
              {
                'logged-in': isValidUser,
                'menu-collapsed': isMenuCollapsed,
                'dark-theme-menu': isDarkTheme,
              },
            ]"
            background-color="transparent"
            text-color="#fff"
            active-text-color="#409eff"
          >
            <!-- 科研人员角色导航 -->
            <template v-if="isResearchMode">
              <el-menu-item index="/front/researcherHome">
                <i class="el-icon-s-home"></i> 首页
              </el-menu-item>
              <el-menu-item
                index="/front/datasetPreprocessing"
                @click="handleMenuClick('/front/datasetPreprocessing')"
                :class="{
                  'menu-item-expanded':
                    activeMenuItem === '/front/datasetPreprocessing',
                }"
              >
                <i class="el-icon-data-line"></i> 数据集生成
              </el-menu-item>
              <el-menu-item
                index="/front/enhance"
                @click="handleMenuClick('/front/enhance')"
                :class="{
                  'menu-item-expanded': activeMenuItem === '/front/enhance',
                }"
              >
                <i class="el-icon-picture"></i> 图像增强
              </el-menu-item>
<!--              <el-menu-item-->
<!--                index="/front/fishyolo"-->
<!--                @click="handleMenuClick('/front/fishyolo')"-->
<!--                :class="{-->
<!--                  'menu-item-expanded': activeMenuItem === '/front/fishyolo',-->
<!--                }"-->
<!--              >-->
<!--                <i class="el-icon-view"></i> 鱼儿识别-->
<!--              </el-menu-item>-->
              <el-menu-item
                index="/front/coralyolo"
                @click="handleMenuClick('/front/coralyolo')"
                :class="{
                  'menu-item-expanded': activeMenuItem === '/front/coralyolo',
                }"
              >
                <i class="el-icon-discover"></i> 珊瑚健康监测
              </el-menu-item>

              <el-menu-item
                index="/front/resources"
                @click="handleMenuClick('/front/resources')"
                :class="{
                  'menu-item-expanded': activeMenuItem === '/front/resources',
                }"
              >
                <i class="el-icon-collection"></i> 研究资源
              </el-menu-item>
              <el-menu-item index="/front/home">
                <i class="el-icon-s-comment"></i> 交流中心
              </el-menu-item>
            </template>

            <!-- 业余爱好者角色导航 -->
            <template v-else>
              <el-menu-item index="/front/home">
                <i class="el-icon-s-home"></i> 首页
              </el-menu-item>
              <el-menu-item index="/front/activity">
                <i class="el-icon-s-cooperation"></i> 活动
              </el-menu-item>
              <el-menu-item index="/front/enhance">
                <i class="el-icon-picture"></i> 图像处理
              </el-menu-item>
              <el-menu-item index="/front/fishyolo">
                <i class="el-icon-view"></i> 鱼类识别
              </el-menu-item>
<!--              <el-menu-item index="/front/coralyolo">-->
<!--                <i class="el-icon-discover"></i> 海星识别-->
<!--              </el-menu-item>-->
            </template>
          </el-menu>
        </div>

        <!-- 用户操作区 -->
        <div class="navbar-end">
          <div class="user-panel">
            <theme-toggle />
            <el-button type="primary" @click="addBlog" class="publish-btn">
              <i class="el-icon-edit"></i> 发表博客
            </el-button>
            <el-dropdown trigger="hover">
              <div class="user-info">
                <img
                  :src="user?.avatar || require('@/assets/imgs/bgc2.jpg')"
                  alt=""
                  class="user-avatar"
                  @error="handleAvatarError"
                />
                <span class="user-name">{{ user?.name || "用户" }}</span>
                <i class="el-icon-arrow-down"></i>
              </div>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item @click.native="switchRole">
                  <i class="el-icon-refresh"></i> 切换角色
                </el-dropdown-item>
                <el-dropdown-item @click.native="gotoPerson">
                  <i class="el-icon-user"></i> 个人中心
                </el-dropdown-item>
                <el-dropdown-item @click.native="gotoMessageCenter">
                  <i class="el-icon-message"></i> 消息中心
                  <el-badge
                    v-if="unreadCount > 0"
                    :value="unreadCount"
                    class="message-badge"
                  ></el-badge>
                </el-dropdown-item>
                <el-dropdown-item @click.native="logout">
                  <i class="el-icon-switch-button"></i> 退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要内容区域 -->
    <div
      class="main-content"
      :class="[themeClass, { 'dark-theme-content': isDarkTheme }]"
    >
      <router-view ref="child" @update:user="updateUser" />
    </div>

    <!-- 底部 -->
    <footer v-if="$route.path !== '/front/researcherHome'" class="footer">
<!--      <div class="footer-content">-->
<!--        <div class="footer-section about-us">-->
<!--          <h2>关于我们</h2>-->
<!--          <div class="team-info">-->
<!--            <h3>视界潜航团队</h3>-->
<!--            <p>-->
<!--              致力于研究水下视觉智能技术，并致力于为水下探索提供技术支持。-->
<!--            </p>-->
<!--          </div>-->
<!--        </div>-->
<!--        <div class="footer-section contact-info">-->
<!--          <h2>联系我们</h2>-->
<!--          <div class="contact-items">-->
<!--            <div class="contact-item">-->
<!--              <i class="el-icon-phone"></i>-->
<!--              <span>电话: 123-456-7890</span>-->
<!--            </div>-->
<!--            <div class="contact-item">-->
<!--              <i class="el-icon-message"></i>-->
<!--              <span>邮箱: contact@watersight.com</span>-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->
      <div class="footer-bottom">
        <p>© 2025 Watersight 水下论坛. All rights reserved.</p>
      </div>
    </footer>

    <transition name="fade">
      <div v-show="showBackTop" class="back-to-top" @click="scrollToTop">
        <i class="el-icon-arrow-up"></i>
      </div>
    </transition>

    <login-dialog ref="loginDialog" />
  </div>
</template>

<script>
import request from "@/utils/request";
import Vue from "vue";
import { mapGetters, mapActions } from "vuex";
import ThemeToggle from "@/components/ThemeToggle.vue";
import LoginDialog from "@/components/LoginDialog.vue";

// 创建事件总线
const bus = new Vue();

export default {
  name: "FrontLayout",
  components: {
    ThemeToggle,
    LoginDialog,
  },
  filters: {
    formatNumber(value) {
      if (value >= 1000000) {
        return (value / 1000000).toFixed(1) + "M";
      } else if (value >= 1000) {
        return (value / 1000).toFixed(1) + "K";
      }
      return value;
    },
    formatLossRate(value) {
      return value.toFixed(4);
    },
  },
  data() {
    return {
      user: null,
      title: "",
      searchType: "blog",
      searchKeyword: "",
      showBackTop: false,
      tokenCheckInterval: null,
      learningRate: 0.001,
      batchSize: 32,
      trendingList: [
        { title: "珊瑚礁修复研究", value: 156 },
        { title: "深海生物识别", value: 142 },
        { title: "水质监测分析", value: 98 },
        { title: "海洋生态系统", value: 87 },
        { title: "海水污染治理", value: 76 },
      ],
      isTraining: false,
      modelStats: {
        accuracy: 98.5,
        samples: 2300000,
        epochTime: "2.3s",
        lossRate: 0.0023,
      },
      menuItems: [
        { path: "/front/home", name: "首页", icon: "el-icon-s-home" },
        { path: "/front/activity", name: "活动", icon: "el-icon-s-promotion" },
        { path: "/front/blog", name: "博客", icon: "el-icon-s-management" },
        { path: "/front/resources", name: "资源", icon: "el-icon-folder" },
        { path: "/front/detect", name: "检测", icon: "el-icon-camera" },
      ],
      isUpcomingCollapsed: false,
      unreadCount: 0,
      messageCheckInterval: null,
      roleDialogVisible: false,
      selectedRole: "",
      researchCategories: [],
      hobbyCategories: [],
      isMenuCollapsed: false,
      activeMenuItem: null,
    };
  },
  computed: {
    ...mapGetters(["isDarkTheme"]),
    isValidUser() {
      try {
        const userData = localStorage.getItem("xm-user");
        if (!userData) return false;
        const user = JSON.parse(userData);
        return !!user && !!user.token;
      } catch (error) {
        console.error("用户数据解析错误:", error);
        return false;
      }
    },
    isResearchMode() {
      return this.user?.browseRole === "RESEARCHER";
    },
    themeClass() {
      try {
        const userData = localStorage.getItem("xm-user");
        if (!userData) return "";
        const user = JSON.parse(userData);
        return {
          "research-theme": user?.browseRole === "RESEARCHER",
          "default-theme": user?.browseRole === "ALL",
          "amateur-theme": user?.browseRole === "ALL",
        };
      } catch (error) {
        console.error("主题类解析错误:", error);
        return "";
      }
    },
  },
  watch: {
    $route(to) {
      // 如果是科研人员首页，重置导航菜单状态
      if (to.path === "/front/researcherHome") {
        this.isMenuCollapsed = false;
        this.activeMenuItem = null;
      }
    },
  },
  created() {
    document.body.classList.add("front-body");
    this.initUser();
    this.startTokenCheck();
    this.startMessageCheck();
    this.loadCategories(); // 加载分类
    window.addEventListener("scroll", this.handleScroll);

    // 监听事件总线事件
    bus.$on("refreshBlogList", () => {
      if (this.$refs.child && this.$refs.child.$refs.blogList) {
        this.$refs.child.$refs.blogList.load();
      }
    });

    bus.$on("refreshCategories", () => {
      this.loadCategories(); // 刷新分类
    });
  },
  mounted() {
    this.updateTrendingList();
    this.initTheme();
  },
  beforeDestroy() {
    document.body.classList.remove("front-body");
    window.removeEventListener("scroll", this.handleScroll);
    this.stopTokenCheck();
    this.stopMessageCheck();

    // 移除事件监听
    bus.$off("refreshBlogList");
    bus.$off("refreshCategories");
  },
  methods: {
    ...mapActions(["toggleTheme", "initTheme"]),
    initUser() {
      try {
        const userData = localStorage.getItem("xm-user");
        if (userData) {
          this.user = JSON.parse(userData);
        } else {
          this.user = null;
        }
      } catch (error) {
        console.error("初始化用户数据错误:", error);
        this.user = null;
        localStorage.removeItem("xm-user");
      }
    },
    startTokenCheck() {
      this.stopTokenCheck();

      this.tokenCheckInterval = setInterval(() => {
        const userStr = localStorage.getItem("xm-user");
        if (!userStr) {
          this.user = {};
          return;
        }

        try {
          const user = JSON.parse(userStr);
          if (!user || !user.token) {
            this.user = {};
          }
        } catch (e) {
          console.error("检查token失败", e);
          this.user = {};
        }
      }, 60000);
    },
    stopTokenCheck() {
      if (this.tokenCheckInterval) {
        clearInterval(this.tokenCheckInterval);
        this.tokenCheckInterval = null;
      }
    },
    startMessageCheck() {
      this.stopMessageCheck();
      if (!this.isValidUser) return;

      // 立即检查一次
      this.checkUnreadMessages();

      // 每30秒检查一次
      this.messageCheckInterval = setInterval(() => {
        this.checkUnreadMessages();
      }, 30000);
    },
    stopMessageCheck() {
      if (this.messageCheckInterval) {
        clearInterval(this.messageCheckInterval);
        this.messageCheckInterval = null;
      }
    },
    checkUnreadMessages() {
      this.$request.get("/message/unread/count").then((res) => {
        if (res.code === "200") {
          this.unreadCount = res.data;
          this.$store.commit("setUnreadMessageCount", res.data);
        }
      });
    },
    handleScroll() {
      this.showBackTop = window.pageYOffset > 300;
    },
    scrollToTop() {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    },
    goSearch() {
      if (!this.title) {
        this.$message.warning("请输入搜索关键词");
        return;
      }

      this.$router.push({
        path: "/front/search",
        query: {
          title: this.title,
          type: this.searchType,
          _t: Date.now(),
        },
      });
    },
    addBlog() {
      this.$router.push("/front/newBlog");
    },
    logout() {
      try {
        localStorage.removeItem("xm-user");
        localStorage.removeItem("xm-token");
        this.user = null;
        this.$router.push("/login");
        this.$message.success("退出成功");
      } catch (error) {
        console.error("退出登录错误:", error);
        this.$message.error("退出失败");
      }
    },
    gotoPerson() {
      if (this.user.id) {
        this.$router.push({
          path: "/front/authorHome",
          query: { authorId: this.user.id },
        });
      }
    },
    gotoMessageCenter() {
      this.$router.push("/front/messageCenter");
    },
    startModelTraining() {
      if (this.isTraining) return;

      this.isTraining = true;
      this.$refs.modelTrainBtn?.classList.add("training");

      let progress = 0;
      const interval = setInterval(() => {
        progress += 10;
        if (progress >= 100) {
          clearInterval(interval);
          this.isTraining = false;
          this.$refs.modelTrainBtn?.classList.remove("training");
          this.$message.success("模型训练完成");

          this.modelStats.accuracy = (98.5 + Math.random() * 0.5).toFixed(2);
          this.modelStats.lossRate = (0.0023 - Math.random() * 0.0005).toFixed(
            4
          );
        }
      }, 500);
    },
    updateTrendingList() {
      setInterval(() => {
        this.trendingList = this.trendingList
          .map((item) => ({
            ...item,
            value: item.value + Math.floor(Math.random() * 10 - 5),
          }))
          .sort((a, b) => b.value - a.value);
      }, 5000);
    },
    switchRole() {
      // 显示角色选择对话框
      this.$refs.loginDialog.show();
    },
    updateUser(userData) {
      try {
        if (userData) {
          this.user = userData;
          localStorage.setItem("xm-user", JSON.stringify(userData));
        } else {
          this.user = null;
          localStorage.removeItem("xm-user");
        }
      } catch (error) {
        console.error("更新用户数据错误:", error);
        this.user = null;
      }
    },
    handleAvatarError(e) {
      e.target.src = require("@/assets/imgs/bgc2.jpg");
    },
    async loadCategories() {
      try {
        // 加载科研人员分类
        const researchRes = await request.get("/category/selectByRole", {
          params: { role: "RESEARCHER" },
        });
        if (researchRes.code === "200") {
          this.researchCategories = researchRes.data || [];
        }

        // 加载业余爱好者分类
        const hobbyRes = await request.get("/category/selectByRole", {
          params: { role: "HOBBYIST" },
        });
        if (hobbyRes.code === "200") {
          this.hobbyCategories = hobbyRes.data || [];
        }
      } catch (error) {
        console.error("加载分类失败:", error);
        this.$message.error("加载分类失败");
      }
    },
    handleMenuClick(item) {
      // 如果点击的是识别按钮的子项目
      if (item === "/front/fishyolo" || item === "/front/coralyolo") {
        this.activeMenuItem = item;
        if (this.isResearchMode) {
          this.isMenuCollapsed = true;
        }
        return;
      }

      this.activeMenuItem = item;
      if (this.isResearchMode) {
        this.isMenuCollapsed = true;
      }
    },
  },
};
</script>

<style lang="less" scoped>
/* 主题变量 */
:root {
  --deep-blue: #003366;
  --tech-silver: #c0c0c0;
  --accent-blue: #0055a4;
  --panel-bg: rgba(0, 51, 102, 0.95);
  --text-primary: #e0e0e0;
  --text-secondary: #a0a0a0;
}

/* 科技感按钮 */
.tech-button {
  background: transparent;
  border: 1px solid var(--tech-silver);
  color: var(--tech-silver);
  padding: 8px 16px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;

  &:hover {
    background: var(--tech-silver);
    color: var(--deep-blue);
  }

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--tech-silver));
    animation: buttonScan 2s linear infinite;
  }
}

/* 神经网络可视化 */
.network-structure {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 0;

  .neural-node {
    width: 12px;
    height: 12px;
    background: var(--tech-silver);
    border-radius: 50%;
    position: relative;
    animation: pulseNode 2s ease-in-out infinite;
  }

  .neural-connection {
    flex: 1;
    height: 2px;
    background: linear-gradient(
      90deg,
      var(--tech-silver) 0%,
      var(--accent-blue) 50%,
      var(--tech-silver) 100%
    );
    margin: 0 10px;
    position: relative;
    overflow: hidden;

    &::after {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: linear-gradient(
        90deg,
        transparent,
        var(--accent-blue),
        transparent
      );
      animation: dataTransfer 2s linear infinite;
    }
  }
}

/* 数据统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-top: 15px;
}

.stat-card {
  background: rgba(0, 51, 102, 0.5);
  border: 1px solid rgba(192, 192, 192, 0.1);
  border-radius: 8px;
  padding: 15px;
  text-align: center;

  .stat-value {
    font-size: 24px;
    font-weight: 600;
    color: var(--tech-silver);
    margin-bottom: 5px;
  }

  .stat-label {
    font-size: 12px;
    color: var(--text-secondary);
  }
}

/* 动画效果 */
@keyframes buttonScan {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

@keyframes pulseNode {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.7;
  }
  50% {
    transform: scale(1.2);
    opacity: 1;
  }
}

@keyframes dataTransfer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* 科技感图标 */
.icon-scientific {
  width: 24px;
  height: 24px;
  stroke: currentColor;
  stroke-width: 1.5;
  fill: none;
}

/* 导航栏样式优化 */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  z-index: 1000;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(8px);
  box-shadow: 0 1px 0 0 rgba(255, 255, 255, 0.1);

  &.dark-theme {
    background: linear-gradient(90deg, #1a1a1a, #2c2c2c);
    box-shadow: 0 1px 0 0 rgba(255, 255, 255, 0.05);

    .navbar-brand .liquid-title h1,
    .navbar-brand .subtitle {
      color: var(--text-color-primary);
    }

    .user-panel .user-info {
      background-color: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .user-panel .user-name {
      color: var(--text-color-primary);
    }

    .publish-btn {
      background-color: var(--primary-color);
      border-color: var(--primary-color);
      color: var(--white);
    }

    .publish-btn:hover {
      background-color: var(--primary-color-hover);
      border-color: var(--primary-color-hover);
    }
  }

  .navbar-content {
    max-width: 1440px;
    margin: 0 auto;
    padding: 0 24px;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .navbar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    padding: 8px 0;
    transition: transform 0.3s ease;

    &:hover {
      transform: translateY(-1px);
    }

    .brand-logo {
      height: 40px;
      width: auto;
      filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
    }

    .liquid-title {
      display: flex;
      flex-direction: column;
      gap: 2px;

      h1 {
        font-family: "Georama", sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #fff;
        margin: 0;
        line-height: 1.2;
        letter-spacing: 0.5px;
      }

      .subtitle {
        font-size: 0.875rem;
        color: rgba(255, 255, 255, 0.85);
        font-weight: 400;
      }
    }
  }

  /deep/ .el-menu {
    background: transparent;
    border: none;
    display: flex;
    align-items: center;
    height: 100%;
    margin-left: 15px;
    flex-wrap: nowrap;

    &.el-menu--horizontal {
      border-bottom: none;
    }

    .el-menu-item {
      height: 64px;
      line-height: 64px;
      font-size: 13px;
      color: rgba(255, 255, 255, 0.85);
      padding: 0 8px;
      border: none !important;
      position: relative;
      transition: all 0.25s ease;
      margin: 0;

      i {
        color: rgba(255, 255, 255, 0.85);
        margin-right: 3px;
        font-size: 15px;
      }

      &:hover {
        color: #fff;
        background-color: rgba(255, 255, 255, 0.1);
      }

      &.is-active {
        color: #fff;
        background-color: rgba(255, 255, 255, 0.15);
        font-weight: 500;
      }
    }
  }
}

.navbar-menu /deep/ .el-menu {
  &.menu-collapsed {
    .el-menu-item {
      transition: all 0.25s ease;
    }

    .el-menu-item:not(.menu-item-expanded) {
      opacity: 0.6;
    }

    .menu-item-expanded {
      position: relative;
      color: #fff;
      background: rgba(255, 255, 255, 0.2);
      font-weight: 500;

      &::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: #fff;
        transform: scaleX(0.7);
        transition: transform 0.25s ease;
      }

      &:hover::after {
        transform: scaleX(1);
      }

      i {
        color: #fff;
      }
    }
  }
}

/* 研究者主题特定样式 */
.navbar.research-theme {
  /deep/ .el-menu {
    .el-menu-item {
      padding: 0 8px;
      margin: 0;

      i {
        font-size: 14px;
        margin-right: 3px;
      }
    }

    &.menu-collapsed {
      .menu-item-expanded {
        background: rgba(255, 255, 255, 0.15);
      }
    }
  }
}

/* 未登录状态 */
.navbar:not(.logged-in) {
  background: linear-gradient(
    90deg,
    rgba(0, 102, 188, 0.95),
    rgba(0, 116, 217, 0.95)
  );

  .auth-buttons {
    display: flex;
    gap: 16px;

    .el-button {
      height: 36px;
      padding: 0 24px;
      font-size: 14px;
      font-weight: 500;
      border-radius: 18px;
      transition: all 0.3s ease;

      &--text {
        color: rgba(255, 255, 255, 0.85);

        &:hover {
          color: #fff;
          transform: translateY(-1px);
        }
      }

      &--primary {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: #fff;

        &:hover {
          background: rgba(255, 255, 255, 0.2);
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
      }
    }
  }
}

/* 业余爱好者主题和科研工作者主题样式 - 整合后的简洁版本 */
.navbar {
  &.research-theme {
    background: linear-gradient(90deg, #0a2463, #1e3a8a);
    box-shadow: 0 2px 10px rgba(10, 36, 99, 0.2);

    &.dark-theme {
      background: linear-gradient(90deg, #0a1433, #102254);
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }

    /deep/ .el-menu {
      .el-menu-item::after {
        background-color: #4d7eff;
      }

      .el-menu-item.is-active::after {
        width: 70%;
      }
    }
  }

  &.amateur-theme {
    background: linear-gradient(90deg, #85cece, #05bfdb);

    &.dark-theme {
      background: linear-gradient(90deg, #106466, #0a4d68);

      .navbar-brand .liquid-title h1,
      .navbar-brand .subtitle,
      .el-menu-item,
      .el-submenu__title,
      .user-panel .user-name {
        color: var(--text-color-primary) !important;
      }

      .el-menu-item::after {
        background-color: var(--primary-color);
      }

      .el-menu-item:hover,
      .el-menu-item.is-active {
        background-color: rgba(255, 255, 255, 0.1) !important;
      }
    }

    /* 统一导航栏所有元素样式 */
    .navbar-brand .liquid-title h1,
    .navbar-brand .subtitle,
    .el-menu-item,
    .el-submenu__title,
    .user-panel .user-info,
    .user-panel .user-name {
      color: #2c3e50 !important;
    }

    .navbar-brand .liquid-title h1 {
      text-shadow: 1px 1px 3px rgba(255, 255, 255, 0.5);
    }

    /* 菜单项样式 */
    .el-menu.el-menu--horizontal {
      background: transparent !important;
      border-bottom: none !important;
    }

    .el-menu-item {
      font-weight: 500;

      &:hover,
      &.is-active {
        color: #1e3a8a !important;
        background-color: rgba(255, 255, 255, 0.25) !important;
      }

      &::after {
        background: #1e3a8a;
      }
    }

    .el-submenu__title {
      &:hover {
        color: #1e3a8a !important;
        background-color: rgba(255, 255, 255, 0.25) !important;
      }
    }

    /* 用户操作区样式 */
    .user-panel .user-info {
      border: 1px solid rgba(44, 62, 80, 0.2);
      background-color: rgba(255, 255, 255, 0.25);
    }

    .publish-btn {
      background-color: #3182ce !important;
      border-color: #3182ce !important;
      box-shadow: 0 2px 5px rgba(49, 130, 206, 0.3);
      color: white !important;
    }

    .publish-btn:hover {
      background-color: #2c5282 !important;
      border-color: #2c5282 !important;
    }

    /* 导航栏整体高度和对齐 */
    .navbar-content {
      background: transparent;
    }
  }
}

/* 下拉菜单样式 */
/deep/ .el-dropdown-menu {
  padding: 8px 0;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border: none;

  .el-dropdown-menu__item {
    padding: 10px 20px;
    font-size: 14px;
    line-height: 1.4;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s ease;

    i {
      font-size: 16px;
      color: #909399;
    }

    &:hover {
      background: #f5f7fa;
      color: var(--theme-color);

      i {
        color: var(--theme-color);
      }
    }

    .message-badge {
      margin-left: auto;
    }
  }
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .navbar {
    .navbar-content {
      padding: 0 8px;
    }

    /deep/ .el-menu {
      margin-left: 8px;

      .el-menu-item {
        padding: 0 6px;

        i {
          margin-right: 2px;
        }
      }
    }
  }
}

@media (max-width: 992px) {
  .navbar {
    .navbar-content {
      /deep/ .el-menu {
        .el-menu-item {
          padding: 0 4px;
          font-size: 12px;

          i {
            font-size: 14px;
            margin-right: 2px;
          }
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .navbar {
    .navbar-content {
      .navbar-brand {
        h1 {
          font-size: 1.25rem;
        }
      }

      /deep/ .el-menu {
        display: none;
      }

      .user-panel {
        .publish-btn {
          padding: 0 15px;

          span {
            display: none;
          }
        }

        .user-name {
          display: none;
        }
      }
    }
  }
}

/* 添加页脚样式 */
.footer {
  background: linear-gradient(135deg, #0a4d68, #088395);
  color: white;
  padding: 0;
  margin-top: 0px;

  .footer-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    justify-content: space-between;
    gap: 40px;

    @media (max-width: 768px) {
      flex-direction: column;
      gap: 30px;
    }

    .footer-section {
      flex: 1;

      h2 {
        font-size: 1.5rem;
        margin-bottom: 20px;
        position: relative;
        padding-bottom: 10px;

        &:after {
          content: "";
          position: absolute;
          left: 0;
          bottom: 0;
          width: 50px;
          height: 3px;
          background: #05bfdb;
        }
      }

      &.about-us {
        .team-info {
          h3 {
            font-size: 1.2rem;
            margin-bottom: 15px;
            color: #05bfdb;
          }

          p {
            line-height: 1.6;
            color: rgba(255, 255, 255, 0.8);
          }
        }
      }

      &.contact-info {
        .contact-items {
          display: flex;
          flex-direction: column;
          gap: 15px;

          .contact-item {
            display: flex;
            align-items: center;
            gap: 10px;
            color: rgba(255, 255, 255, 0.8);

            i {
              color: #05bfdb;
              font-size: 20px;
            }

            &:hover {
              color: white;
              transform: translateX(5px);
              transition: all 0.3s ease;
            }
          }
        }
      }
    }
  }

  .footer-bottom {
    //margin-top: 40px;
    padding: 20px;
    text-align: center;
    border-top: 1px solid rgba(255, 255, 255, 0.1);

    p {
      margin: 0;
      color: rgba(255, 255, 255, 0.6);
      font-size: 0.9rem;
    }
  }
}

/* 调整主体内容最小高度，确保页脚始终在底部 */
.front-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--primary-bg);
  color: var(--primary-text);
  transition: background-color 0.3s ease, color 0.3s ease;
}

/* 主题样式 */
.research-theme {
  &.main-content {
    // background: #d9e8ff;
    min-height: calc(100vh - 64px);

    .content-container {
      max-width: 1200px;
      margin: 0 auto;
      background: #fff;
      border-radius: 8px;
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
      padding: 20px;
    }
  }
}

.default-theme {
  &.navbar {
    background: #85cece; /* 业余爱好者导航栏颜色 */
    box-shadow: 0 2px 8px rgba(26, 200, 237, 0.25);
  }

  &.main-content {
    background: #f5f7fa;
    min-height: calc(100vh - 60px);

    .content-container {
      max-width: 1200px;
      margin: 0 auto;
      background: #fff;
      border-radius: 8px;
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
      padding: 20px;
    }
  }
}

/* 主内容区域样式 */
.main-content,
.main-content.research-theme,
.main-content.default-theme {
  padding-top: 64px; // 为固定导航栏留出空间
  min-height: calc(100vh - 64px);
  background-image: url("@/assets/imgs/bgc3.jpg");
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  position: relative;
  background-repeat: no-repeat;

  &.dark-theme-content {
    background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
      url("@/assets/imgs/bgc3.jpg");
  }
}

@keyframes wave {
  0%,
  100% {
    clip-path: polygon(
      0% 45%,
      15% 44%,
      32% 50%,
      54% 60%,
      70% 61%,
      84% 59%,
      100% 52%,
      100% 100%,
      0% 100%
    );
  }
  50% {
    clip-path: polygon(
      0% 60%,
      16% 65%,
      34% 66%,
      51% 62%,
      67% 50%,
      84% 45%,
      100% 46%,
      100% 100%,
      0% 100%
    );
  }
}

.liquid-title {
  position: relative;
  margin-left: 0;
  overflow: hidden;
  max-width: 100%;

  h1 {
    font-family: "Georama", sans-serif;
    color: #ffffff;
    font-size: 1.3rem !important;
    text-shadow: 0 0 30px rgba(17, 87, 137, 0.6);
    font-weight: 600;
    position: relative;
    white-space: nowrap;
    line-height: 1;
    margin: 0;
    padding: 10px 0;

    &::before {
      content: attr(data-text);
      position: absolute;
      left: 0;
      top: 10px;
      width: 100%;
      height: calc(100% - 20px);
      color: #3e92cc;
      background: linear-gradient(180deg, #3e92cc, #0a2463, #3e92cc);
      -webkit-background-clip: text;
      background-clip: text;
      overflow: hidden;
      animation: wave 3.5s ease-in-out infinite;
    }
  }
}

.front-header-left {
  display: flex;
  align-items: center;
  flex: 0 0 auto;
  margin-right: 20px;
  overflow: hidden;
  max-width: 300px;

  img {
    height: 40px;
    margin-right: 10px;
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .front-header-left {
    flex-direction: column;
    align-items: flex-start;
    flex: 0 0 auto;
    max-width: 250px;
  }

  .liquid-title h1 {
    font-size: 1.4rem !important;
  }
}

@media (max-width: 576px) {
  .liquid-title h1 {
    font-size: 1.2rem !important;
  }

  .front-header-left {
    max-width: 200px;
  }
}

.user-panel {
  display: flex;
  align-items: center;
  gap: 15px;

  .publish-btn {
    padding: 8px 15px;
    font-size: 14px;
    border-radius: 4px;
    background: linear-gradient(135deg, #0a4d68, #088395);
    border: none;
    transition: all 0.3s ease;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(10, 77, 104, 0.2);
    }

    i {
      margin-right: 4px;
    }
  }

  .user-info {
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    padding: 5px 10px;
    border-radius: 4px;
    transition: all 0.3s;

    &:hover {
      background: rgba(255, 255, 255, 0.1);
    }

    .user-avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
    }

    .user-name {
      color: whitesmoke;
    }
  }
}

.message-badge {
  margin-left: 8px;
  /deep/ .el-badge__content {
    background-color: #f56c6c;
  }
}

/deep/ .el-dialog {
  border-radius: 16px;
  overflow: hidden;

  .el-dialog__header {
    background: #2a60c9;
    padding: 20px;
    margin: 0;

    .el-dialog__title {
      color: white;
      font-size: 20px;
      font-weight: 600;
    }
  }

  .el-dialog__body {
    padding: 30px 20px;
  }
}

/* 添加淡入淡出动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

/* 添加导航栏动画样式 - 整合后的版本 */
.navbar .navbar-menu /deep/ .el-menu {
  &.menu-collapsed {
    .el-menu-item:not(.menu-item-expanded),
    .el-submenu:not(.menu-item-expanded) {
      width: auto;
      padding: 0 20px;
      opacity: 1;
      pointer-events: auto;
      overflow: visible;
      margin: 0;
    }

    .menu-item-expanded {
      position: relative;
      font-weight: bold;

      &::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 20px;
        right: 20px;
        width: calc(100% - 40px);
        height: 2px;
        background: #409eff;
      }
    }
  }
}

/* 添加一个更明确的背景图片样式 */
body.front-body {
  background-image: url("@/assets/imgs/bgc3.jpg") !important;
  background-size: cover !important;
  background-position: center center !important;
  background-attachment: fixed !important;
  background-repeat: no-repeat !important;
  min-height: 100vh;
}

.theme-switch {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-right: 15px;
  background: rgba(0, 0, 0, 0.05);

  &:hover {
    background: rgba(0, 0, 0, 0.1);
  }

  i {
    font-size: 20px;
    color: #606266;
  }
}

.dark .theme-switch {
  background: rgba(255, 255, 255, 0.1);

  &:hover {
    background: rgba(255, 255, 255, 0.2);
  }

  i {
    color: #dcdfe6;
  }
}

.theme-icon-enter-active,
.theme-icon-leave-active {
  transition: all 0.3s ease;
}

.theme-icon-enter,
.theme-icon-leave-to {
  opacity: 0;
  transform: rotate(30deg) scale(0.7);
}
</style>
