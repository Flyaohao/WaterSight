<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
  created() {
    // 初始化主题
    this.$store.dispatch("initTheme");
  },
  watch: {
    "$store.state.theme": {
      handler(newTheme) {
        if (newTheme === "dark") {
          document.body.classList.add("dark");
        } else {
          document.body.classList.remove("dark");
        }
      },
      immediate: true,
    },
  },
};
</script>

<style lang="less">
/* 导入字体 */
@import url("https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@300;400;500&display=swap");

/* 全局重置菜单样式 */
.el-menu--horizontal > .el-menu-item {
  height: 64px !important;
  line-height: 64px !important;
}

/* 业余爱好者导航栏样式 */
.amateur-theme {
  .el-menu--horizontal {
    background: transparent !important;
    border-bottom: none !important;

    & > .el-menu-item {
      font-family: "Josefin Sans", sans-serif !important;
      font-size: 0.95rem !important;
      font-weight: 400 !important;
      letter-spacing: 0.4px !important;
      padding: 0 20px !important;
      color: #2c3e50 !important;
      transition: all 0.3s ease !important;

      i {
        font-size: 1.2rem !important;
        margin-right: 6px !important;
        color: inherit !important;
        transition: transform 0.3s ease !important;
      }

      /* 图标替换 */
      .el-icon-s-cooperation::before {
        content: "🌊" !important;
      } /* 活动用海浪 */
      .el-icon-picture::before {
        content: "✨" !important;
      } /* 图像处理保持星光 */
      .el-icon-view::before {
        content: "🐠" !important;
      } /* 鱼儿识别用热带鱼 */
      .el-icon-discover::before {
        content: "⭐️" !important;
      } /* 海星识别用星星 */

      /* 悬浮效果 */
      &:hover {
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: #0a4d68 !important;
        transform: translateY(-2px);

        i {
          animation: menuIconWiggle 0.5s ease-in-out;
        }
      }

      /* 选中状态 */
      &.is-active {
        background-color: rgba(255, 255, 255, 0.2) !important;
        color: #0a4d68 !important;
        font-weight: 500 !important;
        border-bottom: 2px solid #088395 !important;

        i {
          transform: scale(1.1);
        }
      }
    }
  }
}

/* 图标动画 */
@keyframes menuIconWiggle {
  0%,
  100% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(-8deg);
  }
  75% {
    transform: rotate(8deg);
  }
}

#app {
  font-family: "Josefin Sans", Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100%;
}
</style>
