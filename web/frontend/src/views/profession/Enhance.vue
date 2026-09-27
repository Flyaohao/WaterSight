<template>
  <div class="enhance-container">
    <DemoVideoButton video-url="enhance.mp4" />
    <tool-instructions
        title="水下图像增强系统"
        description="创新性集成深度学习与传统图像处理两大技术体系的水下图像增强系统。标准模式采用端到端深度学习模型，通过注意力机制和多尺度特征融合实现最优增强效果；快速模式基于改进的多阶段串联优化，结合暗通道去雾、自适应白平衡等算法提供高效处理。支持图片和视频的双模式处理，满足不同场景需求。"
        :features="[
          '双模式技术：深度学习模式效果最优，传统算法模式速度更快',
          '深度学习：端到端模型、注意力机制、多尺度特征融合、对比学习',
          '快速处理：暗通道去雾、LAB白平衡、对比度优化、USM锐化',
          '全面支持：支持图片和视频文件的实时增强处理'
        ]"
        :formats="[
          '图片格式：JPG、PNG（≤20MB）',
          '视频格式：MP4（≤100MB）',
          '分辨率：建议不超过2048x2048',
          '处理时间：标准模式8-10秒/张，快速模式3-5秒/张'
        ]"
        :steps="[
          '上传文件：选择需要增强的图片或视频文件',
          '选择模式：根据需求选择标准处理（效果优先）或快速处理（速度优先）',
          '开始处理：系统自动进行增强处理，并显示实时进度',
          '下载结果：处理完成后下载增强后的文件'
        ]"
        :notes="[
          '标准模式：深度学习处理，效果最好，适合对质量要求较高的场景',
          '快速模式：传统算法处理，速度更快，适合需要快速处理的场景',
          '建议根据实际需求选择合适的处理模式'
        ]"
        :advantages="[
          {
            title: '深度学习模式',
            description: '采用端到端深度学习模型，通过注意力机制和多尺度特征融合实现最优增强效果'
          },
          {
            title: '快速处理模式',
            description: '基于改进的多阶段串联优化，结合多种传统算法提供高效处理方案'
          },
          {
            title: '灵活双模式',
            description: '可根据需求自由切换处理模式，平衡效果与速度'
          }
        ]"
    />
    <div class="content">
      <div class="detect-container">
        <div class="detection" ref="detectionContainer">
          <el-card class="detection-card">
            <div class="upload-section">
              <h2>水下图像增强系统</h2>

              <!-- 处理模式选择 -->
              <div class="mode-selection">
                <el-radio-group v-model="processingMode" size="medium">
                  <el-radio-button label="fast">快速处理</el-radio-button>
                  <el-radio-button label="standard">标准处理</el-radio-button>
                </el-radio-group>
                <div class="mode-description">
                  {{ modeDescriptions[processingMode] }}
                </div>
              </div>

              <!-- 上传区域 - 当没有文件时显示 -->
              <el-upload
                  v-if="!file"
                  class="upload-area"
                  drag
                  :action="uploadAction"
                  :auto-upload="false"
                  :on-change="handleFileChange"
                  :show-file-list="false"
                  :http-request="() => {}"
              >
                <i class="el-icon-upload"></i>
                <div class="el-upload__text">
                  将文件拖到此处，或<em>点击上传</em>
                </div>
                <div class="el-upload__tip" slot="tip">
                  支持上传jpg/png图片或mp4视频
                </div>
              </el-upload>

              <!-- 文件预览和结果展示区域 -->
              <div v-if="file" :class="['preview-and-result', fileType === 'video' ? 'video-layout' : 'image-layout']">
                <!-- 原始文件预览 -->
                <div :class="['original-file', fileType === 'video' ? 'center-content' : '']">
                  <h3>原始文件</h3>
                  <div class="preview-container">
                    <!-- 图片预览 -->
                    <img
                        v-if="fileType === 'image' && result"
                        :src="getImageUrl(result.original_image)"
                        class="preview-image"
                        alt="原始图片"
                    />
                    <img
                        v-else-if="fileType === 'image'"
                        :src="originalFileUrl"
                        class="preview-image"
                        alt="原始图片"
                    />
                    <!-- 视频预览 -->
                    <div v-if="fileType === 'video'" class="video-preview-wrapper">
                      <video
                          :src="originalFileUrl"
                          class="preview-video"
                          controls
                      ></video>
                      <!-- 视频处理中的简单提示 -->
                      <div v-if="loading" class="video-processing-hint">
                        <i class="el-icon-loading"></i>
                        <span>正在处理，请稍等...</span>
                        <span v-if="result && result.processed_frames && result.total_frames" class="frames-count">
                          ({{ result.processed_frames }}/{{ result.total_frames }} 帧)
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 处理结果展示 - 只在图片模式下显示 -->
                <div class="detection-result" v-if="fileType === 'image'">
                  <h3>检测结果</h3>
                  <div class="result-container">
                    <!-- 处理中显示进度条 -->
                    <div v-if="loading" class="processing-status">
                      <el-progress
                        type="circle"
                        :percentage="100"
                        status="success"
                      >
                        <template #default>
                          <span class="progress-text">
                            处理中...
                          </span>
                        </template>
                      </el-progress>
                      <div class="processing-message">
                        {{ processingMode === 'standard' ? '使用深度学习模型处理中，请耐心等待...' : '快速处理中...' }}
                      </div>
                    </div>
                    
                    <!-- 图片检测结果显示 -->
                    <template v-else-if="result">
                      <el-image
                        :src="getImageUrl(result.result_image)"
                        fit="contain"
                        :preview-src-list="[getImageUrl(result.result_image)]"
                        class="result-image"
                      >
                      </el-image>
                    </template>
                  </div>
                </div>
              </div>

              <!-- 操作按钮 -->
              <div v-if="file" class="action-buttons">
                <el-button
                    type="primary"
                    @click="handleDetect"
                    :loading="loading"
                    :disabled="loading"
                >
                  {{ result ? "重新检测" : "开始检测" }}
                </el-button>
                <!-- 视频处理完成后显示下载按钮 -->
                <el-button
                    type="success"
                    @click="handleDownload"
                    :disabled="!result || loading"
                    v-if="result && (!loading || processingProgress >= 100)"
                >
                  下载结果
                </el-button>
                <el-button @click="resetFile">重置</el-button>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import request from "@/utils/request";
import ToolInstructions from "@/components/ToolInstructions.vue";
import DemoVideoButton from "@/components/DemoVideoButton.vue";

export default {
  name: "Enhance",
  components: {
    ToolInstructions,
    DemoVideoButton,
  },
  data() {
    return {
      file: null,
      fileType: null,
      loading: false,
      result: null,
      processingMode: 'fast',
      modeDescriptions: {
        standard: '采用深度学习模型进行端到端处理，通过注意力机制和多尺度特征融合实现最优增强效果，适合对质量要求较高的场景',
        fast: '使用改进的多阶段串联优化算法，结合暗通道去雾、自适应白平衡等技术实现快速处理，适合需要快速得到结果的场景'
      },
      pythonServiceUrl: process.env.VUE_APP_ENHANCE_URL || "http://localhost:8002",
      videoProcessingTask: null,
      processingProgress: 0,
      processingInterval: null,
      videoError: null,
      retryCount: 0,
      uploadAction: "javascript:;",
      videoUrl: "",
      videoKey: 0,
      originalFileUrl: null,
    };
  },
  computed: {
    progressStatus() {
      if (this.processingProgress >= 100) {
        return 'success';
      }
      return undefined;  // 返回undefined而不是空字符串
    }
  },
  created() {
    // 确保pythonServiceUrl末尾没有斜杠
    if (this.pythonServiceUrl) {
      this.pythonServiceUrl = this.pythonServiceUrl.replace(/\/$/, "");
    }
    console.log("Python服务URL:", this.pythonServiceUrl);
    console.log("环境变量:", process.env.VUE_APP_ENHANCE_URL);
  },
  mounted() {
    // 确保DOM加载完成后再进行样式初始化
    this.$nextTick(() => {
      if (this.$refs.detectionContainer) {
        this.initializeStyles();
      }
    });
  },
  methods: {
    initializeStyles() {
      const container = this.$refs.detectionContainer;
      if (container) {
        container.style.minHeight = "100vh";
        container.style.height = "100vh";
        container.style.padding = "0";
        container.style.position = "relative";
        container.style.display = "flex";
        container.style.alignItems = "center";
        container.style.justifyContent = "center";
        container.style.overflowY = "auto";
      }
    },
    getImageUrl(path) {
      if (!path) {
        console.log("路径为空");
        return "";
      }
      if (path.startsWith("http")) {
        console.log("使用完整URL:", path);
        return path;
      }
      // 确保path以/开头
      const normalizedPath = path.startsWith("/") ? path : `/${path}`;
      const url = `${this.pythonServiceUrl}${normalizedPath}`;
      console.log("构造的URL:", url);
      return url;
    },
    resetState() {
      // 清除之前的结果和状态
      this.result = null;
      this.loading = false;
      this.videoUrl = "";
      this.videoError = null;
      this.processingProgress = 0;
      this.retryCount = 0;
      this.videoProcessingTask = null;
      
      // 停止任何正在进行的轮询
      this.stopPollingStatus();
      
      // 清除之前的视频URL
      if (this.originalFileUrl) {
        URL.revokeObjectURL(this.originalFileUrl);
        this.originalFileUrl = null;
      }
    },
    handleFileChange(file) {
      if (!file || (!file.raw && !file.type)) {
        console.warn('无效的文件对象');
        return;
      }
      
      // 重置状态
      this.resetState();
      
      // 获取实际的文件对象
      const actualFile = file.raw || file;
      
      // 判断文件类型
      this.fileType = actualFile.type && actualFile.type.startsWith('video/') ? 'video' : 'image';
      
      // 创建预览URL
      this.originalFileUrl = URL.createObjectURL(actualFile);
      
      // 保存文件信息
      this.file = actualFile;
      
      console.log('文件类型:', this.fileType);
      console.log('文件对象:', this.file);
    },
    getVideoUrl() {
      if (this.result && this.result.result_video) {
        // 确保使用完整的路径
        const videoPath = this.result.result_video; // 应该是 "/static/videos/enhanced/xxx.mp4"
        // 提取文件名部分
        const videoFilename = videoPath.split('/').pop();
        
        // 使用新的API端点，而不是直接访问静态文件
        const url = `${this.pythonServiceUrl}/api/video-stream/enhanced/${videoFilename}`;
        console.log("构造的视频URL:", url);
        
        // 添加时间戳避免缓存
        const timestamp = new Date().getTime();
        return `${url}?t=${timestamp}`;
      }
      return "";
    },
    handleVideoError(error) {
      console.error("视频加载错误:", error);
      console.log("视频URL:", this.videoUrl);
      console.log("Python服务URL:", this.pythonServiceUrl);
      console.log("结果对象:", JSON.stringify(this.result, null, 2));

      // 最多重试3次
      if (this.retryCount < 3) {
        this.retryCount++;
        this.videoError = `视频加载失败，正在重试(${this.retryCount}/3)...`;

        // 延迟重试
        setTimeout(() => {
          // 重新设置视频URL
          this.videoUrl = this.getVideoUrl();
          // 重新加载视频
          if (this.$refs.videoPlayer) {
            this.$refs.videoPlayer.load();
          }
        }, 2000);
      } else {
        this.videoError = "视频加载失败，请刷新页面重试";
        console.error("视频加载失败，已达到最大重试次数");
      }
    },
    handleVideoLoaded() {
      console.log("视频加载成功");
      this.videoError = null;
      this.retryCount = 0;
    },
    async handleDetect() {
      if (!this.file) {
        this.$message.error('请先上传文件');
        return;
      }
      
      // 重置所有状态
      this.loading = true;
      this.error = null;
      this.result = null;
      this.processingProgress = 0;
      this.videoProcessingTask = null;
      this.videoUrl = "";
      this.videoError = null;

      try {
        console.log('开始进行图像增强处理');
        const formData = new FormData();
        formData.append('file', this.file);
        formData.append('mode', this.processingMode);

        const pythonServiceUrl = this.pythonServiceUrl;
        const apiUrl = `${pythonServiceUrl}/api/enhance`;
        console.log('发送请求到Python服务:', apiUrl);

        // 添加超时控制
        const controller = new AbortController();
        const timeout = setTimeout(() => {
          controller.abort();
        }, 180000); // 3分钟超时
        
        try {
          const response = await fetch(apiUrl, {
            method: 'POST',
            body: formData,
            signal: controller.signal
          });
          
          clearTimeout(timeout); // 清除超时计时器
  
          if (!response.ok) {
            throw new Error(`请求失败: ${response.status} ${response.statusText}`);
          }
  
          const data = await response.json();
          console.log('增强处理结果:', data);
  
          if (this.fileType === 'video') {
            // 视频处理需要轮询状态
            if (data.task_id) {
              this.videoProcessingTask = data.task_id;
              this.result = {
                task_id: data.task_id,
                total_frames: data.total_frames || 0,
                processed_frames: 0,
                status: 'processing'
              };
              // 立即开始轮询状态
              this.startPollingStatus();
            } else {
              throw new Error('未获取到视频处理任务ID');
            }
          } else {
            // 图片处理直接显示结果
            this.handleProcessingComplete(data);
          }
        } catch (err) {
          clearTimeout(timeout); // 确保超时计时器被清除
          throw err; // 向上传递错误
        }
      } catch (error) {
        console.error('增强处理失败:', error);
        if (error.name === 'AbortError') {
          this.$message.error('请求超时，服务器响应时间过长，请稍后重试');
        } else {
          this.$message.error(`处理失败: ${error.message}`);
        }
        this.loading = false;
      }
    },
    startPollingStatus() {
      if (this.processingInterval) {
        clearInterval(this.processingInterval);
      }

      this.processingInterval = setInterval(async () => {
        try {
          if (!this.videoProcessingTask) {
            this.stopPollingStatus();
            return;
          }

          // 添加超时控制
          const controller = new AbortController();
          const timeout = setTimeout(() => {
            controller.abort();
          }, 10000); // 10秒超时
          
          try {
            const response = await fetch(
              `${this.pythonServiceUrl}/api/enhance/video/status/${this.videoProcessingTask}`,
              { signal: controller.signal }
            );
            
            clearTimeout(timeout); // 清除超时计时器

            if (!response.ok) {
              throw new Error(`状态查询失败: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();
            console.log('视频处理状态:', data);

            // 更新进度
            if (data.status === 'processing') {
              // 优先使用后端返回的进度
              if (typeof data.progress === 'number') {
                this.processingProgress = data.progress;
              } else if (data.processed_frames && data.total_frames) {
                this.processingProgress = (data.processed_frames / data.total_frames) * 100;
              }
              // 更新结果对象
              this.result = {
                ...this.result,
                ...data,
                status: 'processing'
              };
            } else if (data.status === 'success') {
              // 处理完成
              this.processingProgress = 100;
              this.stopPollingStatus();
              this.handleProcessingComplete(data);
            } else if (data.status === 'error') {
              throw new Error(data.message || '处理失败');
            }
          } catch (err) {
            clearTimeout(timeout); // 确保超时计时器被清除
            throw err; // 向上传递错误
          }
        } catch (error) {
          console.error('状态查询错误:', error);
          if (error.name === 'AbortError') {
            console.warn('状态查询超时，将在下次轮询中重试');
          } else {
            this.$message.error(`处理出错: ${error.message}`);
            this.stopPollingStatus();
            this.loading = false;
          }
        }
      }, 1000);
    },
    stopPollingStatus() {
      if (this.processingInterval) {
        clearInterval(this.processingInterval);
        this.processingInterval = null;
      }
    },
    handleProcessingComplete(data) {
      console.log('处理完成，接收到的数据:', data);
      
      if (this.fileType === 'video') {
        if (data.status === 'success' && data.result_video) {
          // 更新结果数据
          this.result = {
            ...data,
            filename: this.file.name,
            status: 'success'  // 确保状态被正确设置
          };
          
          // 设置视频URL
          this.videoUrl = this.getVideoUrl();
          console.log('设置视频URL:', this.videoUrl);
          
          // 重置视频相关状态
          this.videoError = null;
          this.retryCount = 0;
          this.videoKey += 1;
          
          // 确保进度为100%
          this.processingProgress = 100;
        }
      } else {
        // 图片处理结果
        this.result = {
          ...data,
          filename: this.file.name
        };
      }

      // 标记加载完成
      this.loading = false;
      // 显示成功消息
      this.$message.success(data.message || '处理成功');
    },
    resetFile() {
      if (this.originalFileUrl) {
        URL.revokeObjectURL(this.originalFileUrl);
      }
      // 添加确认提示
      if (this.loading) {
        this.$confirm("正在处理中，确定要取消吗？", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
            .then(() => {
              this._doReset();
            })
            .catch(() => {
              // 用户取消重置
            });
      } else {
        this._doReset();
      }
    },
    _doReset() {
      this.file = null;
      this.fileType = null;
      this.result = null;
      this.originalFileUrl = null;
      this.loading = false;
      this.videoUrl = "";
      this.videoError = null;
      this.processingProgress = 0;
      this.retryCount = 0;
    },
    // 添加下载方法
    async handleDownload() {
      if (!this.result) {
        this.$message.warning("没有可下载的结果");
        return;
      }

      try {
        const url =
            this.fileType === "image"
                ? this.getImageUrl(this.result.result_image)
                : this.getImageUrl(this.result.result_video);

        // 添加超时控制
        const controller = new AbortController();
        const timeout = setTimeout(() => {
          controller.abort();
        }, 60000); // 60秒超时
        
        try {
          // 使用fetch直接获取数据
          const response = await fetch(url, { signal: controller.signal });
          
          clearTimeout(timeout); // 清除超时计时器
          
          if (!response.ok) {
            throw new Error(`获取文件失败: ${response.status} ${response.statusText}`);
          }
  
          // 获取blob数据
          const blob = await response.blob();
  
          // 创建下载链接
          const downloadUrl = window.URL.createObjectURL(blob);
          const link = document.createElement("a");
          link.href = downloadUrl;
  
          // 设置文件名
          const originalFileName = this.file.name;
          const extension = originalFileName.split(".").pop();
          const timestamp = new Date().getTime();
          const downloadFileName = `enhanced_${timestamp}.${extension}`;
          link.download = downloadFileName;
  
          // 触发下载
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
  
          // 清理URL对象
          window.URL.revokeObjectURL(downloadUrl);
  
          this.$message.success("下载开始");
        } catch (err) {
          clearTimeout(timeout); // 确保超时计时器被清除
          throw err; // 向上传递错误
        }
      } catch (error) {
        console.error("下载失败:", error);
        if (error.name === 'AbortError') {
          this.$message.error("下载超时，文件可能过大，请稍后重试");
        } else {
          this.$message.error("下载失败，请重试");
        }
      }
    },
    // 添加视频URL验证方法
    validateVideoUrl(url) {
      if (!url) return false;
      try {
        const urlObj = new URL(url);
        return urlObj.pathname.includes("/static/videos/");
      } catch (e) {
        console.error("无效的URL:", url);
        return false;
      }
    },
  },
  beforeDestroy() {
    this.stopPollingStatus();
    if (this.originalFileUrl) {
      URL.revokeObjectURL(this.originalFileUrl);
    }
  },
};
</script>

<style lang="less" scoped>
.enhance-container {
  min-height: calc(100vh - 60px);
  background: #f5f7fa;
  padding-top: 0;


}

.detection {
  background: url("../../assets/imgs/bgc3.jpg") no-repeat center center;
  background-size: cover;
  min-height: calc(100vh - 60px);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.detection::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
      to bottom,
      rgba(0, 14, 41, 0.85) 0%,
      rgba(0, 29, 82, 0.75) 50%,
      rgba(0, 14, 41, 0.85) 100%
  );
  backdrop-filter: blur(8px);
}

.detection-card {
  position: relative;
  z-index: 1;
  width: 90%;
  max-width: 1200px;
  margin: 20px auto;
  background: rgba(6, 25, 56, 0.85);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 198, 255, 0.15);
  border-radius: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3),
  0 0 0 1px rgba(0, 198, 255, 0.15) inset;
  overflow: hidden;
  animation: fadeIn 0.5s ease-out;
}

.upload-section {
  padding: 40px 30px;
  text-align: center;
  color: rgba(255, 255, 255, 0.9);
}

.upload-section h2 {
  font-size: 2.5rem;
  margin-bottom: 30px;
  background: linear-gradient(120deg, #00c6ff, #0072ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  animation: glow 3s ease-in-out infinite alternate;
  letter-spacing: 2px;
}

.mode-selection {
  margin-bottom: 30px;
  padding: 20px;
  background: rgba(2, 17, 43, 0.6);
  border: 1px solid rgba(0, 198, 255, 0.15);
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.el-radio-group {
  margin-bottom: 15px;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.el-radio-button {
  margin: 0;
}

.mode-description {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.95rem;
  text-align: center;
  padding: 10px;
  background: rgba(0, 198, 255, 0.1);
  border-radius: 8px;
  margin-top: 10px;
}

/deep/ .el-radio-button__inner {
  background: rgba(0, 198, 255, 0.15);
  border: 1px solid rgba(0, 198, 255, 0.3);
  color: rgba(255, 255, 255, 0.9);
  padding: 10px 25px;
  transition: all 0.3s ease;
}

/deep/ .el-radio-button__orig-radio:checked + .el-radio-button__inner {
  background: linear-gradient(45deg, rgba(0, 98, 255, 0.8), rgba(0, 163, 255, 0.8));
  border-color: transparent;
  box-shadow: none;
}

.upload-area {
  margin: 30px auto;
  max-width: 600px;
  padding: 40px;
  border: 2px dashed rgba(0, 198, 255, 0.3);
  border-radius: 20px;
  background: linear-gradient(
      145deg,
      rgba(2, 17, 43, 0.7) 0%,
      rgba(6, 25, 56, 0.8) 100%
  );
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2),
  0 0 0 1px rgba(0, 198, 255, 0.1) inset;
}

.el-upload {
  background: transparent !important;
  width: 100%;
}

.el-upload-dragger {
  background: transparent !important;
  border: none !important;
  width: 100% !important;
}

/deep/.el-upload-dragger {
  background: transparent !important;
  border: none !important;
  width: 100% !important;
}

/deep/.el-upload {
  background: transparent !important;
  width: 100%;
}

.el-icon-upload {
  font-size: 48px;
  color: rgba(0, 198, 255, 0.8);
  margin-bottom: 20px;
  transition: all 0.3s ease;
  animation: float 3s ease-in-out infinite;
  filter: drop-shadow(0 0 10px rgba(0, 198, 255, 0.5));
}

.el-upload__text {
  color: rgba(255, 255, 255, 0.9) !important;
  font-size: 1.2rem;
  margin-bottom: 10px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.el-upload__text em {
  color: rgba(0, 198, 255, 0.9) !important;
  font-style: normal;
  text-decoration: none;
  border-bottom: 1px solid rgba(0, 198, 255, 0.3);
  padding-bottom: 2px;
  transition: all 0.3s ease;
}

.el-upload__tip {
  color: rgba(255, 255, 255, 0.6) !important;
  font-size: 0.9rem;
  margin-top: 15px;
}

.preview-and-result {
  display: grid;
  gap: 20px;
  margin: 30px auto;
  padding: 0 20px;
  max-width: 1000px;
}

/* 图片模式使用左右分栏布局 */
.preview-and-result.image-layout {
  grid-template-columns: 1fr 1fr;
}

/* 视频模式使用单列布局 */
.preview-and-result.video-layout {
  grid-template-columns: 1fr;
}

/* 居中内容的样式 */
.center-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  width: 100%;
  max-width: 800px;
}

.preview-container,
.result-container {
  background: rgba(2, 17, 43, 0.6);
  border: 1px solid rgba(0, 198, 255, 0.15);
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.preview-image,
.result-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.preview-video {
  width: 100%;
  max-width: 800px;
  height: auto;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.video-title {
  color: rgba(255, 255, 255, 0.9);
  margin: 10px 0;
  font-size: 1.1rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.action-buttons {
  margin: 20px 0;
  display: flex;
  justify-content: center;
  gap: 15px;
}

.el-button {
  background: rgba(0, 198, 255, 0.15);
  border: 1px solid rgba(0, 198, 255, 0.3);
  color: rgba(255, 255, 255, 0.9);
  padding: 10px 25px;
  border-radius: 25px;
  transition: all 0.3s ease;
}

.el-button:hover {
  background: rgba(0, 198, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 198, 255, 0.2);
}

.el-button--primary {
  background: linear-gradient(
      45deg,
      rgba(0, 98, 255, 0.8),
      rgba(0, 163, 255, 0.8)
  );
  border: none;
}

.el-button--primary:hover {
  background: linear-gradient(
      45deg,
      rgba(0, 114, 255, 0.9),
      rgba(0, 179, 255, 0.9)
  );
}

.processing-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  width: 100%;
  padding: 40px;
  background: rgba(2, 17, 43, 0.4);
  border-radius: 15px;
  
  /deep/ .el-progress {
    .el-progress-circle {
      width: 120px !important;
      height: 120px !important;
    }
    
    .el-progress__text {
      color: rgba(255, 255, 255, 0.9);
      font-size: 16px;
    }
  }
  
  .progress-text {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.9);
    text-align: center;
    line-height: 1.5;
  }
  
  .processing-message {
    margin-top: 20px;
    color: rgba(255, 255, 255, 0.7);
    font-size: 14px;
    padding: 12px 20px;
    background: rgba(0, 198, 255, 0.1);
    border-radius: 8px;
    border: 1px solid rgba(0, 198, 255, 0.15);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(4px);
    max-width: 300px;
    text-align: center;
  }
}

.video-error {
  color: #ff5722;
  background: rgba(255, 87, 34, 0.1);
  padding: 15px;
  border-radius: 10px;
  margin-top: 20px;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 87, 34, 0.2);
}

.video-loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.8);
  padding: 30px;
  border-radius: 15px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 10;
}

.start-detection {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(0, 198, 255, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(0, 198, 255, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(0, 198, 255, 0);
  }
}

@keyframes glow {
  from {
    text-shadow: 0 0 10px rgba(0, 198, 255, 0.5),
    0 0 20px rgba(0, 114, 255, 0.3);
  }
  to {
    text-shadow: 0 0 20px rgba(0, 198, 255, 0.7),
    0 0 30px rgba(0, 114, 255, 0.5), 0 0 40px rgba(0, 114, 255, 0.3);
  }
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* 添加新的动画 */
@keyframes borderGlow {
  0%,
  100% {
    border-color: rgba(0, 198, 255, 0.3);
  }
  50% {
    border-color: rgba(0, 198, 255, 0.8);
  }
}

@keyframes backgroundPulse {
  0%,
  100% {
    background: rgba(6, 25, 56, 0.5);
  }
  50% {
    background: rgba(6, 25, 56, 0.7);
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .detection {
    padding: 20px 0;
  }

  .detection-card {
    margin: 10px;
    width: 95%;
  }

  .upload-section h2 {
    font-size: 2rem;
  }

  .preview-and-result {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .el-button {
    width: 100%;
  }
}

.video-preview-wrapper {
  position: relative;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.video-processing-hint {
  margin-top: 15px;
  padding: 10px 20px;
  background: rgba(0, 198, 255, 0.1);
  border: 1px solid rgba(0, 198, 255, 0.15);
  border-radius: 20px;
  color: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  backdrop-filter: blur(5px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  animation: pulse 2s infinite;
}

.video-processing-hint i {
  color: rgba(0, 198, 255, 0.9);
  font-size: 18px;
}

.frames-count {
  margin-left: 5px;
  font-size: 12px;
  opacity: 0.8;
}

.preview-video {
  width: 100%;
  max-width: 800px;
  height: auto;
  border-radius: 8px;
  transition: transform 0.3s ease;
}
</style>
