<template>
  <div class="researcher-home">
    <div class="background-wrapper"></div>
    <div class="background-overlay"></div>
    <div class="grid-container">
      <div
        class="grid-item dataset"
        @click="navigateTo('/datasetPreprocessing')"
      >
        <i class="el-icon-folder"></i>
        <h3>数据集生成</h3>
        <p>水下模拟数据集生成</p>
        <span class="item-label">Dataset</span>
      </div>

      <div class="grid-item enhance" @click="navigateTo('/enhance')">
        <i class="el-icon-picture"></i>
        <h3>图像增强</h3>
        <p>水下图像增强系统</p>
        <span class="item-label">Enhancement</span>
      </div>

      <div class="grid-item fish" @click="navigateTo('/coralyolo')">
        <i class="el-icon-dish"></i>
        <h3>珊瑚健康监测</h3>
        <p>珊瑚礁健康监测系统</p>
        <span class="item-label">Coral Health</span>
      </div>

      <div class="grid-item starfish" @click="navigateTo('/resources')">
        <i class="el-icon-star-on"></i>
        <h3>研究资源</h3>
        <p>水下领域学习途径</p>
        <span class="item-label">Resources</span>
      </div>

      <div class="grid-item forum" @click="navigateTo('/home')">
        <i class="el-icon-chat-dot-round"></i>
        <h3>交流中心</h3>
        <p>与其他研究者交流</p>
        <span class="item-label">Forum</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ReSearcherHome",
  data() {
    return {
      searchQuery: "",
      particles: [],
      particleCount: 20,
    };
  },
  mounted() {
    document.body.style.backgroundColor = "#0077B6";
    document.body.classList.add("researcher-page");
    this.createParticles();
  },
  beforeDestroy() {
    document.body.style.backgroundColor = "";
    document.body.classList.remove("researcher-page");
    this.clearParticles();
  },
  methods: {
    createParticles() {
      const container = this.$refs.particlesContainer;
      if (!container) return;

      for (let i = 0; i < this.particleCount; i++) {
        const particle = document.createElement("div");
        particle.className = "particle";
        particle.style.left = Math.random() * 100 + "%";
        particle.style.animationDuration = Math.random() * 3 + 2 + "s";
        particle.style.animationDelay = Math.random() * 2 + "s";
        container.appendChild(particle);
        this.particles.push(particle);
      }
    },
    clearParticles() {
      this.particles.forEach((particle) => {
        particle.remove();
      });
      this.particles = [];
    },
    navigateTo(path) {
      this.$router.push({ path: `/front${path}` });
    },
    handleSearch() {
      if (this.searchQuery.trim()) {
        this.$router.push({
          path: "/front/search",
          query: { q: this.searchQuery },
        });
      }
    },
  },
};
</script>

<style lang="less" scoped>
// 主色系
@primary-blue: #2b6cb0; // 深海蓝
@hover-blue: #3b82f6; // 动态蓝（悬停状态）
@accent-teal: #2c7a7b; // 水族绿

// 中性色
@background: #d9e8ff; // 主背景（替换原#e2e8f0）
@card-bg: rgba(255, 255, 255, 0.95); // 卡片（带轻微透明度的白）
@text-primary: #1e293b; // 主文字
@text-secondary: #64748b; // 辅助文字

// 功能色
@border-color: #e2e8f0; // 边框色
/* 全局样式覆盖 */
:global(.researcher-page) {
  position: relative;
  min-height: 100vh;
}

.researcher-home {
  padding: 20px 40px;
  max-width: 1150px;
  margin: 20px auto;
  position: relative;
  z-index: 2;
  height: calc(55vh); /* 减少留白，使用视口高度 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: var(--bg-color);
  color: var(--text-color-primary);
}

/* 背景和遮罩层 */
.background-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url("../../assets/imgs/underwater.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    z-index: 0;
    opacity: 0.8;
  }

  &::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      135deg,
      var(--bg-gradient-light) 0%,
      var(--bg-gradient-dark) 100%
    );
    z-index: 1;
  }
}

.background-overlay {
  position: absolute;
  border-radius: 18px;
  top: 38px;
  left: 0;
  right: 0;
  bottom: -240px;
  background: var(--bg-color-alpha) !important;
  z-index: 1;
  backdrop-filter: blur(5px);
  opacity: 0.92;
}

.grid-container {
  display: grid;
  grid-template-columns: 2fr 1fr 1.5fr;
  grid-template-rows: 325px 175px; /* 调整为500px总高度，65%和35%的比例 */
  gap: 20px;
  grid-template-areas:
    "dataset enhance forum"
    "fish starfish forum";
  position: relative;
  z-index: 10;
  margin: 0 auto;
  width: 100%;
  bottom: -140px;
}

.grid-item {
  background: var(--bg-color-secondary);
  border: 1px solid var(--border-color);
  backdrop-filter: blur(5px);
  border-radius: 12px;
  padding: 30px;
  text-align: center;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: var(--card-shadow);

  &:hover {
    transform: translateY(-5px);
    background: var(--bg-color-hover);
    box-shadow: var(--shadow-color-hover);
    border-color: var(--primary-color);
  }

  i {
    font-size: 48px;
    width: 48px;
    height: 48px;
    line-height: 48px;
    margin-bottom: 20px; /* 调整图标下边距 */
    color: var(--text-color-secondary);
    transition: all 0.3s ease;
  }

  &:hover i {
    color: var(--primary-color);
  }

  h3 {
    margin: 10px 0 5px; /* 调整标题边距 */
    font-size: 18px;
    color: var(--text-color-primary);
    font-weight: 600;
    letter-spacing: 0.5px;
  }

  p {
    color: var(--text-color-secondary);
    font-size: 14px;
    margin: 0;
    font-weight: 400;
    line-height: 1.4; /* 调整行高 */
  }
}

.item-label {
  position: absolute;
  bottom: 12px;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 10px;
  font-weight: 200;
  color: var(--text-color-secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* 为每个板块设置不同的样式 */
.dataset,
.enhance,
.fish,
.starfish {
  background-color: var(--bg-color-secondary);
  border-top: 2px solid var(--border-color);
}

.forum {
  height: 540px;
  grid-area: forum;
  grid-row: 1 / -1;
  background-color: var(--bg-color-secondary);
  border-top: 2px solid var(--primary-color);

  i {
    color: var(--primary-color);
    &:hover {
      color: var(--primary-color);
      opacity: 0.8;
    }
  }
}

.dataset {
  height: 325px; /* 65% of 500px */
  display: flex;
  flex-direction: column;
  justify-content: center;

  i {
    margin-bottom: 25px;
  }

  h3 {
    margin: 15px 0 8px;
  }
}

.enhance {
  height: 300px; /* 55% of 500px */
  display: flex;
  flex-direction: column;
  justify-content: center;

  i {
    margin-bottom: 22px;
  }

  h3 {
    margin: 12px 0 6px;
  }
}

.fish {
  height: 195px; /* 35% of 500px */
  display: flex;
  flex-direction: column;
  justify-content: center;

  i {
    margin-bottom: 15px;
  }

  h3 {
    margin: 8px 0 4px;
  }
}

.starfish {
  margin-top: -25px;
  height: 220px; /* 45% of 500px */
  display: flex;
  flex-direction: column;
  justify-content: center;

  i {
    margin-bottom: 18px;
  }

  h3 {
    margin: 10px 0 5px;
  }
}

/* 响应式布局调整 */
@media (max-width: 1200px) {
  .grid-container {
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: auto auto auto;
    grid-template-areas:
      "dataset enhance"
      "fish starfish"
      "forum forum";
  }

  .dataset {
    min-height: 300px;
  }

  .enhance {
    min-height: 250px;
  }

  .fish {
    min-height: 160px;
  }

  .starfish {
    min-height: 200px;
  }
}

@media (max-width: 768px) {
  .researcher-home {
    padding: 20px;
    margin: 20px auto;
  }

  .grid-container {
    grid-template-columns: 1fr;
    grid-template-areas:
      "dataset"
      "enhance"
      "fish"
      "starfish"
      "forum";
    gap: 15px;
  }

  .grid-item {
    padding: 20px;
  }

  .dataset {
    min-height: 250px;
  }

  .enhance {
    min-height: 220px;
  }

  .fish {
    min-height: 140px;
  }

  .starfish {
    min-height: 180px;
  }
}
</style>
