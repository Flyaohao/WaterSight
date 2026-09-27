<template>
  <div class="fish-yolo-container">
    <DemoVideoButton video-url="yolofish.mp4" />
    <!-- 工具说明组件 -->
    <tool-instructions
      title="水下鱼类智能识别系统"
      description="基于改进YOLOv5的水下鱼类智能识别系统，专门针对水下环境下的鱼类识别进行优化，支持13种常见观赏鱼类的实时精确识别。系统集成了鱼类行为分析、种群统计和生态评估等功能，为水族馆管理和海洋生态研究提供专业支持。"
      :features="[
        '多目标检测：同时识别多个鱼类目标',
        '场景适应：可在不同水下环境和光照条件识别',
        '鱼种百科：集成13种常见观赏鱼类的基本信息',
        '结果导出：支持检测结果图片一键保存与分享',
      ]"
      :formats="[
        '图片格式：JPG、PNG（≤20MB）',
        '视频格式：MP4（≤100MB，限30秒）',
        '分辨率：建议1080P以上',
        '拍摄要求：光照充足，画面稳定'
      ]"
      :steps="[
        '选择文件：上传图片或视频文件',
        '自动分析：系统进行目标检测',
        '结果展示：显示识别结果和统计信息',
        '详情查看：获取每种鱼类的详细信息'
      ]"
      :notes="[
        '当前支持识别的鱼类：神仙鱼、蓝倒吊、蝴蝶鱼、小丑鱼等13种观赏鱼类',
        '建议在水质清澈、光照充足的环境下拍摄',
        '避免快速移动导致画面模糊',
        '单个画面建议不超过10条鱼'
      ]"
      :advantages="[
        {
          title: '识别精度高',
          description: '针对水下环境优化，识别准确率达95%以上，支持复杂场景的多目标检测'
        },
        {
          title: '处理速度快',
          description: '采用改进YOLOv5架构，实现毫秒级的检测响应，支持实时视频分析'
        },
        {
          title: '功能丰富',
          description: '集成鱼类百科知识库，提供专业的生态信息和养护建议'
        },
        {
          title: '水下环境适应',
          description:
            '通过特殊的预处理和数据增强技术，有效应对水下光照变化和模糊问题',
        }
      ]"
    />

    <div class="content">
      <div class="detect-container">
        <div class="detection-card">
          <div class="upload-section">
            <h2>鱼类目标识别</h2>

            <!-- 支持的鱼类提示 -->
            <div class="support-info">
              <h3>目前支持识别的鱼类（13种）：</h3>
              <div class="fish-types">
                <span>神仙鱼</span>
                <span>蓝倒吊</span>
                <span>蝴蝶鱼</span>
                <span>小丑鱼</span>
                <span>金鱼</span>
                <span>斗鱼</span>
                <span>摩里斯神仙</span>
                <span>剑尾鱼</span>
                <span>条纹甜唇鱼</span>
                <span>三带雀鲷</span>
                <span>黄丽鱼</span>
                <span>黄燕尾鱼</span>
                <span>斑马鱼</span>
              </div>
            </div>

            <!-- 上传区域 -->
            <el-upload
              v-if="!detections && !loading"
              class="upload-area"
              drag
              action="#"
              :http-request="uploadImage"
              :show-file-list="false"
              :before-upload="beforeUpload"
              accept="image/*"
            >
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">
                将图片拖到此处，或<em>点击上传</em>
              </div>
              <div class="el-upload__tip" slot="tip">
                支持上传jpg/png格式图片，仅支持识别以上13种鱼类
              </div>
            </el-upload>

            <!-- 处理进度条 -->
            <div v-if="loading" class="processing-status">
              <el-progress
                type="circle"
                :percentage="processingProgress"
              ></el-progress>
              <p>正在进行目标识别...</p>
            </div>

            <!-- 识别结果 -->
            <div v-if="detections" class="detection-results">
              <div class="action-bar">
                <el-upload
                  class="upload-button"
                  action="#"
                  :show-file-list="false"
                  :http-request="uploadImage"
                  :before-upload="beforeUpload"
                  accept="image/*"
                >
                  <el-button size="small" type="primary">
                    <i class="el-icon-upload2"></i>
                    上传新图片
                  </el-button>
                </el-upload>
              </div>

              <!-- 检测结果表格 -->
              <el-card class="detection-summary">
                <div slot="header">
                  <span>检测结果统计</span>
                </div>
                <el-table :data="detectionsTable" style="width: 100%">
                  <el-table-column
                    prop="fish_en"
                    label="鱼类(英文)"
                  ></el-table-column>
                  <el-table-column
                    prop="fish_zh"
                    label="鱼类(中文)"
                  ></el-table-column>
                  <el-table-column prop="count" label="数量"></el-table-column>
                  <el-table-column prop="confidence" label="置信度">
                    <template slot-scope="scope">
                      {{ (scope.row.confidence * 100).toFixed(1) }}%
                    </template>
                  </el-table-column>
                  <el-table-column prop="iou" label="IOU" v-if="hasIouScores">
                    <template slot-scope="scope">
                      {{
                        scope.row.iou
                          ? (scope.row.iou * 100).toFixed(1) + "%"
                          : "-"
                      }}
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" width="120">
                    <template slot-scope="scope">
                      <el-button
                        type="text"
                        size="small"
                        @click="showDetails(scope.row.fish_en)"
                      >
                        查看详情
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>

              <!-- 预览区域 -->
              <div class="preview-and-result">
                <div class="preview-container">
                  <h4>原始图片</h4>
                  <img :src="originalImage" alt="原始图片" />
                </div>
                <div class="result-container">
                  <h4>识别结果</h4>
                  <img :src="resultImage" alt="识别结果" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 鱼类详情对话框 -->
        <el-dialog
          title="  "
          custom-class="fish-detail-dialog"
          :visible.sync="detailsDialogVisible"
          width="60%"
          :close-on-click-modal="false"
          @open="handleDialogOpen"
        >
          <div class="dialog-header">
            <div class="species-name">
              <h2>{{ currentDetails.name }}</h2>
              <span class="name-en">{{ currentDetails.name_en }}</span>
            </div>
            <el-tag :type="getDifficultyType" effect="dark">
              {{ currentDetails.difficulty }}
            </el-tag>
          </div>
          <div class="fish-details" v-if="currentDetails">
            <el-tabs v-model="activeTab" class="detail-tabs">
              <el-tab-pane label="基本信息" name="basic">
                <div class="detail-section">
                  <div class="detail-item">
                    <h4><i class="el-icon-info"></i>物种描述</h4>
                    <p>{{ currentDetails.description }}</p>
                  </div>
                </div>
              </el-tab-pane>

              <el-tab-pane label="饲养指南" name="care">
                <div class="detail-section">
                  <div class="care-tips">
                    <h4><i class="el-icon-warning-outline"></i>饲养建议</h4>
                    <div
                      v-for="(tip, index) in parsedCareGuide.tips"
                      :key="index"
                      class="tip-item"
                    >
                      {{ tip }}
                    </div>
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script>
import request from "@/utils/request";
import ToolInstructions from "@/components/ToolInstructions.vue";
import DemoVideoButton from "@/components/DemoVideoButton.vue";

export default {
  name: "FishYolo",
  components: {
    ToolInstructions,
    DemoVideoButton,
  },
  data() {
    return {
      originalImage: "",
      resultImage: "",
      loading: false,
      detections: null,
      fishDetails: null,
      detailsDialogVisible: false,
      currentDetails: {},
      activeTab: "basic",
      parsedCareGuide: {},
      processingProgress: 0,
      progressTimer: null,
    };
  },
  computed: {
    detectionsTable() {
      if (!this.detections) return [];
      return Object.entries(this.detections).map(([fish, info]) => ({
        fish_en: fish,
        fish_zh: info.name_zh,
        count: info.count,
        confidence: info.confidence,
        iou: info.iou,
      }));
    },
    hasIouScores() {
      return this.detectionsTable.some((row) => row.iou != null);
    },
    getDifficultyType() {
      const difficultyMap = {
        简单: "success",
        中等: "warning",
        较难: "danger",
        专业: "danger",
      };
      return difficultyMap[this.currentDetails.difficulty] || "info";
    },
  },
  methods: {
    beforeUpload(file) {
      // 检查文件类型
      const isImage = file.type.startsWith("image/");
      if (!isImage) {
        this.$message.error("只能上传图片文件!");
        return false;
      }

      // 检查文件大小（限制为10MB）
      const isLt10M = file.size / 1024 / 1024 < 10;
      if (!isLt10M) {
        this.$message.error("图片大小不能超过 10MB!");
        return false;
      }

      // 预处理图片
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
          const img = new Image();
          img.onload = () => {
            // 检查图片尺寸
            if (img.width > 1920 || img.height > 1080) {
              // 创建canvas进行压缩
              const canvas = document.createElement("canvas");
              let width = img.width;
              let height = img.height;

              // 保持宽高比进行缩放
              if (width > 1920) {
                height = Math.round((1920 * height) / width);
                width = 1920;
              }
              if (height > 1080) {
                width = Math.round((1080 * width) / height);
                height = 1080;
              }

              canvas.width = width;
              canvas.height = height;
              const ctx = canvas.getContext("2d");
              ctx.drawImage(img, 0, 0, width, height);

              // 转换为Blob
              canvas.toBlob(
                (blob) => {
                  resolve(new File([blob], file.name, { type: file.type }));
                },
                file.type,
                0.9
              );
            } else {
              resolve(file);
            }
          };
          img.src = e.target.result;
        };
        reader.readAsDataURL(file);
      });
    },
    uploadImage(options) {
      this.loading = true;
      this.processingProgress = 0;
      this.startProgressSimulation();
      this.detections = null;
      this.originalImage = "";
      this.resultImage = "";

      const formData = new FormData();
      formData.append("file", options.file);

      request({
        url: "/api/detection/fish",
        method: "post",
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
        .then((res) => {
          if (res.code === "200") {
            const data = res.data;
            this.detections = data.detections;
            this.fishDetails = data.details;
            
            // 使用环境变量或默认值获取Python服务URL
            const pythonServiceUrl = process.env.VUE_APP_PYTHON_URL || "http://localhost:8000";
            
            // 构建完整的图片URL
            this.originalImage = `${pythonServiceUrl}/uploads/${data.original
              .split("/")
              .pop()}`;
            this.resultImage = `${pythonServiceUrl}/results/${data.result
              .split("/")
              .pop()}`;
            
            console.log("图片路径:", {
              original: this.originalImage,
              result: this.resultImage,
            });
          } else {
            this.$message.error(res.msg || "检测失败");
          }
        })
        .catch((err) => {
          console.error("检测错误：", err);
          this.$message.error("检测失败：" + err.message);
        })
        .finally(() => {
          this.loading = false;
          this.stopProgressSimulation();
        });
    },
    showDetails(fishName) {
      if (this.fishDetails && this.fishDetails[fishName]) {
        this.currentDetails = this.fishDetails[fishName];
        this.detailsDialogVisible = true;
      }
    },
    handleDialogOpen() {
      this.activeTab = "basic";
      this.parseCareGuide();
    },
    parseCareGuide() {
      if (!this.currentDetails.care_guide) {
        this.parsedCareGuide = { parameters: {}, tips: [] };
        return;
      }

      const guide = this.currentDetails.care_guide;
      const parameters = {};
      const tips = [];

      const lines = guide
        .split("\n")
        .map((line) => line.trim())
        .filter((line) => line);

      lines.forEach((line) => {
        if (line.includes("：") || line.includes(":")) {
          const [key, value] = line.split(/[：:]/);
          parameters[key.trim()] = value.trim();
        } else if (line.startsWith("-")) {
          tips.push(line.substring(1).trim());
        }
      });

      this.parsedCareGuide = { parameters, tips };
    },
    startProgressSimulation() {
      this.processingProgress = 0;
      clearInterval(this.progressTimer);

      this.progressTimer = setInterval(() => {
        if (this.processingProgress < 90) {
          this.processingProgress += Math.random() * 10;
          if (this.processingProgress > 90) {
            this.processingProgress = 90;
          }
        }
      }, 500);
    },
    stopProgressSimulation() {
      clearInterval(this.progressTimer);
      this.processingProgress = 100;
    },
  },
  beforeDestroy() {
    clearInterval(this.progressTimer);
  },
};
</script>

<style lang="less" scoped>
.fish-yolo-container {
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

.detect-container {
  min-height: calc(100vh - 60px);
  max-height: calc(130vh - 60px);
  padding: 0;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow-y: auto;
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
  margin: 20px auto;
  background: rgba(6, 25, 56, 0.85);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 198, 255, 0.15);
  border-radius: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
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
  letter-spacing: 2px;
}

.detection-results {
  margin-top: 30px;
  overflow: visible;
}

.detection-summary {
  margin: 20px auto;
  max-width: 1000px;
  background: rgba(2, 17, 43, 0.7);
  border: 1px solid rgba(0, 198, 255, 0.15);
  border-radius: 15px;
  overflow: visible;
}

/deep/.el-card {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.9);
}

/deep/.el-card__header {
  border-bottom: 1px solid rgba(0, 198, 255, 0.15);
  padding: 15px 20px;
}

/deep/.el-table {
  background: transparent;
  color: rgba(255, 255, 255, 0.9);
}

/deep/.el-table tr,
/deep/.el-table th,
/deep/.el-table td {
  background: transparent;
  border-bottom: 1px solid rgba(0, 198, 255, 0.1);
}

/deep/.el-table--enable-row-hover .el-table__body tr:hover > td {
  background: rgba(0, 198, 255, 0.1);
}

/deep/.el-table th.is-leaf {
  background: rgba(0, 198, 255, 0.1);
  border-bottom: 1px solid rgba(0, 198, 255, 0.2);
}

/deep/.el-button--text {
  color: white;
}

/deep/.el-button--text:hover {
  color: orange;
}

.preview-and-result {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin: 30px auto;
  padding: 0 20px;
  max-width: 1000px;
}

.preview-container,
.result-container {
  background: rgba(2, 17, 43, 0.7);
  border: 1px solid rgba(0, 198, 255, 0.15);
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.preview-container h4,
.result-container h4 {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.preview-container img,
.result-container img {
  width: 400px;
  height: 400px;
  object-fit: contain;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.2);
}

.processing-status {
  margin: 40px auto;
  text-align: center;
  max-width: 200px;
}

.processing-status p {
  margin-top: 20px;
  color: #ffffff;
  font-size: 1.1rem;
}

.action-bar {
  margin: 20px 0;
  display: flex;
  justify-content: center;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .preview-container img,
  .result-container img {
    width: 350px;
    height: 350px;
  }
}

@media (max-width: 768px) {
  .preview-and-result {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .preview-container img,
  .result-container img {
    width: 300px;
    height: 300px;
  }
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

/* 修改进度条样式 */
/deep/.el-progress-circle {
  color: rgba(255, 255, 255, 0.9);
}

/* 鱼类详情对话框样式 */
/deep/.fish-detail-dialog {
  background: rgba(6, 25, 56, 0.95);
  border: 1px solid rgba(0, 198, 255, 0.15);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(20px);
}

/deep/.fish-detail-dialog .el-dialog__header {
  padding: 0;
  border-bottom: none;
}

/deep/.fish-detail-dialog .el-dialog__body {
  padding: 0 20px 30px;
  color: rgba(255, 255, 255, 0.9);
}

/deep/.fish-detail-dialog .el-dialog__headerbtn {
  top: 15px;
  right: 15px;
  z-index: 10;
}

/deep/.fish-detail-dialog .el-dialog__headerbtn .el-dialog__close {
  color: rgba(255, 255, 255, 0.7);
  font-size: 20px;
}

.dialog-header {
  padding: 25px 30px;
  background: linear-gradient(
    145deg,
    rgba(2, 17, 43, 0.8) 0%,
    rgba(6, 25, 56, 0.9) 100%
  );
  border-radius: 20px 20px 0 0;
  margin: 22px 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(0, 198, 255, 0.15);
}

.species-name {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.species-name h2 {
  margin: 0;
  font-size: 1.8rem;
  background: linear-gradient(120deg, #00c6ff, #0072ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.name-en {
  color: rgba(255, 255, 255, 0.6);
  font-size: 1rem;
  font-style: italic;
}

/deep/.el-tag {
  background: transparent;
  border: 1px solid;
  padding: 8px 15px;
  font-size: 0.9rem;
  height: auto;
  line-height: 1.2;
}

.fish-details {
  padding: 20px;
}

.detail-section {
  padding: 20px;
}

.detail-item {
  background: rgba(2, 17, 43, 0.4);
  border: 1px solid rgba(0, 198, 255, 0.1);
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 20px;
}

.detail-item h4 {
  color: #00c6ff;
  font-size: 1.1rem;
  margin: 0 0 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-item p {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin: 0;
}

.care-tips {
  background: rgba(2, 17, 43, 0.4);
  border: 1px solid rgba(0, 198, 255, 0.1);
  border-radius: 15px;
  padding: 20px;
}

.care-tips h4 {
  color: #00c6ff;
  font-size: 1.1rem;
  margin: 0 0 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tip-item {
  color: rgba(255, 255, 255, 0.8);
  margin: 10px 0;
  line-height: 1.5;
}

/deep/.detail-tabs .el-tabs__header {
  background: transparent;
  border-bottom: 1px solid rgba(0, 198, 255, 0.15);
  margin: 0;
  padding: 0;
}

/deep/.detail-tabs .el-tabs__item {
  color: rgba(255, 255, 255, 0.6);
  font-size: 1rem;
  padding: 15px 20px;
}

/deep/.detail-tabs .el-tabs__item.is-active {
  color: #00c6ff;
}

/deep/.detail-tabs .el-tabs__active-bar {
  background-color: #00c6ff;
  height: 2px;
}

.support-info {
  margin: 20px auto;
  max-width: 800px;
  padding: 20px;
  background: rgba(2, 17, 43, 0.7);
  border: 1px solid rgba(0, 198, 255, 0.15);
  border-radius: 15px;
  text-align: center;
}

.support-info h3 {
  color: #00c6ff;
  font-size: 1.2rem;
  margin-bottom: 15px;
}

.fish-types {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.fish-types span {
  background: rgba(0, 198, 255, 0.1);
  border: 1px solid rgba(0, 198, 255, 0.2);
  padding: 5px 15px;
  border-radius: 20px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.fish-types span:hover {
  background: rgba(0, 198, 255, 0.2);
  transform: translateY(-2px);
}
</style>
