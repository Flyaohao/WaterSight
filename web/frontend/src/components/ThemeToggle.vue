<template>
  <div
    class="theme-toggle"
    @click="toggleTheme"
    :title="isDarkTheme ? '切换到白天模式' : '切换到黑夜模式'"
  >
    <transition name="theme-icon" mode="out-in">
      <i
        :class="isDarkTheme ? 'el-icon-sunny' : 'el-icon-moon'"
        :key="isDarkTheme"
      ></i>
    </transition>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "ThemeToggle",
  computed: {
    ...mapGetters(["isDarkTheme"]),
  },
  methods: {
    ...mapActions(["toggleTheme"]),
  },
  created() {
    // 初始化主题
    this.$store.dispatch("initTheme");
  },
};
</script>

<style lang="less" scoped>
.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  margin-right: 15px;
  background: var(--theme-toggle-bg, rgba(255, 255, 255, 0.2));
  color: var(--theme-toggle-color, #fff);
  position: relative;
  overflow: hidden;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(
      circle,
      transparent 10%,
      rgba(255, 255, 255, 0.1) 10.5%
    );
    transform: scale(5);
    opacity: 0;
    transition: transform 0.5s, opacity 0.6s;
  }

  &:hover {
    background: var(--theme-toggle-hover-bg, rgba(255, 255, 255, 0.3));
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);

    &::before {
      transform: scale(1);
      opacity: 1;
    }
  }

  &:active {
    transform: translateY(0);
  }

  i {
    font-size: 20px;
    filter: drop-shadow(0 1px 1px rgba(0, 0, 0, 0.2));
  }
}

.theme-icon-enter-active,
.theme-icon-leave-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.theme-icon-enter {
  opacity: 0;
  transform: rotate(-45deg) scale(0.7);
}

.theme-icon-leave-to {
  opacity: 0;
  transform: rotate(45deg) scale(0.7);
}

/* 暗色主题特殊样式 */
:global(.dark) .theme-toggle {
  background: var(--theme-toggle-bg-dark, rgba(255, 255, 255, 0.1));
  color: var(--theme-toggle-color-dark, rgba(255, 255, 255, 0.9));
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);

  &:hover {
    background: var(--theme-toggle-hover-bg-dark, rgba(255, 255, 255, 0.15));
  }

  i {
    filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.3));
  }
}
</style>
