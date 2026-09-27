<template>
  <div>
    <el-row :gutter="20" v-if="total">
      <el-col
        :xs="24"
        :sm="12"
        :md="span"
        :lg="span"
        v-for="item in tableData"
        :key="item.id"
      >
        <div class="activity-card" @click="handleActivityClick(item)">
          <div class="card-cover">
            <img
              :src="item.cover || defaultCover"
              alt=""
              @error="handleImageError"
            />
            <div class="activity-status" v-if="item.isEnd">已结束</div>
            <div class="activity-status signed" v-else-if="item.isSign">
              已报名
            </div>
          </div>
          <div class="card-content">
            <h3 class="activity-title">{{ item.name }}</h3>
            <div class="activity-time">
              <i class="el-icon-date"></i> {{ item.start }}
            </div>
            <div class="activity-footer">
              <el-button
                type="primary"
                size="small"
                v-if="!item.isEnd && !item.isSign"
                >立即报名</el-button
              >
              <span class="activity-location" v-if="item.address">
                <i class="el-icon-location"></i> {{ item.address }}
              </span>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
    <div class="empty-data" v-if="total === 0">暂无数据</div>
    <div class="pagination-wrapper" v-if="total">
      <el-pagination
        background
        @current-change="handleCurrentChange"
        @size-change="handleSizeChange"
        :current-page.sync="pageNum"
        :page-size="pageSize"
        :page-sizes="[12, 24, 36, 48]"
        :pager-count="5"
        layout="total, sizes, prev, pager, next"
        :total="total"
      >
      </el-pagination>
      <div class="jump-page">
        <span>前往</span>
        <el-input
          v-model.number="jumpPage"
          size="mini"
          style="width: 70px; margin: 0 5px"
          @keyup.enter.native="handleJumpPage"
        >
        </el-input>
        <span>页</span>
        <el-button
          size="mini"
          type="primary"
          @click="handleJumpPage"
          style="margin-left: 5px"
          >跳转</el-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import Footer from "@/components/Footer";
import LoginDialog from "@/components/LoginDialog";
import request from "@/utils/request";
import axios from "axios";

export default {
  name: "ActivityList",
  components: {
    Footer,
    LoginDialog,
  },
  props: {
    type: null,
    span: {
      type: Number,
      default: 6, // 默认值为6，表示一行显示4个活动卡片 (24/6=4)
    },
    customApi: {
      type: String,
      default: "",
    },
    customParams: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      tableData: [], // 所有的数据
      pageNum: 1, // 当前的页码
      pageSize: 12, // 每页显示12个活动
      total: 0,
      name: null,
      status: null, // 添加状态筛选字段
      isLogin: false,
      defaultCover:
        "https://tse1-mm.cn.bing.net/th/id/OIP-C.nODoTn--Oen-QCfMEiMoywHaEJ?w=284&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7", // 默认图片https://via.placeholder.com/300x150?text=No+Image

      jumpPage: 1,
    };
  },
  created() {
    this.load(1);
    this.checkLoginStatus();
  },
  methods: {
    checkLoginStatus() {
      const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
      this.isLogin = !!user.role;
    },
    handleActivityClick(item) {
      console.log("点击活动:", item);
      this.$router.push(`/front/activityDetail?activityId=${item.id}`);
    },
    handleImageError(e) {
      e.target.src = this.defaultCover;
    },
    async load(pageNum) {
      // 分页查询
      if (pageNum) this.pageNum = pageNum;

      let url;
      // 优先使用自定义 API
      if (this.customApi) {
        url = this.customApi;
      } else {
        // 如果没有自定义 API，使用默认逻辑
        switch (this.type) {
          case "user":
            url = "/activity/selectUser";
            break;
          case "like":
            url = "/activity/selectLike";
            break;
          case "collect":
            url = "/activity/selectCollect";
            break;
          default:
            url = "/activity/selectPage";
        }
      }

      try {
        // 构建请求参数
        const params = {
          pageNum: this.pageNum,
          pageSize: this.pageSize,
          ...this.customParams, // 合并自定义参数
        };

        // 仅在没有自定义API时添加额外参数
        if (!this.customApi) {
          // 添加可选参数
          if (this.name) {
            params.name = this.name;
          }

          // 添加状态筛选参数
          if (this.status) {
            params.status = this.status;
          }
        }

        // 使用环境变量或配置的API基础URL，而不是硬编码localhost
        const apiBaseUrl = process.env.VUE_APP_BASE_API || "http://localhost:9090";
        
        // 使用axios直接发送请求
        const token = localStorage.getItem("xm-token");
        const directRes = await axios.get(`${apiBaseUrl}${url}`, {
          params,
          headers: token ? { token: token } : {},
          timeout: 30000,
        });

        if (directRes.data && directRes.data.code === "200") {
          this.tableData =
            directRes.data.data?.records || directRes.data.data?.list || [];
          this.total = directRes.data.data?.total || 0;

          // 触发数据加载完成事件
          this.$emit("data-loaded", {
            list: this.tableData,
            total: this.total,
          });

          return;
        }

        // 如果直接请求失败，尝试使用request
        const res = await request.get(url, { params });

        if (res.code === "200") {
          if (res.data && (res.data.records || res.data.list)) {
            this.tableData = res.data.records || res.data.list;
            this.total = res.data.total || 0;
          } else {
            console.warn("活动列表数据结构异常:", res.data);
            this.tableData = [];
            this.total = 0;
          }
        } else {
          console.warn("活动列表请求失败:", res);
          this.tableData = [];
          this.total = 0;
        }
      } catch (error) {
        console.error("加载活动列表失败:", error);
        this.tableData = [];
        this.total = 0;
      }
    },
    reset() {
      this.name = null;
      this.status = null; // 重置状态筛选
      this.load(1);
    },
    handleCurrentChange(pageNum) {
      this.load(pageNum);
    },
    handleSizeChange(pageSize) {
      this.pageSize = pageSize;
      this.pageNum = 1; // 切换每页显示条数时，重置为第一页
      this.load();
    },
    handleJumpPage() {
      if (!this.jumpPage) {
        this.jumpPage = 1;
        return;
      }

      // 计算最大页数
      const maxPage = Math.ceil(this.total / this.pageSize);

      // 确保页码在有效范围内
      if (this.jumpPage < 1) {
        this.jumpPage = 1;
      } else if (this.jumpPage > maxPage) {
        this.jumpPage = maxPage;
      }

      if (this.pageNum !== this.jumpPage) {
        this.pageNum = this.jumpPage;
        this.load();
      }
    },
  },
};
</script>

<style scoped>
.activity-card {
  background-color: var(--bg-color-secondary);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 15px var(--shadow-color);
  transition: all 0.3s;
  margin-bottom: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  max-width: 280px;
  margin-left: auto;
  margin-right: auto;
  border: 1px solid var(--border-color-light);
}

.activity-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px var(--shadow-color-hover);
  border-color: var(--primary-color);
}

.card-cover {
  position: relative;
  height: 180px;
  overflow: hidden;
  border-bottom: 1px solid var(--border-color);
}

.card-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.activity-card:hover .card-cover img {
  transform: scale(1.05);
}

.activity-status {
  position: absolute;
  top: 10px;
  right: 10px;
  background: var(--danger-color-alpha);
  color: var(--white);
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  border: 1px solid var(--border-color-light);
  box-shadow: 0 2px 8px var(--shadow-color);
}

.activity-status.signed {
  background: var(--success-color-alpha);
}

.card-content {
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.activity-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color-primary);
  margin: 0 0 10px 0;
  line-height: 1.4;
  height: 44px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.activity-time {
  color: var(--text-color-regular);
  font-size: 14px;
  margin-bottom: 15px;
}

.activity-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.activity-location {
  color: var(--text-color-secondary);
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 60%;
}

.activity-footer .el-button {
  border: 1px solid var(--primary-color-light);
  box-shadow: 0 2px 8px var(--primary-shadow);
}

.activity-footer .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px var(--primary-shadow-hover);
}

.empty-data {
  background-color: var(--bg-color-secondary);
  border-radius: 10px;
  padding: 40px;
  text-align: center;
  font-size: 16px;
  color: var(--text-color-secondary);
  box-shadow: 0 4px 15px var(--shadow-color);
}

.pagination-wrapper {
  background-color: var(--bg-color-secondary);
  border-radius: 10px;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  margin-top: 20px;
  box-shadow: 0 4px 15px var(--shadow-color);
  border: 1px solid var(--border-color-light);
}

.jump-page {
  display: inline-flex;
  align-items: center;
  color: var(--text-color-regular);
  font-size: 13px;
}

.jump-page .el-input /deep/ .el-input__inner {
  text-align: center;
  padding: 0 5px;
  border: 1px solid var(--border-color);
  background-color: var(--bg-color-secondary);
  color: var(--text-color-primary);
}

.jump-page .el-input /deep/ .el-input__inner:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px var(--primary-shadow);
}

@media (max-width: 768px) {
  .pagination-wrapper {
    flex-direction: column;
    gap: 15px;
  }

  .jump-page {
    width: 100%;
    justify-content: center;
  }
}

/* 确保每行的卡片高度一致 */
.el-row {
  display: flex;
  flex-wrap: wrap;
}

.el-col {
  display: flex;
  margin-bottom: 20px;
}
</style>
