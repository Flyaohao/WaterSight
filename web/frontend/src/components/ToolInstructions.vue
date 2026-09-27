<template>
  <div class="tool-instructions" :class="{ expanded: isExpanded }">
    <div class="instruction-toggle" @click="toggleExpand">
      <i :class="isExpanded ? 'el-icon-close' : 'el-icon-document'"></i>
      <span>{{ isExpanded ? "关闭说明" : "查看说明" }}</span>
    </div>
    <div class="instruction-content" v-if="isExpanded">
      <h2>{{ title }}</h2>

      <div class="section">
        <h3>功能介绍</h3>
        <p>{{ description }}</p>
        <ul class="feature-list" v-if="features.length > 0">
          <li v-for="(feature, index) in features" :key="index">
            {{ feature }}
          </li>
        </ul>
      </div>

      <div class="section">
        <h3>使用指南</h3>
        <div class="guide-section">
          <h4>支持格式</h4>
          <ul>
            <li v-for="(format, index) in formats" :key="index">
              {{ format }}
            </li>
          </ul>
        </div>

        <div class="guide-section">
          <h4>使用步骤</h4>
          <ol>
            <li v-for="(step, index) in steps" :key="index">{{ step }}</li>
          </ol>
        </div>

        <div class="guide-section">
          <h4>注意事项</h4>
          <ul>
            <li v-for="(note, index) in notes" :key="index">{{ note }}</li>
          </ul>
        </div>
      </div>

      <div class="section" v-if="advantages.length > 0">
        <h3>技术优势</h3>
        <div
          v-for="(advantage, index) in advantages"
          :key="index"
          class="advantage-item"
        >
          <h4>{{ advantage.title }}</h4>
          <p>{{ advantage.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ToolInstructions",
  props: {
    title: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: true,
    },
    features: {
      type: Array,
      default: () => [],
    },
    formats: {
      type: Array,
      default: () => [],
    },
    steps: {
      type: Array,
      default: () => [],
    },
    notes: {
      type: Array,
      default: () => [],
    },
    advantages: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      isExpanded: false,
    };
  },
  methods: {
    toggleExpand() {
      this.isExpanded = !this.isExpanded;
    },
  },
};
</script>

<style lang="less" scoped>
.tool-instructions {
  position: fixed;
  top: 80px;
  left: 0;
  z-index: 100;
  transition: all 0.3s ease;
}

.instruction-toggle {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  background: linear-gradient(
    135deg,
    var(--primary-color, #0a4d68),
    var(--secondary-color, #088395)
  );
  color: var(--text-color-inverse, white);
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;

  &:hover {
    transform: translateX(5px);
  }

  i {
    margin-right: 8px;
  }
}

.expanded .instruction-toggle {
  border-radius: 0 4px 0 0;
}

.instruction-content {
  width: 360px;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
  background: var(--bg-color, white);
  padding: 20px;
  border-radius: 0 0 4px 0;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);

  h2 {
    color: var(--primary-color, #0a4d68);
    border-bottom: 2px solid var(--secondary-color, #088395);
    padding-bottom: 10px;
    margin-top: 0;
  }

  h3 {
    color: var(--secondary-color, #088395);
    margin-top: 20px;
  }

  h4 {
    color: var(--primary-color, #0a4d68);
    margin: 15px 0 10px;
  }

  p {
    line-height: 1.6;
  }

  ul,
  ol {
    padding-left: 20px;
    margin: 10px 0;

    li {
      margin-bottom: 8px;
      line-height: 1.5;
    }
  }

  .feature-list {
    list-style-type: disc;
  }

  .section {
    margin-bottom: 25px;
  }

  .guide-section {
    margin-bottom: 20px;
  }

  .advantage-item {
    margin-bottom: 15px;

    h4 {
      margin-bottom: 5px;
      color: var(--secondary-color, #088395);
    }

    p {
      margin-top: 0;
    }
  }
}

// Styling for scrollbar
.instruction-content::-webkit-scrollbar {
  width: 6px;
}

.instruction-content::-webkit-scrollbar-track {
  background: var(--scrollbar-track-color, #f1f1f1);
}

.instruction-content::-webkit-scrollbar-thumb {
  background: var(--primary-color, #0a4d68);
  border-radius: 3px;
}

.instruction-content::-webkit-scrollbar-thumb:hover {
  background: var(--secondary-color, #088395);
}

:root[theme="dark"] {
  .tool-instructions {
    .instruction-content {
      background: var(--bg-color-dark, #1a1a1a);
      box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
    }
  }
}
</style>
