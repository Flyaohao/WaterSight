<template>
  <div class="main-content">
    <!-- 返回按钮 -->
    <div class="back-button" @click="goBack">
      <i class="el-icon-arrow-left"></i>
      返回
    </div>

    <div class="activity-container">
      <div class="card activity-header">
        <div class="activity-content">
          <img :src="activity.cover" alt="" class="activity-cover" />
          <div class="activity-info">
            <div class="activity-title">{{ activity.name }}</div>
            <div class="activity-desc">{{ activity.descr }}</div>
            <div class="activity-meta">
              <i class="el-icon-date"></i> 时间
              <span>{{ activity.start }} ~ {{ activity.end }}</span>
            </div>
            <div class="activity-meta">
              <i class="el-icon-location"></i> 地址
              <a
                class="activity-link"
                :href="activity.address"
                v-if="activity.form === '线上'"
                >{{ activity.address }}</a
              >
              <span v-else>{{ activity.address }}</span>
              <el-tag type="primary" size="mini">{{ activity.form }}</el-tag>
            </div>

            <div class="activity-actions">
              <div class="action-buttons">
                <el-button
                  type="primary"
                  @click="sign"
                  v-if="!activity.isSign && !activity.isEnd"
                  >报名参加</el-button
                >
                <el-button
                  type="info"
                  @click="cancel"
                  v-if="activity.isSign && !activity.isEnd"
                  >取消报名</el-button
                >
                <el-button type="info" disabled v-if="activity.isEnd"
                  >活动已结束</el-button
                >
              </div>
              <div class="activity-stats">
                <div
                  class="stat-item"
                  @click="setLikes"
                  :class="{ active: activity.userLike }"
                >
                  <i class="el-icon-thumb"></i>
                  <span>{{ activity.likesCount }}</span>
                </div>
                <div
                  class="stat-item"
                  @click="setCollect"
                  :class="{ active: activity.userCollect }"
                >
                  <i class="el-icon-star-on"></i>
                  <span>{{ activity.collectCount }}</span>
                </div>
                <div class="stat-item">
                  <i class="el-icon-view"></i>
                  <span>{{ activity.readCount }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card activity-detail">
        <div class="detail-title">活动详情</div>
        <div class="w-e-text">
          <div v-html="activity.content"></div>
        </div>
      </div>

      <div class="activity-comments">
        <Comment :fid="activityId" module="活动" />
      </div>
    </div>
  </div>
</template>

<script>
import Comment from "@/components/Comment";
import request from "@/utils/request";
import moment from "moment";

export default {
  name: "ActivityDetail",
  components: {
    Comment,
  },
  data() {
    return {
      activityId: this.$route.query.activityId,
      activity: {},
      user: JSON.parse(localStorage.getItem("xm-user") || "{}"),
    };
  },
  created() {
    this.checkLogin();
    if (this.user.token) {
      this.load();
    }
  },
  methods: {
    checkLogin() {
      if (!this.user.token) {
        this.$confirm("请先登录后再查看详情", "提示", {
          confirmButtonText: "去登录",
          cancelButtonText: "返回首页",
          type: "warning",
          closeOnClickModal: false,
          closeOnPressEscape: false,
          showClose: false,
        })
          .then(() => {
            this.$router.push("/login");
          })
          .catch(() => {
            this.$router.push("/front/home");
          });
      }
    },
    load() {
      this.$request
        .get("/activity/selectById/" + this.activityId)
        .then((res) => {
          if (res.code === "200") {
            this.activity = res.data || {};
            this.updateReadCount();
          } else {
            this.$message.error(res.msg || "获取活动详情失败");
          }
        })
        .catch(() => {
          this.$router.push("/front/home");
        });
    },
    updateReadCount() {
      // 直接更新浏览量，参考博客的实现方式
      this.$request
        .put(`/activity/updateReadCount/${this.activityId}`)
        .then(() => {
          console.log("活动浏览量更新成功");
          // 不需要手动更新前端显示，下次加载时会自动更新
        })
        .catch((error) => {
          console.error("活动浏览量更新失败:", error);
        });
    },
    setLikes() {
      /*      if (!this.user.token) {
        this.$message.warning('请先登录')
        return
      }
      this.$request.post('/likes/set', { fid: this.activityId, module: '活动' }).then(res => {
        if (res.code === '200') {
          this.$message.success('点赞成功')
          this.load()
        }
      })*/
      if (!this.user.token) {
        this.$message.warning("请先登录");
        return;
      }

      this.$request
        .post("/likes/set", { fid: this.activityId, module: "活动" })
        .then((res) => {
          if (res.code === "200") {
            this.activity.userLike = res.data; // res.data 为 true 表示收藏，false 表示取消收藏
            const message1 = this.activity.userLike
              ? "点赞成功"
              : "取消点赞成功";
            this.$message.success(message1);

            this.load();
          }
        })
        .catch((error) => {
          console.error("请求失败:", error);
          this.$message.error("操作失败，请稍后重试");
        });
    },
    setCollect() {
      if (!this.user.token) {
        this.$message.warning("请先登录");
        return;
      }

      this.$request
        .post("/collect/set", { fid: this.activityId, module: "活动" })
        .then((res) => {
          if (res.code === "200") {
            // 根据后端返回的数据更新 userCollect 状态
            this.activity.userCollect = res.data; // res.data 为 true 表示收藏，false 表示取消收藏
            const message2 = this.activity.userCollect
              ? "收藏成功"
              : "取消收藏成功";
            this.$message.success(message2);

            this.load();
          }
        })
        .catch((error) => {
          console.error("请求失败:", error);
          this.$message.error("操作失败，请稍后重试");
        });
    },
    sign() {
      if (!this.user.token) {
        this.$message.warning("请先登录");
        return;
      }
      this.$request
        .post("/activitySign/add", { activityId: this.activityId })
        .then((res) => {
          if (res.code === "200") {
            this.$message.success("报名成功");
            this.load();
          } else {
            this.$message.error(res.msg);
          }
        });
    },
    cancel() {
      this.$confirm("您确定取消报名吗？", "确认取消", { type: "warning" })
        .then((response) => {
          this.$request
            .delete(
              "/activitySign/delete/user/" +
                this.activityId +
                "/" +
                this.user.id
            )
            .then((res) => {
              if (res.code === "200") {
                this.$message.success("操作成功");
                this.load();
              } else {
                this.$message.error(res.msg);
              }
            });
        })
        .catch(() => {});
    },
    goBack() {
      if (window.history.length <= 1) {
        this.$message.info("没有上一页了哦");
        return;
      }
      this.$router.go(-1);
    },
  },
  watch: {
    user: {
      handler(newVal) {
        if (!newVal.token) {
          this.checkLogin();
        }
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
.main-content {
  position: relative;
  min-height: 100vh;
  background-color: var(--bg-color);
  background-image: linear-gradient(
      135deg,
      var(--bg-gradient-light) 0%,
      var(--bg-gradient-dark) 100%
    ),
    url("https://images.unsplash.com/photo-1551244072-5d12893278ab?q=80&w=2070");
  background-attachment: fixed;
  background-size: cover;
}

.back-button {
  position: fixed;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  background-color: var(--bg-color-secondary);
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 0 10px var(--shadow-color);
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  color: var(--text-color-regular);
  font-size: 14px;
  z-index: 999;
}

.back-button:hover {
  background-color: var(--bg-color-hover);
  transform: translateY(-50%) translateX(5px);
}

.back-button i {
  margin-right: 5px;
  font-size: 16px;
}

.activity-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.activity-header {
  margin-bottom: 20px;
  padding: 20px;
}

.activity-content {
  display: flex;
  gap: 30px;
}

.activity-cover {
  width: auto;
  height: 250px;
  border-radius: 8px;
  object-fit: cover;
}

.activity-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.activity-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 15px;
  color: var(--text-color-primary);
}

.activity-desc {
  color: var(--text-color-regular);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 20px;
  text-align: justify;
}

.activity-meta {
  color: var(--text-color-regular);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.activity-link {
  color: var(--primary-color);
  text-decoration: none;
}

.activity-link:hover {
  color: var(--primary-color-hover);
}

.activity-actions {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.activity-stats {
  display: flex;
  gap: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 5px;
  color: var(--text-color-regular);
  cursor: pointer;
  transition: all 0.3s;
  padding: 8px 12px;
  border-radius: 4px;
}

.stat-item:hover {
  background-color: var(--bg-color-hover);
}

.stat-item.active {
  color: var(--primary-color);
}

.stat-item i {
  font-size: 18px;
}

.activity-detail {
  margin-bottom: 20px;
  padding: 20px;
}

.detail-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
  padding-left: 10px;
  border-left: 4px solid var(--primary-color);
  color: var(--text-color-primary);
}

.activity-comments {
  margin-bottom: 20px;
}

.el-tag {
  margin-left: 8px;
}

.fish-container {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  z-index: 100;
  pointer-events: none;
}

.card {
  background-color: var(--bg-color-secondary);
  border-radius: 8px;
  box-shadow: 0 2px 12px var(--shadow-color);
  margin-bottom: 20px;
}

.w-e-text {
  color: var(--text-color-primary) !important;
  background-color: var(--bg-color-secondary) !important;
}

.w-e-text * {
  color: var(--text-color-primary) !important;
}

.w-e-text pre {
  background-color: var(--code-bg-color) !important;
  border: 1px solid var(--border-color) !important;
}

.w-e-text code {
  color: var(--code-text-color) !important;
  background-color: var(--code-bg-color) !important;
}

.w-e-text blockquote {
  border-left: 4px solid var(--border-color) !important;
  background-color: var(--blockquote-bg-color) !important;
  color: var(--text-color-regular) !important;
}
</style>
