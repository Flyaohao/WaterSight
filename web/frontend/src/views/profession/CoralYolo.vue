<template>
  <div class="coral-yolo-container">
    <DemoVideoButton video-url="yolo2.mp4" />
    <!-- 工具说明组件 -->
    <tool-instructions
      title="珊瑚礁健康监测系统"
      description="基于改进YOLOv5的水下珊瑚礁监测系统，专注于珊瑚生态威胁评估。系统可实时识别珊瑚，评估其健康状况，并对棘冠海星等威胁生物进行智能预警，为珊瑚礁保护提供科技支持。"
      :features="[
        '威胁检测：自动识别棘冠海星等危害生物',
        '位置识别：精准检测珊瑚礁表面海星的分布位置与密度',
        '健康评估：对珊瑚礁受侵害程度进行监测',
        '保卫环境：为及时开展海星清除工作提供支持',
      ]"
      :formats="[
        '图片格式：JPG、PNG（≤20MB）',
        '视频格式：MP4（≤100MB）',
        '分辨率要求：建议2K以上',
        '拍摄要求：水质清澈，光照均匀'
      ]"
      :steps="[
        '上传图片：选择需要分析的水下图片',
        '自动检测：系统进行多目标识别',
        '威胁分析：评估潜在生态威胁',
        '生成报告：输出详细分析结果'
      ]"
      :notes="[
        '适合清晰的水下环境拍摄',
        '建议使用专业水下相机',
        '避免浑浊或背光环境',
        '保持适当观察距离'
      ]"
      :advantages="[
       {
          title: '精准识别',
          description: '支持水下海星识别，准确率达90%以上，可靠性高',
        },
        {
          title: '智能预警',
          description: '检测棘冠海星等威胁，提供准确位置信息和处理建议',
        },
        {
          title: '优化处理',
          description: '显示海星数量统计，提供分布区域可视化展示',
        },
        {
          title: '环境适应',
          description: '适应不同水下光照和能见度条件下的海星识别',
        },
      ]"
    />

    <div class="content">
      <div class="detect-container">
        <div class="detection-card">
          <div class="upload-section">
            <h2>珊瑚礁健康监测系统</h2>

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
                支持上传jpg/png格式图片
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
                  <span style="color: white">检测结果统计</span>
                </div>
                <el-table :data="detectionsTable" style="width: 100%">
                  <el-table-column
                    prop="coral_en"
                    label="物种(英文)"
                  ></el-table-column>
                  <el-table-column
                    prop="coral_zh"
                    label="物种(中文)"
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
                        @click="showDetails(scope.row.coral_en)"
                      >
                        查看详情
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>

              <!-- 警告卡片 -->
              <el-card class="warning-card" v-if="hasStarfish">
                <template v-if="!captured">
                  <div
                    class="warning-header"
                    :class="{ 'warning-ignored': warningIgnored }"
                  >
                    <i class="el-icon-warning"></i>
                    <span>警告：发现危害珊瑚礁生物</span>
                  </div>
                  <div
                    class="warning-content"
                    :class="{ 'warning-ignored': warningIgnored }"
                  >
                    <p class="warning-text">
                      <span class="warning-highlight"
                        >检测到 {{ detections["starfish"].count }} 个海星</span
                      >
                      <template
                        v-if="
                          detections['positions'] &&
                          detections['positions'].length
                        "
                      >
                        <br />具体位置：
                        <span
                          v-for="(pos, index) in detections['positions']"
                          :key="index"
                        >
                          {{ index + 1 }}号海星位于图片{{ pos }}部
                          {{
                            index < detections["positions"].length - 1
                              ? "；"
                              : ""
                          }}
                        </span>
                      </template>
                    </p>
                    <div class="warning-action">
                      <div class="action-header">
                        <i class="el-icon-warning-outline"></i>
                        <span>需要立即采取的行动：</span>
                      </div>
                      <div class="action-steps">
                        <div class="step">
<!--                          <span class="step-number">1.</span>-->
                          <div class="step-content">
                            <h5>紧急清理</h5>
                            <p>
                              立即派遣工作人员前往标记位置清除海星，避免对珊瑚造成进一步伤害。
                            </p>
                          </div>
                        </div>
                        <div class="step">
<!--                          <span class="step-number">2.</span>-->
                          <div class="step-content">
                            <h5>记录情况</h5>
                            <p>
                              详细记录海星数量、位置和周边珊瑚受损情况，建立监测档案。
                            </p>
                          </div>
                        </div>
                        <div class="step">
<!--                          <span class="step-number">3.</span>-->
                          <div class="step-content">
                            <h5>后续跟进</h5>
                            <p>
                              安排定期巡查，防止海星再次聚集，评估珊瑚恢复情况。
                            </p>
                          </div>
                        </div>
                      </div>
                      <div class="emergency-contact">
                        <i class="el-icon-phone-outline"></i>
                        紧急联系：0123-4567890
                      </div>
                      <div class="action-buttons">
                        <el-button type="success" @click="handleCapture">
                          <i class="el-icon-check"></i>
                          捉捕完毕
                        </el-button>
                        <el-button
                          v-if="!warningIgnored"
                          type="info"
                          @click="handleIgnore"
                        >
                          <i class="el-icon-close"></i>
                          忽略警告
                        </el-button>
                      </div>
                    </div>
                  </div>
                </template>
                <template v-else>
                  <div class="thanks-content">
                    <h3 class="thanks-title">感谢您的贡献！</h3>
                    <div class="thanks-info">
                      <div class="info-section">
                        <h4>海星对珊瑚的危害</h4>
                        <p>
                          棘冠海星是珊瑚礁生态系统中最具破坏性的捕食者之一。一只成年棘冠海星每天可以消耗多达6平方米的珊瑚。它们会分泌消化酶溶解珊瑚组织，导致珊瑚白化和死亡。
                        </p>
                      </div>
                      <div class="info-section">
                        <h4>危害数据</h4>
                        <ul>
                          <li>每年造成珊瑚礁面积减少约5-10%</li>
                          <li>过去30年导致大堡礁40%的珊瑚覆盖率损失</li>
                          <li>单个爆发可影响数平方公里的珊瑚礁区域</li>
                        </ul>
                      </div>
                      <div class="info-section highlight">
                        <h4>您的贡献</h4>
                        <p>
                          通过及时发现和清除海星，您帮助保护了珊瑚礁生态系统的健康。这不仅维护了海洋生物的多样性，也为子孙后代保护了这片美丽的海底花园。
                        </p>
                      </div>
                    </div>
                  </div>
                </template>
              </el-card>

              <!-- 图片显示区域 -->
              <div class="preview-section">
                <div class="preview-item">
                  <h4>原始图片</h4>
                  <div class="image-container">
                    <el-image
                      :src="originalImage"
                      v-if="originalImage"
                      :preview-src-list="[originalImage]"
                      fit="contain"
                    >
                    </el-image>
                  </div>
                </div>
                <div class="preview-item">
                  <h4>检测结果</h4>
                  <div class="image-container">
                    <el-image
                      :src="resultImage"
                      v-if="resultImage"
                      :preview-src-list="[resultImage]"
                      fit="contain"
                    >
                    </el-image>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 详情对话框 -->
      <el-dialog
        :visible.sync="detailsDialogVisible"
        custom-class="coral-detail-dialog"
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
        <div class="coral-details" v-if="currentDetails">
          <el-tabs v-model="activeTab" class="detail-tabs">
            <el-tab-pane label="基本信息" name="basic">
              <div class="detail-section">
                <div class="detail-item">
                  <h4><i class="el-icon-info"></i>物种描述</h4>
                  <p>{{ currentDetails.description }}</p>
                </div>
                <div class="detail-item">
                  <h4><i class="el-icon-location"></i>栖息地</h4>
                  <p>{{ currentDetails.habitat }}</p>
                </div>
              </div>
            </el-tab-pane>

            <el-tab-pane label="生态信息" name="ecology">
              <div class="detail-section">
                <div class="detail-item">
                  <h4><i class="el-icon-connection"></i>生态作用</h4>
                  <p>{{ currentDetails.ecological_role }}</p>
                </div>
                <div class="detail-item">
                  <h4><i class="el-icon-warning"></i>保护状态</h4>
                  <p>{{ currentDetails.conservation_status }}</p>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import request from "@/utils/request";
import ToolInstructions from "@/components/ToolInstructions.vue";
import DemoVideoButton from "@/components/DemoVideoButton.vue";

export default {
  name: "CoralYolo",
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
      coralDetails: null,
      detailsDialogVisible: false,
      currentDetails: {},
      activeTab: "basic",
      dialogVisible: false,
      processingProgress: 0,
      progressTimer: null,
      warningIgnored: false,
      showSuccessAnimation: false,
      captured: false,
    };
  },
  computed: {
    detectionsTable() {
      if (!this.detections) return [];
      // 过滤掉 positions 字段，只显示实际检测结果
      const entries = Object.entries(this.detections).filter(
        ([key]) => key !== "positions"
      );
      return entries.map(([coral, info]) => ({
        coral_en: coral,
        coral_zh: info.name_zh,
        count: info.count,
        confidence: info.confidence,
        iou: info.iou,
      }));
    },
    hasIouScores() {
      return this.detectionsTable.some((row) => row.iou != null);
    },
    hasStarfish() {
      return (
        this.detections &&
        this.detections["starfish"] &&
        this.detections["starfish"].count > 0
      );
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
    parsedCareGuide() {
      if (!this.currentDetails.care_guide) return { parameters: {}, tips: [] };

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

      return { parameters, tips };
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
      // 重置警告框状态
      this.captured = false;
      this.warningIgnored = false;

      const formData = new FormData();
      formData.append("file", options.file);

      request({
        url: "/api/detection/shanhu",
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
            this.coralDetails = data.details;
            
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
    showDetails(coralName) {
      if (this.coralDetails && this.coralDetails[coralName]) {
        this.currentDetails = this.coralDetails[coralName];
        this.detailsDialogVisible = true;
      }
    },
    formatPositions(positions) {
      if (!positions || positions.length === 0) return "";
      return positions.map((pos, index) => `${pos}部`).join("、");
    },
    handleDialogOpen() {
      this.activeTab = "basic";
    },
    handleCapture() {
      this.captured = true;
      this.showSuccessAnimation = true;
      this.$notify({
        title: "感谢您的贡献！",
        message: "谢谢你为保护珊瑚贡献了力量！",
        type: "success",
        duration: 3000,
        customClass: "success-notification",
      });
      setTimeout(() => {
        this.showSuccessAnimation = false;
      }, 3000);
    },
    handleIgnore() {
      this.warningIgnored = true;
    },
  },
  beforeDestroy() {
    clearInterval(this.progressTimer);
  },
};
</script>

<style lang="less" scoped>
.coral-yolo-container {
  min-height: 100vh;
  background: #05050596;
  padding: 60px 0;  /* 添加上下padding，避免被导航栏遮住 */
  display: flex;
  flex-direction: column;
}

.detect-container {
  flex: 1;
  padding: 20px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 20px auto;  /* 添加外边距 */
  max-width: 1400px;  /* 限制最大宽度 */
}

.detection-card {
  position: relative;
  z-index: 1;
  width: 100%;
  margin: 0 auto;
  background: rgba(6, 25, 56, 0.85);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 198, 255, 0.15);
  border-radius: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.upload-section {
  padding: 100px;
  text-align: center;
}

.upload-section h2 {
  font-size: 2.5rem;
  margin-bottom: 30px;
  background: linear-gradient(120deg, #00c6ff, #0072ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
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
  transition: all 0.3s ease;
}

.upload-area:hover {
  border-color: rgba(0, 198, 255, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
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

.detection-results {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.preview-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  max-width: 1000px;
}

.preview-item {
  background: rgba(2, 17, 43, 0.7);
  border: 1px solid rgba(0, 198, 255, 0.15);
  border-radius: 15px;
  padding: 20px;
  text-align: center;
}

.preview-item h4 {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.image-container {
  width: 500px;
  height: 400px;
  margin: 0 auto;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-container /deep/.el-image {
  width: 100%;
  height: 100%;
}

.image-container /deep/.el-image__inner {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.warning-card {
  margin: 0 auto;
  max-width: 1000px;
  background: rgba(2, 17, 43, 0.7);
  transition: all 0.3s ease;
}

.detection-summary {
  margin: 0 auto;
  max-width: 1000px;
  background: rgba(2, 17, 43, 0.7);

  /deep/ .el-table {
    background-color: transparent;
    color: rgb(255, 255, 255);
    
    &::before {
      display: none;
    }
    
    th {
      background-color: rgba(0, 0, 0, 0.6);
      color: rgb(255, 255, 255);
      border-bottom: 1px solid rgb(3, 3, 3);
    }
    
    td {
      background-color: rgba(2, 17, 43, 0.4);
      border-bottom: 1px solid rgb(35, 36, 36);
    }

    tr.el-table__row:hover > td {
      background-color: rgba(2, 17, 43, 0.4) !important;
    }
    
    .el-button--text {
      color: rgba(255, 255, 255, 0.8);
      
      &:hover {
        color: #ff0000;
      }
    }
  }
}

@media (max-width: 1200px) {
  .detect-container {
    padding: 15px;
    margin: 15px auto;
  }
}

@media (max-width: 768px) {
  .coral-yolo-container {
    padding: 50px 0;
  }
  
  .detect-container {
    padding: 10px;
    margin: 10px auto;
  }
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

.detection-summary,
.warning-card {
  width: 100%;
  max-width: none;
  margin: 0;
}

.warning-card {
  background: rgba(2, 17, 43, 0.7);
  transition: all 0.3s ease;
}

.warning-header {
  text-align: center;
  color: #ff4d4f;
  font-size: 1.3rem;
  font-weight: bold;
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

.warning-header i {
  margin-right: 8px;
  font-size: 1.4rem;
}

.warning-content {
  color: rgba(255, 255, 255, 0.9);
}

.warning-highlight {
  color: #ff4d4f;
  font-weight: bold;
  font-size: 1.2rem;
}

.action-header {
  text-align: center;
  color: #ff4d4f;
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 20px;
}

.action-steps {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 0 20px;
}

.step {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  color: rgba(255, 255, 255, 0.9);
}

.step-number {
  color: #ff4d4f;
  font-weight: bold;
  font-size: 1.1rem;
  min-width: 25px;
}

.step-content {
  flex: 1;
}

.step-content h5 {
  color: #00c6ff;
  font-size: 1.1rem;
  margin: 0 0 8px;
}

.step-content p {
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.5;
  margin: 0;
}

.emergency-contact {
  text-align: center;
  color: #00c6ff;
  font-size: 1.1rem;
  margin: 20px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.warning-text {
  text-align: center;
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.1rem;
  margin-bottom: 20px;
}

/* 详情对话框样式 */
/deep/.coral-detail-dialog {
  background: rgba(6, 25, 56, 0.95);
  border: 1px solid rgba(0, 198, 255, 0.15);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(20px);
}

.dialog-header {
  padding: 25px 30px;
  background: linear-gradient(
    145deg,
    rgba(2, 17, 43, 0.8) 0%,
    rgba(6, 25, 56, 0.9) 100%
  );
  border-radius: 20px 20px 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(0, 198, 255, 0.15);
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
}

.success-notification {
  background: linear-gradient(145deg, #52c41a, #73d13d);
  border: none;
  color: white;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.action-buttons .el-button {
  padding: 12px 30px;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.action-buttons .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.action-buttons .el-button i {
  font-size: 1.2rem;
}

/deep/.el-notification {
  background: rgba(6, 25, 56, 0.95);
  border: 1px solid rgba(0, 198, 255, 0.15);
  border-radius: 12px;
  backdrop-filter: blur(20px);
}

/deep/.el-notification__title {
  color: #fff;
  font-size: 1.2rem;
}

/deep/.el-notification__content {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.1rem;
}

.thanks-content {
  padding: 30px;
  color: rgba(255, 255, 255, 0.9);
}

.thanks-title {
  text-align: center;
  font-size: 1.8rem;
  color: #52c41a;
  margin-bottom: 30px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.thanks-info {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.info-section {
  background: rgba(2, 17, 43, 0.4);
  border: 1px solid rgba(0, 198, 255, 0.15);
  border-radius: 15px;
  padding: 20px;
}

.info-section h4 {
  color: #00c6ff;
  font-size: 1.2rem;
  margin-bottom: 15px;
}

.info-section p {
  line-height: 1.6;
  margin: 0;
}

.info-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.info-section li {
  position: relative;
  padding-left: 20px;
  margin-bottom: 10px;
  line-height: 1.5;
}

.info-section li::before {
  content: "•";
  color: #00c6ff;
  position: absolute;
  left: 0;
}

.info-section.highlight {
  background: rgba(82, 196, 26, 0.1);
  border-color: rgba(82, 196, 26, 0.3);
}

.info-section.highlight h4 {
  color: #52c41a;
}

.warning-header.warning-ignored,
.warning-content.warning-ignored .warning-highlight,
.warning-content.warning-ignored .action-header,
.warning-content.warning-ignored .step-number {
  color: rgba(255, 255, 255, 0.9);
}

.warning-content.warning-ignored .warning-action {
  background: rgba(255, 255, 255, 0.1);
}
</style>
