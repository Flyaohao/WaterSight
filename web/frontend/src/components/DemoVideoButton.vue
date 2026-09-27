<template>
  <div class="demo-video-btn">
    <el-button type="primary" @click="showVideo" class="floating-btn">
      <i class="el-icon-video-camera"></i>
      观看示例
    </el-button>

    <!-- 视频对话框 -->
    <el-dialog
      title="功能演示视频"
      :visible.sync="dialogVisible"
      width="70%"
      custom-class="demo-video-dialog"
      :modal="false"
      :close-on-click-modal="false"
      :before-close="handleClose"
    >
      <div class="video-container">
        <video
          v-if="dialogVisible && videoSrc"
          :src="videoSrc"
          controls
          class="demo-video"
        >
          您的浏览器不支持视频播放
        </video>
      </div>
<!--      <span slot="footer" class="dialog-footer">-->
<!--        <el-button @click="dialogVisible = false">关闭</el-button>-->
<!--      </span>-->
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'DemoVideoButton',
  props: {
    videoUrl: {
      type: String,
      required: true
    }
  },
  computed: {
    videoSrc() {
      try {
        // 优先从本地 assets/videos 加载（该目录未随仓库分发，见 README「模型权重说明」）
        return require(`@/assets/videos/${this.videoUrl}`);
      } catch (e) {
        // 本地缺失时回退为外部地址，可在 .env 中配置 VUE_APP_DEMO_VIDEO_BASE
        const base = process.env.VUE_APP_DEMO_VIDEO_BASE || '';
        return `${base}${this.videoUrl}`;
      }
    }
  },
  data() {
    return {
      dialogVisible: false
    }
  },
  methods: {
    showVideo() {
      this.dialogVisible = true
    },
    handleClose(done) {
      done()
    }
  }
}
</script>

<style lang="less" scoped>
.demo-video-btn {
  position: fixed;
  top: 80px;
  right: 0px;
  z-index: 1000;
}

.floating-btn {
  background: linear-gradient(45deg, #00c6ff, #0072ff);
  border: none;
  padding: 10px 20px;
  border-radius: 10px;
  color: white;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 5px;
  box-shadow: 0 4px 15px rgba(0, 198, 255, 0.3);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 198, 255, 0.4);
    background: linear-gradient(45deg, #00d4ff, #0080ff);
  }

  i {
    font-size: 16px;
  }
}

/deep/ .demo-video-dialog {
  background: rgba(6, 25, 56, 0.95);
  border: 1px solid rgba(0, 198, 255, 0.15);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(20px);

  .el-dialog__header {
    padding: 20px;
    border-bottom: 1px solid rgba(0, 198, 255, 0.15);

    .el-dialog__title {
      color: #ffffff;
      font-size: 1.2rem;
    }

    .el-dialog__headerbtn .el-dialog__close {
      color: rgba(255, 255, 255, 0.7);
    }
  }

  .el-dialog__body {
    padding: 20px;
    background: rgba(0, 0, 0, 0.2);
  }

  .el-dialog__footer {
    border-top: 1px solid rgba(0, 198, 255, 0.15);
    padding: 15px 20px;
  }
}

.video-container {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 10px;
  overflow: hidden;
}

.demo-video {
  width: 100%;
  max-height: 70vh;
  object-fit: contain;
  background: #000;
}
</style> 