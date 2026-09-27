<template>
  <div class="front-container">
    <!-- 添加登录弹窗组件 -->
    <login-dialog ref="loginDialog" @login-success="handleLoginSuccess" />

    <!-- 路由视图 -->
    <router-view></router-view>
  </div>
</template>

<script>
import LoginDialog from "@/components/LoginDialog";

export default {
  name: "Front",
  components: {
    LoginDialog,
  },
  data() {
    return {
      isLogin: false,
      unreadCount: 0,
    };
  },
  created() {
    this.checkLoginStatus();
    this.checkUnreadMessages();
    // 添加路由守卫
    this.$router.beforeEach((to, from, next) => {
      const needLogin = ["NewBlog", "BlogDetail", "Person"];
      if (needLogin.includes(to.name) && !this.isLogin) {
        this.$refs.loginDialog.show();
        next(false);
      } else {
        next();
      }
    });
  },
  methods: {
    checkLoginStatus() {
      const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
      this.isLogin = !!user.role;
    },
    handleLoginSuccess() {
      this.isLogin = true;
      this.checkLoginStatus();
      // 登录成功后重新加载当前路由
      this.$router.replace(this.$route.fullPath);

      // 触发全局事件，通知其他组件刷新数据
      this.$root.$emit("login-success");
    },
    checkUnreadMessages() {
      console.log("开始检查未读消息...");
      this.$request
        .get("/message/unread/count")
        .then((res) => {
          console.log("未读消息数量响应:", res);
          if (res.code === "0") {
            this.unreadCount = res.data;
            console.log("更新未读消息数量:", this.unreadCount);
          }
        })
        .catch((err) => {
          console.error("检查未读消息失败:", err);
        });
    },
  },
};
</script>

<style lang="less">
/* 导入手写风格字体 */
@import url("https://fonts.googleapis.com/css2?family=Indie+Flower&display=swap");

/* 业余爱好者导航栏样式 */
.navbar.amateur-theme {
  .el-menu.el-menu--horizontal {
    .el-menu-item {
      font-family: "Indie Flower", cursive !important;
      font-size: 1.2rem !important;
      font-weight: 600 !important;
      letter-spacing: 0.5px !important;
      position: relative !important;
      overflow: visible !important;
      transition: transform 0.3s ease !important;
      padding: 0 20px !important;
      height: 64px !important;
      line-height: 64px !important;

      /* 图标样式 */
      .el-icon-s-home,
      .el-icon-s-cooperation,
      .el-icon-picture,
      .el-icon-view,
      .el-icon-discover {
        font-size: 1.5rem !important;
        margin-right: 8px !important;
        position: relative !important;
        display: inline-block !important;
        vertical-align: middle !important;
        transition: transform 0.3s ease !important;
      }

      /* 小鱼图标 */
      .el-icon-s-home::before {
        content: "🐠" !important;
      }

      /* 海星图标 */
      .el-icon-s-cooperation::before {
        content: "⭐" !important;
      }

      /* 相机图标 */
      .el-icon-picture::before {
        content: "📸" !important;
      }

      /* 鱼眼图标 */
      .el-icon-view::before {
        content: "🐟" !important;
      }

      /* 海星图标 */
      .el-icon-discover::before {
        content: "🌟" !important;
      }

      /* 悬浮效果 */
      &:hover {
        transform: translateY(-2px) !important;
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: #0a4d68 !important;

        i {
          animation: wiggle 0.5s ease-in-out !important;
        }
      }

      /* 选中状态 */
      &.is-active {
        color: #0a4d68 !important;
        font-weight: 700 !important;
        background-color: rgba(255, 255, 255, 0.2) !important;

        &::after {
          content: "" !important;
          position: absolute !important;
          bottom: 0 !important;
          left: 15% !important;
          width: 70% !important;
          height: 3px !important;
          background: linear-gradient(90deg, #05bfdb, #088395) !important;
          border-radius: 3px !important;
        }

        i {
          color: #0a4d68 !important;
          transform: scale(1.1) !important;
        }
      }
    }
  }
}

/* 图标动画 */
@keyframes wiggle {
  0%,
  100% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(-10deg);
  }
  75% {
    transform: rotate(10deg);
  }
}
</style>
