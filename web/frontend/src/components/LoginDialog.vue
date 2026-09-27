<template>
  <el-dialog
    title="选择您的角色"
    :visible.sync="dialogVisible"
    width="500px"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :show-close="true"
    @close="handleDialogClose"
  >
    <div class="role-selection">
      <div class="role-options">
        <div
          class="role-option"
          :class="{ active: selectedRole === 'RESEARCHER' }"
          @click="selectRole('RESEARCHER')"
        >
          <i class="el-icon-s-custom"></i>
          <h3>科研工作者</h3>
          <p>访问科研相关词条</p>
        </div>
        <div
          class="role-option"
          :class="{ active: selectedRole === 'ALL' }"
          @click="selectRole('ALL')"
        >
          <i class="el-icon-camera"></i>
          <h3>业余爱好者</h3>
          <p>访问摄影、潜水等词条</p>
        </div>
      </div>
      <div class="dialog-footer">
        <el-button type="primary" @click="confirmRole" :disabled="!selectedRole"
          >确认选择</el-button
        >
      </div>
    </div>
  </el-dialog>
</template>

<script>
import request from "@/utils/request";

export default {
  name: "LoginDialog",
  data() {
    return {
      dialogVisible: false,
      selectedRole: "",
      userInfo: null,
    };
  },
  methods: {
    show() {
      this.dialogVisible = true;
      // 获取当前用户信息
      const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
      this.userInfo = user;
      // 设置当前选中的角色
      this.selectedRole = user.browseRole || "ALL";
    },
    selectRole(role) {
      this.selectedRole = role;
    },
    async confirmRole() {
      if (!this.selectedRole) return;

      try {
        // 验证用户ID
        if (!this.userInfo || !this.userInfo.id) {
          this.$message.error("请先登录后再切换角色");
          return;
        }

        // 验证角色参数
        if (
          !this.selectedRole ||
          !["RESEARCHER", "HOBBYIST", "ALL"].includes(this.selectedRole)
        ) {
          this.$message.error("无效的角色参数");
          return;
        }

        const res = await request.put("/user/updateBrowseRole", {
          userId: this.userInfo.id,
          browseRole: this.selectedRole,
        });

        if (res.code === "200") {
          // 清除博客列表状态以确保角色切换后正确加载
          sessionStorage.removeItem("blog-list-state");

          // 更新本地存储的用户信息
          this.userInfo.browseRole = this.selectedRole;
          localStorage.setItem("xm-user", JSON.stringify(this.userInfo));

          this.dialogVisible = false;

          // 根据角色切换路由，并使用Promise确保路由跳转完成后再刷新
          try {
            const targetRoute = this.selectedRole === "RESEARCHER" 
              ? "/front/researcherHome" 
              : "/front/home";
            
            // 等待路由跳转完成
            await this.$router.push(targetRoute);
            
            // 路由跳转成功后再刷新页面
            window.location.reload();
          } catch (navError) {
            // 处理路由重复导航的错误（可以忽略）
            if (navError.name !== 'NavigationDuplicated') {
              console.error("导航错误:", navError);
              throw navError;
            } else {
              // 即使是重复导航，也刷新页面
              window.location.reload();
            }
          }
        } else {
          throw new Error(res.msg || "切换角色失败");
        }
      } catch (error) {
        console.error("切换角色失败:", error);
        this.$message.error(error.message || "切换角色失败，请稍后重试");
      }
    },
    handleDialogClose() {
      this.dialogVisible = false;
      // 恢复到之前选择的角色
      const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
      this.selectedRole = user.browseRole || "ALL";
    },
  },
};
</script>

<style lang="less" scoped>
/* 角色选择对话框样式 */
.role-selection {
  .role-options {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 30px;
    padding: 0 20px;
  }

  .role-option {
    flex: 1;
    text-align: center;
    padding: 30px 20px;
    border-radius: 12px;
    border: 2px solid #e4e7ed;
    cursor: pointer;
    transition: all 0.3s ease;
    background: rgba(255, 255, 255, 0.9);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);

    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }

    &.active {
      border-color: #2a60c9;
      background: rgba(42, 96, 201, 0.05);
    }

    i {
      font-size: 36px;
      color: #2a60c9;
      margin-bottom: 15px;
    }

    h3 {
      margin: 15px 0;
      font-size: 18px;
      font-weight: 600;
    }

    p {
      margin: 0;
      font-size: 14px;
      color: #909399;
      line-height: 1.5;
    }
  }

  .dialog-footer {
    text-align: center;
    padding: 0 20px;

    .el-button {
      width: 120px;
      height: 40px;
      font-size: 16px;
    }
  }
}

/deep/ .el-dialog {
  border-radius: 16px;
  overflow: hidden;

  .el-dialog__header {
    background: #2a60c9;
    padding: 20px;
    margin: 0;

    .el-dialog__title {
      color: white;
      font-size: 20px;
      font-weight: 600;
    }
  }

  .el-dialog__body {
    padding: 30px 20px;
  }
}
</style>
