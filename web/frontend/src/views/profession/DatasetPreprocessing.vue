<script>
import axios from "axios";
import FrontLayout from "@/views/Front.vue";
import request from "@/utils/request";
import ToolInstructions from "@/components/ToolInstructions.vue";
import DemoVideoButton from "@/components/DemoVideoButton.vue";

export default {
  name: "DatasetPreprocessing",
  components: {
    ToolInstructions,
    FrontLayout,
    DemoVideoButton,
  },
  data() {
    return {
      dataset: null,
      loading: false,
      result: null,
      javaServiceUrl: process.env.VUE_APP_BASE_API || "http://localhost:9090",
      pythonServiceUrl: process.env.VUE_APP_DATASET_URL || "http://localhost:8001",
      uploadAction: "javascript:;",
      processingProgress: 0,
      uploading: false,
      uploadProgress: 0,
      previewImages: [],
      currentPreviewIndex: 0,
      errorImages: [],
      totalImages: 0,
      selectedEnvironment: "deep", // 默认选择深水环境
      processedTimestamp: null,
    };
  },
  methods: {
    progressFormat(percentage) {
      return percentage === 100 ? "上传完成" : `${percentage}%`;
    },

    async handleUpload(file) {
      if (!file.raw.type.includes("zip")) {
        this.$message.error("请上传ZIP格式的文件！");
        return false;
      }

      try {
        // 直接在本地保存文件对象，不再上传到Java服务器
        this.dataset = {
          ...file,
          path: null,  // 不再依赖文件路径
        };

        this.$message.success("文件已准备好，点击开始处理按钮进行处理");
        return true;
      } catch (error) {
        console.error("准备文件失败:", error);
        this.$message.error("准备文件失败: " + error.message);
        return false;
      } finally {
        this.uploading = false;
        this.uploadProgress = 0;
      }
    },

    showErrorNotification(title, message) {
      this.$notify({
        title: title,
        message: message.replace(/\n/g, "<br>"),
        type: "error",
        duration: 0,
        dangerouslyUseHTMLString: true,
        customClass: "error-notification",
      });
    },

    async handleProcess() {
      if (!this.dataset) {
        this.$message.warning("请先选择数据集");
        return;
      }

      // 添加确认提示
      this.$confirm('处理过程中请勿刷新或离开页面，是否继续？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        this.loading = true;
        this.processingProgress = 0;
        this.result = null;
        this.previewImages = [];

        try {
          this.processingProgress = 30;

          // 创建FormData对象
          const formData = new FormData();

          // 如果dataset.raw存在，直接上传原始文件
          if (this.dataset.raw) {
            formData.append("file", this.dataset.raw);
            formData.append("environment", this.selectedEnvironment);

            console.log("直接上传文件到Python服务");
            console.log("使用环境参数:", this.selectedEnvironment);
            console.log("FormData内容:", Array.from(formData.entries()));
            
            // 发送FormData请求给Python服务 - 直接处理，不再分两步
            console.log("发送请求到:", `${this.pythonServiceUrl}/api/dataset/process`);

            const pythonResponse = await axios.post(
                `${this.pythonServiceUrl}/api/dataset/process`,
                formData,
                {
                  headers: {
                    "Content-Type": "multipart/form-data"
                  },
                  onUploadProgress: (progressEvent) => {
                    const percentCompleted = Math.round(
                        (progressEvent.loaded * 100) / progressEvent.total
                    );
                    this.processingProgress = 30 + percentCompleted * 0.6; // 30-90%
                  }
                }
            );

            console.log("Python服务响应:", pythonResponse.data);

            if (pythonResponse.data && pythonResponse.data.path) {
              this.result = {
                processedDatasetPath: pythonResponse.data.path,
              };
              this.processingProgress = 100;
              this.$message({
                message: pythonResponse.data.message || "数据集预处理完成",
                type: "success",
                duration: 1000  // 1秒后自动关闭
              });

              // 提取时间戳ID用于获取预览图片
              const processedPath = pythonResponse.data.path;
              const timestampMatch = processedPath.match(/\d{14}/);
              if (timestampMatch) {
                this.processedTimestamp = timestampMatch[0];
                console.log("提取的时间戳ID:", this.processedTimestamp);
              }

              await this.fetchPreviewImages();
            } else {
              throw new Error("处理失败：响应数据格式不正确");
            }
          } 
          // 使用JSON发送文件路径
          else if (this.dataset.path) {
            // 使用JSON发送文件路径
            const requestData = {
              datasetPath: this.dataset.path,
              environment: this.selectedEnvironment,
              fileName: this.dataset.name,
              fileSize: this.dataset.size
            };

            console.log("使用已上传文件路径:", this.dataset.path);
            console.log("使用环境参数:", this.selectedEnvironment);

            // 直接处理已上传的文件
            console.log("发送请求到:", `${this.javaServiceUrl}/api/dataset/datasetprocess`);
            // 注意：这里使用Java服务器，而不是直接调用Python
            const response = await request({
              url: "/api/dataset/datasetprocess",
              method: "post",
              data: requestData
            });

            console.log("Java服务响应:", response);

            if (response.code === "200" && response.data) {
              this.result = {
                processedDatasetPath: response.data.path,
              };
              this.processingProgress = 100;
              this.$message({
                message: "数据集预处理完成",
                type: "success",
                duration: 1000
              });

              await this.fetchPreviewImages();
            } else {
              throw new Error("处理失败：" + (response.msg || "服务器返回错误"));
            }
          }
          else {
            throw new Error("无效的数据集格式");
          }
        } catch (error) {
          console.error("处理失败:", error);
          let errorTitle = "处理失败";
          let errorMessage = "处理过程出现错误，请重试";

          if (error.response) {
            const { status, data } = error.response;
            console.log("错误响应:", data);

            if (status === 400) {
              if (data.detail && typeof data.detail === "string") {
                if (data.detail.includes("No dataset folder found")) {
                  errorMessage =
                      "文件结构错误：未找到数据集文件夹\n\n正确的操作步骤：\n1. 创建一个文件夹（名称任意）\n2. 将所有图片放入该文件夹\n3. 将该文件夹压缩成ZIP文件";
                } else if (data.detail.includes("Invalid image dimensions")) {
                  errorMessage =
                      "图片尺寸错误：\n请确保所有图片尺寸在256x256到1024x1024像素之间";
                } else if (data.detail.includes("Unsupported file format")) {
                  errorMessage = "文件格式错误：\n请确保所有文件为jpg或png格式";
                } else {
                  errorMessage = `数据集格式错误：\n${data.detail}`;
                }
              }
            } else if (status === 413) {
              errorMessage = "文件太大，请压缩后重试";
            } else if (status === 415) {
              errorMessage = "不支持的文件类型，请上传ZIP格式的文件";
            } else if (status === 500) {
              errorTitle = "服务器错误";
              errorMessage = "服务器处理失败，请检查数据格式是否正确";
            }
          } else if (error.request) {
            errorTitle = "连接错误";
            errorMessage = "无法连接到服务器，请检查网络连接";
          }

          this.showErrorNotification(errorTitle, errorMessage);
          this.processingProgress = 0;
        } finally {
          this.loading = false;
        }
      });
    },

    async fetchPreviewImages() {
      try {
        if (!this.result || !this.result.processedDatasetPath) {
          return;
        }

        // 优先使用processedTimestamp作为ID
        if (!this.processedTimestamp) {
          // 尝试从路径中提取时间戳
          const processedPath = this.result.processedDatasetPath;
          const timestampMatch = processedPath.match(/\d{14}/);
          if (timestampMatch) {
            this.processedTimestamp = timestampMatch[0];
          }
        }

        // 如果没有时间戳，无法获取预览图片
        if (!this.processedTimestamp) {
          console.error("无法提取处理ID，无法获取预览图片");
          return;
        }

        console.log("获取预览图片，时间戳:", this.processedTimestamp);
        // 添加随机参数，避免缓存
        const timestamp = new Date().getTime();
        // 首先尝试Python直接路径
        let previewResponse;
        try {
          console.log(`尝试从Python服务获取预览: ${this.pythonServiceUrl}/api/datasetprocess/preview/${this.processedTimestamp}`);
          previewResponse = await axios.get(
              `${this.pythonServiceUrl}/api/datasetprocess/preview/${this.processedTimestamp}?_t=${timestamp}`,
              {
                headers: {
                  "Content-Type": "application/json",
                  "Cache-Control": "no-cache"
                },
              }
          );
        } catch (error) {
          console.log("Python服务获取预览失败，尝试Java服务:", error);
          // 如果Python直接访问失败，尝试通过Java服务代理
          previewResponse = await request({
            url: `/api/dataset/preview/${this.processedTimestamp}`,
            method: "get",
            params: { _t: timestamp }
          });
        }

        console.log("预览接口响应:", previewResponse.data);

        if (previewResponse.data) {
          if (previewResponse.data.previewPairs && previewResponse.data.previewPairs.length > 0) {
            // 为每个图片URL添加基础路径和时间戳参数避免缓存
            this.previewImages = previewResponse.data.previewPairs.map((pair) => ({
              original: `${this.pythonServiceUrl}${pair.original}?_t=${timestamp}`,
              processed: `${this.pythonServiceUrl}${pair.processed}?_t=${timestamp}`,
            }));
            this.currentPreviewIndex = 0;
            console.log("成功获取预览图片:", this.previewImages.length, "张");
          } else if (previewResponse.data.status === "processing") {
            // 如果处理中，等待1秒后重试
            console.log("数据集仍在处理中，稍后重试获取预览");
            setTimeout(() => {
              this.fetchPreviewImages();
            }, 1000);
            return;
          } else {
            console.log("没有找到预览图片或正在处理中");
          }

          // 保存错误图片信息
          this.errorImages = previewResponse.data.errorImages || [];
          this.totalImages = previewResponse.data.totalImages || 0;

          // 如果有错误图片，显示警告信息
          if (this.errorImages.length > 0) {
            this.$notify({
              title: "处理警告",
              message: `${this.errorImages.length}张图片因尺寸问题未能处理`,
              type: "warning",
              duration: 5000,
            });
          }
        }
      } catch (error) {
        console.error("获取预览图片失败:", error);
        // 不显示错误信息，可能是服务器正在处理中
      }
    },

    async handleDownload() {
      if (!this.result || !this.result.processedDatasetPath) {
        this.$message.warning("没有可下载的结果");
        return;
      }

      try {
        // 处理下载路径
        const downloadPath = this.result.processedDatasetPath.replace(
            /^\/+/,
            ""
        ); // 移除开头的斜杠

        // 直接从Python服务下载
        const response = await axios({
          url: `${this.pythonServiceUrl}/${downloadPath}`,
          method: "GET",
          responseType: "blob"
        });

        const blob = new Blob([response.data]);
        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = downloadUrl;

        // 从路径中提取文件名或使用时间戳生成文件名
        let filename = downloadPath.split("/").pop();
        if (!filename) {
          const timestamp = new Date().getTime();
          filename = `processed_dataset_${timestamp}.zip`;
        }

        link.download = filename;

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);

        this.$message.success("下载开始");
      } catch (error) {
        console.error("下载失败:", error);
        this.$message.error("下载失败，请重试");
      }
    },

    resetDataset() {
      if (this.loading) {
        this.$confirm("正在处理中，确定要取消吗？", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
            .then(() => {
              this._doReset();
            })
            .catch(() => {});
      } else {
        this._doReset();
      }
    },

    _doReset() {
      this.dataset = null;
      this.result = null;
      this.loading = false;
      this.processingProgress = 0;
      this.uploading = false;
      this.uploadProgress = 0;
      this.previewImages = [];
      this.currentPreviewIndex = 0;
    },

    formatFileSize(bytes) {
      if (bytes === 0) return "0 Bytes";
      const k = 1024;
      const sizes = ["Bytes", "KB", "MB", "GB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
    },
  },
};
</script>

<template>
  <div class="dataset-preprocessing-container">
    <DemoVideoButton video-url="dataset.mp4" />
    <tool-instructions
        title="水下模拟数据集生成工具"
        description="专为水下计算机视觉研究设计的数据集生成工具。基于深度学习的图像转换技术，可将普通图片精确模拟转换为不同水深环境下的图像效果，为水下目标检测、图像增强等研究提供高质量的训练数据集。"
        :features="[
          '双环境模拟：支持深水/浅水环境的精确模拟',
          '批量处理：支持大规模数据集的批量转换',
          '保真度高：准确还原水下成像物理特性',
          '可控性强：可调节不同水下环境参数'
        ]"
        :formats="[
          '输入格式：JPG、PNG、JPEG格式图片',
          '图片尺寸：建议不小于256x256像素',
          '数据组织：ZIP压缩包，包含待处理图片',
          '单次处理：150张图片(158MB)/1min30s; 4000张图片(2.42GB)/30min'
        ]"
        :steps="[
          '准备图片：收集清晰的原始图片',
          '打包上传：将图片打包成ZIP格式',
          '选择环境：选择深水或浅水环境',
          '开始处理：等待系统自动处理(过程中不可切换页面)',
          '下载结果：获取模拟后的水下图像'
        ]"
        :notes="[
          '图片质量：建议使用清晰、光照均匀的原始图片，(不可使用复制粘贴出的wins快捷方式图片)',
          '环境选择：深水环境色调偏蓝，浅水环境偏绿',
          '处理时间：根据数据量约3-5分钟/100张',
          '图片尺寸：系统会自动调整为4的倍数'
        ]"
        :advantages="[
          {
            title: '物理模型驱动',
            description: '基于水下光学传播模型，精确模拟水下成像衰减特性'
          },
          {
            title: '场景适应性强',
            description: '适用于各类场景图片，支持不同深度和水质条件的模拟'
          },
          {
            title: '降质效果真实',
            description: '通过大量真实水下图像训练，生成效果与实际水下拍摄高度相似'
          }
        ]"
    />
    <div class="content">
      <div class="detect-container">
        <div class="detection-card">
          <div class="upload-section">
            <h2>水下模拟数据集生成</h2>

            <!-- 尺寸要求说明 -->
            <div class="size-requirements">
              <h3>数据要求说明</h3>
              <el-alert
                  title="请确保您的数据满足以下要求："
                  type="info"
                  :closable="false"
              >
                <div class="requirements-list">
                  <p>图片尺寸：建议不小于256x256像素，图片尺寸会自动调整为4的倍数</p>
                  <p>
                    ZIP文件结构：必须包含一个数据集文件夹，文件夹内放置图片
                  </p>
                  <p>支持格式：jpg/png格式图片</p>
                  <p>为保证最佳效果，建议使用清晰、光照均匀的原始图片</p>
                </div>
              </el-alert>
            </div>

            <!-- 上传区域 -->
            <el-upload
                v-if="!dataset"
                class="upload-area"
                drag
                :action="uploadAction"
                :auto-upload="false"
                :on-change="handleUpload"
                :show-file-list="false"
                :http-request="() => {}"
                accept=".zip"
            >
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">
                将数据集压缩包拖到此处，或<em>点击上传</em>
              </div>
              <div class="el-upload__tip" slot="tip">
                请上传包含图片的ZIP压缩文件
              </div>
            </el-upload>

            <!-- 添加上传进度条 -->
            <div v-if="uploading" class="upload-progress">
              <el-progress
                  :percentage="uploadProgress"
                  :format="progressFormat"
                  status="success"
              >
              </el-progress>
              <p>正在上传文件，请稍候...</p>
            </div>

            <!-- 数据集信息展示区域 -->
            <div v-if="dataset" class="dataset-info">
              <h3>数据集信息</h3>
              <p>文件名：{{ dataset.name }}</p>
              <p>大小：{{ formatFileSize(dataset.size) }}</p>

              <!-- 添加环境选择 -->
              <div class="environment-select">
                <h3>环境选择</h3>
                <div
                    class="custom-radio-group"
                    role="radiogroup"
                    aria-label="环境选择"
                >
                  <label class="custom-radio" :class="{'active-deep': selectedEnvironment === 'deep'}">
                    <input
                        type="radio"
                        v-model="selectedEnvironment"
                        value="deep"
                        :checked="selectedEnvironment === 'deep'"
                        @change="selectedEnvironment = 'deep'"
                    />
                    <span class="radio-label">
                      <span>深水环境</span>
                      <el-tooltip
                          content="模拟深水环境下的图像降质效果：蓝色色调更强，可见度较低"
                          placement="top"
                      >
                        <i class="el-icon-question"></i>
                      </el-tooltip>
                    </span>
                  </label>
                  <label class="custom-radio" :class="{'active-shallow': selectedEnvironment === 'shallow'}">
                    <input
                        type="radio"
                        v-model="selectedEnvironment"
                        value="shallow"
                        :checked="selectedEnvironment === 'shallow'"
                        @change="selectedEnvironment = 'shallow'"
                    />
                    <span class="radio-label">
                      <span>浅水环境</span>
                      <el-tooltip
                          content="模拟浅水环境下的图像降质效果：绿色色调更强，可见度相对较高"
                          placement="top"
                      >
                        <i class="el-icon-question"></i>
                      </el-tooltip>
                    </span>
                  </label>
                </div>
                <div class="environment-info" v-if="selectedEnvironment === 'shallow'">
                  <el-alert
                    title="浅水环境特性"
                    type="info"
                    :closable="false"
                    show-icon
                  >
                    <p>浅水模型特点：绿色调为主，水下物体轮廓较清晰，环境光散射较少</p>
                  </el-alert>
                </div>
                <div class="environment-info" v-else>
                  <el-alert
                    title="深水环境特性"
                    type="info" 
                    :closable="false"
                    show-icon
                  >
                    <p>深水模型特点：蓝色调为主，水下物体轮廓有模糊，环境光散射强烈</p>
                  </el-alert>
                </div>
              </div>

              <!-- 处理状态和进度 -->
              <div class="processing-status" v-if="loading">
                <el-progress
                    type="circle"
                    :percentage="processingProgress"
                ></el-progress>
                <p>正在处理中，请稍候...</p>
                <el-alert
                    title="请勿刷新页面或离开页面，否则进度将中断！"
                    type="warning"
                    :closable="false"
                    show-icon
                    style="margin-top: 20px;"
                >
                </el-alert>
              </div>

              <!-- 错误信息显示 -->
              <div v-if="errorImages.length > 0" class="error-section">
                <el-alert
                    title="处理警告"
                    type="warning"
                    :closable="false"
                    show-icon
                >
                  <div class="error-list">
                    <p>
                      以下 {{ errorImages.length }} 张图片因尺寸问题未能处理：
                    </p>
                    <ul>
                      <li v-for="(error, index) in errorImages" :key="index">
                        第{{ error.index }}张图片 ({{ error.file }})
                      </li>
                    </ul>
                    <p class="error-note">
                      请确保图片尺寸符合要求：宽高必须是4的倍数，且不小于256像素
                    </p>
                  </div>
                </el-alert>
              </div>

              <!-- 预览区域 -->
              <div v-if="previewImages.length > 0" class="preview-section">
                <h3>处理效果预览</h3>
                <div class="preview-status">
                  已处理 {{ currentPreviewIndex + 1 }}/{{
                    previewImages.length
                  }}
                  张图片
                </div>
                <div class="preview-container">
                  <div class="image-box">
                    <h4>原始图片</h4>
                    <img
                        :src="previewImages[currentPreviewIndex].original"
                        alt="原始图片"
                    />
                  </div>
                  <div class="image-box">
                    <h4>处理后图片</h4>
                    <img
                        :src="previewImages[currentPreviewIndex].processed"
                        alt="处理后图片"
                    />
                  </div>
                </div>
                <div class="preview-controls">
                  <el-button
                      :disabled="currentPreviewIndex === 0"
                      @click="currentPreviewIndex--"
                      icon="el-icon-arrow-left"
                  >
                    上一张
                  </el-button>
                  <span class="preview-counter">
                    {{ currentPreviewIndex + 1 }} / {{ previewImages.length }}
                  </span>
                  <el-button
                      :disabled="currentPreviewIndex >= previewImages.length - 1"
                      @click="currentPreviewIndex++"
                      icon="el-icon-arrow-right"
                  >
                    下一张
                  </el-button>
                </div>
              </div>

              <!-- 处理完成后的结果 -->
              <div v-if="result" class="processing-result">
                <el-alert
                    title="处理完成"
                    type="success"
                    :closable="true"
                    show-icon
                    :duration="1000"
                >
                </el-alert>
                <div class="result-actions">
                  <el-button
                      type="success"
                      @click="handleDownload"
                      :disabled="!result"
                  >
                    下载处理后的数据集
                  </el-button>
                </div>
              </div>

              <!-- 操作按钮 -->
              <div class="action-buttons">
                <el-button
                    type="primary"
                    @click="handleProcess"
                    :loading="loading"
                    :disabled="loading"
                >
                  {{ result ? "重新处理" : "开始处理" }}
                </el-button>
                <el-button @click="resetDataset">重置</el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="less" scoped>
.dataset-preprocessing-container {
  min-height: calc(100vh - 60px);
  background: #f5f7fa;
  padding-top: 0;


}

.detect-container {
  min-height: 100vh;
  padding: 40px 0;
  background: url("../../assets/imgs/bgc3.jpg") no-repeat center center;
  background-size: cover;
  position: relative;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.detect-container::before {
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
  top:20px;
  margin: 0 auto;
  background: rgba(6, 25, 56, 0.85);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 198, 255, 0.15);
  border-radius: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3),
  0 0 0 1px rgba(0, 198, 255, 0.15) inset;
  overflow: visible;
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

.size-requirements {
  margin: 30px auto;
  max-width: 800px;
  padding: 30px;
  background: linear-gradient(
      145deg,
      rgba(2, 17, 43, 0.7) 0%,
      rgba(6, 25, 56, 0.8) 100%
  );
  border-radius: 20px;
  border: 1px solid rgba(0, 198, 255, 0.1);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2),
  0 0 0 1px rgba(0, 198, 255, 0.1) inset;
  text-align: center;
}

.size-requirements h3 {
  color: #ffffff;
  font-size: 1.5rem;
  margin-bottom: 20px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/deep/.el-alert--info.is-light {
  background-color: #041430;
  color: #909399;
  border: none;
  border-radius: 10px;
  margin-top: 15px;
  display: flex;
  align-items: center;
  min-height: 60px;
}

/deep/.el-alert__content {
  padding: 0;
  text-align: center;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/deep/.el-alert__title {
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
  text-align: center;
}

.requirements-list {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.1rem;
  line-height: 1.6;
  text-align: center;
  padding: 10px 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.requirements-list p {
  margin: 5px 0;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
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

.dataset-info {
  margin: 30px auto;
  max-width: 800px;
  padding: 30px;
  background: linear-gradient(
      145deg,
      rgba(2, 17, 43, 0.7) 0%,
      rgba(6, 25, 56, 0.8) 100%
  );
  border-radius: 20px;
  border: 1px solid rgba(0, 198, 255, 0.1);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2),
  0 0 0 1px rgba(0, 198, 255, 0.1) inset;
}

.environment-select {
  margin: 40px auto;
  padding: 30px;
  background: linear-gradient(
      145deg,
      rgba(2, 17, 43, 0.7) 0%,
      rgba(6, 25, 56, 0.8) 100%
  );
  border-radius: 20px;
  border: 1px solid rgba(0, 198, 255, 0.1);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2),
  0 0 0 1px rgba(0, 198, 255, 0.1) inset;
}

.custom-radio-group {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-top: 25px;
}

.custom-radio {
  padding: 15px 30px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 198, 255, 0.2);
  border-radius: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.custom-radio:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 198, 255, 0.2);
}

.preview-section {
  margin: 40px auto;
  max-width: 1000px;
  padding: 0 20px;
}

.preview-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin: 30px 0;
}

.image-box {
  background: linear-gradient(
      145deg,
      rgba(2, 17, 43, 0.7) 0%,
      rgba(6, 25, 56, 0.8) 100%
  );
  padding: 20px;
  border-radius: 15px;
  border: 1px solid rgba(0, 198, 255, 0.15);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2),
  0 0 0 1px rgba(0, 198, 255, 0.1) inset;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.image-box img {
  width: 100%;
  max-width: 350px;
  height: auto;
  max-height: 350px;
  object-fit: contain;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.image-box h4 {
  color: rgba(255, 255, 255, 0.9);
  margin: 10px 0;
  font-size: 1.1rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.preview-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 30px;
}

.preview-counter {
  color: #ffffff;
  font-size: 1.1rem;
  min-width: 80px;
  text-align: center;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
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

.el-button--success {
  background: linear-gradient(45deg, #00b09b, #86c93d);
  border: none;
  box-shadow: 0 4px 15px rgba(0, 176, 155, 0.3);
}

.el-button--success:hover {
  background: linear-gradient(45deg, #00c0a9, #96d94d);
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 176, 155, 0.5);
}

.el-button--default {
  background: transparent;
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: rgba(255, 255, 255, 0.9);
}

.el-button--default:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 255, 255, 0.2);
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
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

/* 响应式调整 */
@media (max-width: 1200px) {
  .image-box img {
    max-width: 300px;
    max-height: 300px;
  }
}

@media (max-width: 768px) {
  .detect-container {
    padding: 20px 0;
  }

  .detection-card {
    width: 95%;
  }

  .upload-section h2 {
    font-size: 2rem;
  }

  .preview-container {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .image-box img {
    max-width: 280px;
    max-height: 280px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .el-button {
    width: 100%;
  }
}

.preview-section h3 {
  color: #ffffff;
  font-size: 1.8rem;
  margin-bottom: 10px;
  text-align: center;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.preview-status {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.1rem;
  text-align: center;
  margin-bottom: 20px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

/* 环境选择样式 */
.active-deep {
  background: linear-gradient(
      45deg,
      rgba(0, 114, 255, 0.2),
      rgba(0, 179, 255, 0.3)
  ) !important;
  box-shadow: 0 0 15px rgba(0, 140, 255, 0.4);
  border-color: rgba(0, 140, 255, 0.5) !important;
  transform: translateY(-3px);
}

.active-shallow {
  background: linear-gradient(
      45deg,
      rgba(0, 150, 136, 0.2),
      rgba(76, 175, 80, 0.3)
  ) !important;
  box-shadow: 0 0 15px rgba(76, 175, 80, 0.4);
  border-color: rgba(76, 175, 80, 0.5) !important;
  transform: translateY(-3px);
}

.environment-info {
  margin-top: 15px;
  transition: all 0.3s ease;
}
</style>
