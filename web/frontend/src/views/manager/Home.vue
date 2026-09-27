<template>
  <div class="manager-home">
    <div class="welcome-card">
      您好，{{ user?.name }}！欢迎使用本系统
    </div>

    <div class="content-layout">
      <div class="notice-card">
        <div class="notice-title">公告列表</div>
        <div class="notice-content">
          <el-timeline reverse v-if="notices && notices.length">
            <el-timeline-item v-for="item in notices" :key="item.id" :timestamp="item.time">
              <el-popover
                  placement="right"
                  width="200"
                  trigger="hover"
                  :content="item.content">
                <template #reference>
                  <span>{{ item.title }}</span>
                </template>
              </el-popover>
            </el-timeline-item>
          </el-timeline>
          <div v-else class="empty-notice">暂无公告</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ManagerHome',
  data() {
    return {
      user: JSON.parse(localStorage.getItem('xm-user') || '{}'),
      notices: []
    }
  },
  created() {
    this.loadNotices()
  },
  methods: {
    loadNotices() {
      this.$request.get('/notice/selectAll').then(res => {
        this.notices = res.data || []
      }).catch(err => {
        console.error('加载公告失败:', err)
        this.notices = []
      })
    }
  }
}
</script>

<style lang="less" scoped>
.manager-home {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
}

.welcome-card {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  font-size: 16px;
  color: #333;
}

.content-layout {
  display: flex;
  gap: 20px;
}

.notice-card {
  flex: 1;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.notice-title {
  margin-bottom: 20px;
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.notice-content {
  position: relative;
  max-height: 500px;
  overflow-y: auto;
}

.empty-notice {
  text-align: center;
  color: #909399;
  padding: 20px 0;
}

/deep/.el-timeline {
  padding-left: 0;
}

/deep/.el-timeline-item__content {
  color: #666;
}

/deep/.el-timeline-item__timestamp {
  color: #999;
}

/deep/.el-popover {
  max-width: 300px;
}
</style>