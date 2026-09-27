<template>
  <div class="resources-container">
    <!-- 学习工具板块 -->
    <h2 class="section-title">学习工具</h2>

    <!-- 编程开发工具 -->
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span class="category-title">编程开发工具</span>
        <el-tag size="small" effect="plain">基础开发</el-tag>
      </div>
      <div class="tool-list">
        <el-row :gutter="20">
          <el-col :span="8" v-for="tool in programmingTools" :key="tool.id">
            <el-card class="tool-card" shadow="hover">
              <div class="tool-title">
                <i
                  v-if="tool.icon.startsWith('el-icon')"
                  :class="tool.icon"
                  class="tool-icon"
                ></i>
                <img
                  v-else
                  :src="tool.icon"
                  class="tool-icon"
                  @error="handleImageError($event)"
                />
                <h3>{{ tool.name }}</h3>
              </div>
              <p class="tool-desc">{{ tool.description }}</p>
              <div class="tool-links">
                <el-button
                  type="primary"
                  size="small"
                  @click="openUrl(tool.url)"
                  >访问官网</el-button
                >
                <el-button
                  type="success"
                  size="small"
                  @click="openUrl(tool.tutorial)"
                  >使用教程</el-button
                >
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <!-- 数据分析工具 -->
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span class="category-title">数据分析工具</span>
        <el-tag size="small" effect="plain">数据处理</el-tag>
      </div>
      <div class="tool-list">
        <el-row :gutter="20">
          <el-col :span="8" v-for="tool in dataTools" :key="tool.id">
            <el-card class="tool-card" shadow="hover">
              <div class="tool-title">
                <i
                  v-if="tool.icon.startsWith('el-icon')"
                  :class="tool.icon"
                  class="tool-icon"
                ></i>
                <img
                  v-else
                  :src="tool.icon"
                  class="tool-icon"
                  @error="handleImageError($event)"
                />
                <h3>{{ tool.name }}</h3>
              </div>
              <p class="tool-desc">{{ tool.description }}</p>
              <div class="tool-links">
                <el-button
                  type="primary"
                  size="small"
                  @click="openUrl(tool.url)"
                  >访问官网</el-button
                >
                <el-button
                  type="success"
                  size="small"
                  @click="openUrl(tool.tutorial)"
                  >使用教程</el-button
                >
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <!-- 水下探测工具 -->
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span class="category-title">水下探测工具</span>
        <el-tag size="small" effect="plain">专业软件</el-tag>
      </div>
      <div class="tool-list">
        <el-row :gutter="20">
          <el-col :span="8" v-for="tool in detectionTools" :key="tool.id">
            <el-card class="tool-card" shadow="hover">
              <div class="tool-title">
                <i
                  v-if="tool.icon.startsWith('el-icon')"
                  :class="tool.icon"
                  class="tool-icon"
                ></i>
                <img
                  v-else
                  :src="tool.icon"
                  class="tool-icon"
                  @error="handleImageError($event)"
                />
                <h3>{{ tool.name }}</h3>
              </div>
              <p class="tool-desc">{{ tool.description }}</p>
              <div class="tool-links">
                <el-button
                  type="primary"
                  size="small"
                  @click="openUrl(tool.url)"
                  >访问官网</el-button
                >
                <el-button
                  type="success"
                  size="small"
                  @click="openUrl(tool.tutorial)"
                  >使用教程</el-button
                >
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <!-- 地理信息工具 -->
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span class="category-title">地理信息工具</span>
        <el-tag size="small" effect="plain">GIS应用</el-tag>
      </div>
      <div class="tool-list">
        <el-row :gutter="20">
          <el-col :span="8" v-for="tool in gisTools" :key="tool.id">
            <el-card class="tool-card" shadow="hover">
              <div class="tool-title">
                <i
                  v-if="tool.icon.startsWith('el-icon')"
                  :class="tool.icon"
                  class="tool-icon"
                ></i>
                <img
                  v-else
                  :src="tool.icon"
                  class="tool-icon"
                  @error="handleImageError($event)"
                />
                <h3>{{ tool.name }}</h3>
              </div>
              <p class="tool-desc">{{ tool.description }}</p>
              <div class="tool-links">
                <el-button
                  type="primary"
                  size="small"
                  @click="openUrl(tool.url)"
                  >访问官网</el-button
                >
                <el-button
                  type="success"
                  size="small"
                  @click="openUrl(tool.tutorial)"
                  >使用教程</el-button
                >
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <!-- 友情链接板块 -->
    <h2 class="section-title">友情链接</h2>

    <!-- 科研机构 -->
    <el-card class="box-card friend-links">
      <div slot="header" class="clearfix">
        <span class="category-title">科研机构</span>
      </div>
      <div class="link-list">
        <el-row :gutter="20">
          <el-col :span="6" v-for="link in researchLinks" :key="link.id">
            <el-link :href="link.url" target="_blank" :underline="false">
              {{ link.name }}
            </el-link>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <!-- 学习平台 -->
    <el-card class="box-card friend-links">
      <div slot="header" class="clearfix">
        <span class="category-title">学习平台</span>
      </div>
      <div class="link-list">
        <el-row :gutter="20">
          <el-col :span="6" v-for="link in educationLinks" :key="link.id">
            <el-link :href="link.url" target="_blank" :underline="false">
              {{ link.name }}
            </el-link>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <!-- 技术社区 -->
    <el-card class="box-card friend-links">
      <div slot="header" class="clearfix">
        <span class="category-title">技术社区</span>
      </div>
      <div class="link-list">
        <el-row :gutter="20">
          <el-col :span="6" v-for="link in communityLinks" :key="link.id">
            <el-link :href="link.url" target="_blank" :underline="false">
              {{ link.name }}
            </el-link>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "Resources",
  data() {
    return {
      defaultIcon:
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsTAAALEwEAmpwYAAABYklEQVR4nO2XTU7DMBBGn1BXLCvYcADOwZodJ+AQXIBzcAJOwLpbVhyAHbCFDQtQJCSQEPqDRJQQO3bGbhOJSn1SV7E9M+/LxHYCf10AQ2AGTIB34Av4BN6AJ+AeGADFf4EPKWQF/JjEV8A9cAZkuwKfU8CbQXQJXALHcQIHwDVFnAIXQC8UfELRbwbhZ+AkFHxIEXOD+D1QDwHvAUuD+BdwFgJ+ThGfBvFHoLZr+BFF3BnEP4BGjPgdRbwaxGdAPUZ8QBFzg/hTjHiDIpYG8dEu4EOKeDGIL4BajPgJRbwZxO+BWox4nyLmBvFnoBEjfkcRrwbxEVCPEe9RxNIgPt4FvEkRLwbxBXAUI95k+xK+A7UY8T5FzA3iz0AzRvyOIl4N4iOgESPepYilQXyyC3iTIl4M4gvgOEa8yfYlfAfUYsT7FDE3iH8AzRjxO4p4NYiPgEaM+F/XN9C+2zWLJMmwAAAAAElFTkSuQmCC",
      programmingTools: [
        {
          id: 1,
          name: "Python",
          icon: "https://www.python.org/static/favicon.ico",
          description:
            "数据科学和机器学习首选语言，常用于水下图像处理和声学数据分析",
          url: "https://www.python.org/",
          tutorial: "https://www.runoob.com/python3/python3-tutorial.html",
        },
        {
          id: 2,
          name: "MATLAB",
          icon: "https://www.mathworks.com/favicon.ico",
          description: "科学计算软件，广泛应用于水下声学信号处理",
          url: "https://www.mathworks.com/products/matlab.html",
          tutorial: "https://www.bilibili.com/video/BV1Db4y1m7Ho/",
        },
        {
          id: 3,
          name: "Visual Studio Code",
          icon: "https://code.visualstudio.com/favicon.ico",
          description: "轻量级代码编辑器，支持多种编程语言和插件",
          url: "https://code.visualstudio.com/",
          tutorial: "https://www.runoob.com/w3cnote/vscode-tutorial.html",
        },
      ],
      dataTools: [
        {
          id: 1,
          name: "Jupyter Notebook",
          icon: "https://jupyter.org/favicon.ico",
          description: "交互式数据分析工具，支持实时数据可视化",
          url: "https://jupyter.org/",
          tutorial:
            "https://www.runoob.com/w3cnote/jupyter-notebook-tutorial.html",
        },
        {
          id: 2,
          name: "ParaView",
          icon: "https://www.paraview.org/favicon.ico",
          description: "海洋数据可视化和分析工具",
          url: "https://www.paraview.org/",
          tutorial:
            "https://blog.csdn.net/qq_40259641/article/details/106959063",
        },
        {
          id: 3,
          name: "Origin",
          icon: "https://www.originlab.com/favicon.ico",
          description: "专业的数据分析绘图软件",
          url: "https://www.originlab.com/",
          tutorial: "https://www.bilibili.com/video/BV1Yb411J7n3/",
        },
      ],
      detectionTools: [
        {
          id: 1,
          name: "Kongsberg Maritime",
          icon: "el-icon-monitor",
          description: "水下声呐系统及数据处理软件",
          url: "https://www.kongsberg.com/maritime/",
          tutorial:
            "https://www.kongsberg.com/maritime/support/software-downloads/",
        },
        {
          id: 2,
          name: "Tritech Gemini",
          icon: "el-icon-view",
          description: "多波束声呐成像软件",
          url: "https://www.tritech.co.uk/",
          tutorial: "https://www.tritech.co.uk/support-software",
        },
        {
          id: 3,
          name: "Coda Octopus",
          icon: "el-icon-data-analysis",
          description: "水下测绘和声学成像软件",
          url: "https://www.codaoctopus.com/",
          tutorial: "https://www.codaoctopus.com/support/training",
        },
      ],
      gisTools: [
        {
          id: 1,
          name: "ArcGIS",
          icon: "https://www.arcgis.com/favicon.ico",
          description: "专业GIS软件，用于海洋地理数据处理和制图",
          url: "https://www.arcgis.com/",
          tutorial: "https://www.bilibili.com/video/BV1ZE411F7RN/",
        },
        {
          id: 2,
          name: "QGIS",
          icon: "https://www.qgis.org/favicon.ico",
          description: "开源地理信息系统软件",
          url: "https://www.qgis.org/",
          tutorial: "https://www.osgeo.cn/qgis-tutorial/",
        },
        {
          id: 3,
          name: "Global Mapper",
          icon: "https://www.bluemarblegeo.com/favicon.ico",
          description: "地理空间数据处理和分析软件",
          url: "https://www.bluemarblegeo.com/global-mapper/",
          tutorial: "https://www.bluemarblegeo.com/knowledgebase/",
        },
      ],
      researchLinks: [
        {
          id: 1,
          name: "中国海洋信息网",
          url: "http://www.nmdis.org.cn/",
          description: "国家海洋信息中心官方网站",
        },
        {
          id: 2,
          name: "中国水产科学研究院",
          url: "https://www.cafs.ac.cn/",
          description: "国家级水产研究机构",
        },
        {
          id: 3,
          name: "中国科学院海洋研究所",
          url: "http://www.qdio.cas.cn/",
          description: "中科院海洋研究重点机构",
        },
        {
          id: 4,
          name: "水声工程网",
          url: "http://www.acoustics.org.cn/",
          description: "水声工程专业网站",
        },
      ],
      educationLinks: [
        {
          id: 1,
          name: "菜鸟教程",
          url: "https://www.runoob.com/",
          description: "基础编程教程网站",
        },
        {
          id: 2,
          name: "B站教程",
          url: "https://www.bilibili.com/v/knowledge",
          description: "视频教学平台",
        },
        {
          id: 3,
          name: "W3School",
          url: "https://www.w3school.com.cn/",
          description: "Web技术教程",
        },
      ],
      communityLinks: [
        {
          id: 1,
          name: "CSDN",
          url: "https://www.csdn.net/",
          description: "综合性技术社区",
        },
        {
          id: 2,
          name: "掘金",
          url: "https://juejin.cn/",
          description: "高质量技术社区",
        },
        {
          id: 3,
          name: "GitHub海洋科学专题",
          url: "https://github.com/topics/ocean-science",
          description: "开源代码平台",
        },
        {
          id: 4,
          name: "ResearchGate",
          url: "https://www.researchgate.net/",
          description: "科研社交平台",
        },
      ],
    };
  },
  methods: {
    openUrl(url) {
      window.open(url, "_blank");
    },
    handleImageError(event) {
      event.target.src = this.defaultIcon;
    },
  },
};
</script>

<style scoped>
/* 预加载字体 */
@font-face {
  font-family: "element-icons";
  src: url("~element-ui/lib/theme-chalk/fonts/element-icons.woff")
      format("woff"),
    url("~element-ui/lib/theme-chalk/fonts/element-icons.ttf")
      format("truetype");
  font-weight: normal;
  font-style: normal;
  font-display: swap; /* 使用 swap 策略加快显示 */
}

/* 整体容器样式 */
.resources-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: var(--bg-color);
  min-height: calc(100vh - 60px);
}

/* 添加海洋波浪效果 */
.resources-container::before {
  content: "";
  position: fixed;
  top: 0;
  left: 165px;
  right: 165px;
  bottom: 50%;
  background: radial-gradient(
      circle at 90% 10%,
      rgba(79, 172, 254, 0.1) 0%,
      transparent 40%
    ),
    radial-gradient(
      circle at 10% 90%,
      rgba(0, 242, 254, 0.1) 0%,
      transparent 40%
    ),
    linear-gradient(45deg, rgba(240, 247, 255, 0.2) 25%, transparent 25%) -50px 0,
    linear-gradient(45deg, rgba(240, 247, 255, 0.2) 25%, transparent 25%) 0 0,
    linear-gradient(135deg, rgba(240, 247, 255, 0.2) 25%, transparent 25%) 0 0,
    linear-gradient(135deg, rgba(240, 247, 255, 0.2) 25%, transparent 25%) -50px
      0;
  background-size: 100px 100px;
  pointer-events: none;
  z-index: -999;
  animation: wave 20s infinite linear;
}

@keyframes wave {
  0% {
    background-position: 0% 0%;
  }
  100% {
    background-position: 100% 100%;
  }
}

/* 主要标题样式 - 添加装饰元素 */
.section-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-color-primary);
  margin: 30px 0 20px;
  padding-left: 15px;
  border-left: 4px solid var(--primary-color);
}

.section-title::before {
  content: "🌊"; /* 使用海浪emoji作为装饰 */
  margin-right: 15px;
  font-size: 28px;
}

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 卡片样式优化 */
.box-card {
  margin-bottom: 30px;
  background-color: var(--bg-color-secondary);
  border: 1px solid var(--border-color);
  box-shadow: var(--card-shadow);
  transition: all 0.3s ease;
}

.box-card:hover {
  box-shadow: var(--card-shadow-hover);
}

.box-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 卡片头部样式 */
.box-card .el-card__header {
  padding: 15px 20px;
  border-bottom: 1px solid var(--border-color);
  background-color: var(--bg-color-secondary);
}

/* 工具卡片内容布局优化 */
.tool-card {
  height: 100%;
  background-color: var(--bg-color-tertiary);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.tool-card:hover {
  transform: translateY(-5px);
  border-color: var(--primary-color);
  box-shadow: var(--card-shadow-hover);
}

.tool-card::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s ease;
}

.tool-card:hover::after {
  transform: scaleX(1);
}

/* 工具标题样式 */
.tool-title {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.tool-title .tool-icon {
  width: 32px;
  height: 32px;
  margin-right: 10px;
  color: var(--primary-color);
  font-size: 24px;
}

.tool-title h3 {
  margin: 0;
  font-size: 16px;
  color: var(--text-color-primary);
  font-weight: 500;
}

.tool-icon {
  width: 40px;
  height: 40px;
  padding: 6px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.5s ease;
  object-fit: contain;
}

.tool-card:hover .tool-icon {
  transform: rotate(360deg);
  box-shadow: 0 6px 15px rgba(79, 172, 254, 0.2);
}

/* 工具描述样式 */
.tool-desc {
  color: var(--text-color-regular);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 20px;
  min-height: 44px;
}

/* 工具链接样式 */
.tool-links {
  display: flex;
  gap: 10px;
}

/* 按钮样式 - 添加渐变效果 */
.tool-links .el-button--primary {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.tool-links .el-button--primary:hover,
.tool-links .el-button--primary:focus {
  background-color: var(--primary-color-hover);
  border-color: var(--primary-color-hover);
}

.tool-links .el-button--success {
  background-color: var(--success-color);
  border-color: var(--success-color);
}

.tool-links .el-button--success:hover,
.tool-links .el-button--success:focus {
  background-color: var(--success-color-hover);
  border-color: var(--success-color-hover);
}

.tool-links .el-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

/* 友情链接样式 - 添加悬停效果 */
.friend-links {
  margin-bottom: 30px;
  background-color: var(--bg-color-secondary);
  border: 1px solid var(--border-color);
}

.friend-links .el-link {
  display: block;
  padding: 10px;
  color: var(--text-color-regular);
  transition: all 0.3s;
  border-radius: 4px;
}

.friend-links .el-link:hover {
  color: var(--primary-color);
  background-color: var(--bg-color-hover);
}

.friend-links .el-link::before {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 3px;
  background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
  transition: width 0.3s ease;
}

.friend-links .el-link:hover::before {
  width: 100%;
}

/* 标签样式优化 */
.el-tag {
  background-color: var(--primary-color-light);
  border-color: var(--primary-color-light);
  color: var(--primary-color);
}

/* 分类标题装饰 */
.category-title {
  font-size: 18px;
  font-weight: 500;
  color: var(--text-color-primary);
}

.category-title::before {
  content: "⚓";
  position: absolute;
  left: 0;
  font-size: 16px;
}

/* 工具列表布局优化 */
.tool-list {
  margin-top: 20px;
}

.tool-list .el-row {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -10px;
}

.tool-list .el-col {
  padding: 10px;
  display: flex;
}

.tool-list .el-col-8 {
  width: 33.33%;
}

/* 友情链接布局优化 */
.link-list {
  padding: 15px;
}

.link-list .el-row {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -8px;
}

.link-list .el-col {
  padding: 8px;
}

.link-list .el-col-6 {
  width: 25%;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .resources-container {
    padding: 25px;
    max-width: 100%;
  }

  .box-card {
    max-width: 100%;
  }

  .tool-list .el-col-8 {
    width: 33.33%;
  }

  .link-list .el-col-6 {
    width: 25%;
  }
}

@media (max-width: 992px) {
  .resources-container {
    padding: 25px;
  }

  .section-title {
    font-size: 24px;
    padding: 15px 25px;
  }

  .section-title::before {
    font-size: 24px;
  }

  .tool-list .el-col-8 {
    width: 50%;
  }

  .link-list .el-col-6 {
    width: 33.33%;
  }
}

@media (max-width: 768px) {
  .resources-container {
    padding: 15px;
  }

  .section-title {
    font-size: 20px;
    margin: 20px 0 15px;
  }

  .tool-list .el-col-8 {
    width: 100%;
  }

  .link-list .el-col-6 {
    width: 50%;
  }

  .tool-links {
    flex-direction: column;
  }

  .tool-links .el-button {
    width: 100%;
    margin-left: 0 !important;
    margin-top: 8px;
  }

  .tool-links .el-button:first-child {
    margin-top: 0;
  }
}

@media (max-width: 480px) {
  .link-list .el-col-6 {
    width: 100%;
  }
}
</style>
