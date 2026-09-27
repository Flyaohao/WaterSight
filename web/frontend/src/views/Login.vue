<template>
  <div class="container">
    <button @click="goToHome" class="backToleader">返回导引页</button>
    <div class="login-box">
      <div class="login-title">WaterSight</div>
      <el-form
        :model="form"
        :rules="rules"
        ref="formRef"
        @keyup.enter.native="login"
      >
        <el-form-item prop="username">
          <el-input
            size="large"
            prefix-icon="el-icon-user"
            placeholder="请输入账号"
            v-model="form.username"
          ></el-input>
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            type="password"
            v-model="form.password"
            placeholder="请输入密码"
            prefix-icon="el-icon-lock"
            show-password
          ></el-input>
        </el-form-item>

        <el-form-item>
          <div class="login-btn">
            <el-button type="primary" @click="login" :loading="loading"
              >登录</el-button
            >
          </div>
        </el-form-item>

        <div class="register-link">
          还没有账号？请 <router-link to="/register">注册</router-link>
        </div>
      </el-form>
    </div>

    <login-dialog ref="loginDialog" />
  </div>
</template>

<script>
import request from "@/utils/request";
import LoginDialog from "@/components/LoginDialog.vue";

export default {
  name: "Login",
  components: {
    LoginDialog,
  },
  data() {
    return {
      form: {
        username: "",
        password: "",
        role: "USER", // 默认使用USER角色登录
      },
      loading: false,
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
      },
      userInfo: null,
    };
  },
  methods: {
    async login() {
      // 防止重复点击
      if (this.loading) return;

      // 表单验证
      this.$refs.formRef.validate(async (valid) => {
        if (!valid) {
          return;
        }

        this.loading = true;
        try {
          // 确保数据格式正确
          const loginData = {
            username: this.form.username.trim(),
            password: this.form.password,
            role: this.form.role,
          };

          console.log("登录请求数据:", loginData);

          const res = await request.post("/login", loginData);

          if (res.code === "200" && res.data) {
            // 确保返回的数据包含必要的字段
            if (!res.data.token) {
              throw new Error("登录返回数据缺少token");
            }

            // 保存用户信息
            this.userInfo = res.data;
            localStorage.setItem("xm-user", JSON.stringify(res.data));

            // 显示角色选择对话框
            this.$refs.loginDialog.show();
          } else {
            throw new Error(res.msg || "登录失败");
          }
        } catch (error) {
          console.error("登录失败：", error);
          // 根据错误类型显示不同的错误信息
          if (error.response) {
            const status = error.response.status;
            const data = error.response.data;

            switch (status) {
              case 400:
                this.$message.error(
                  "请求参数错误：" + (data.msg || "参数格式不正确")
                );
                break;
              case 401:
                this.$message.error("账号或密码错误");
                break;
              case 403:
                this.$message.error("账号已被禁用");
                break;
              case 500:
                this.$message.error("服务器错误，请稍后重试");
                break;
              default:
                this.$message.error(data.msg || error.message || "登录失败");
            }
          } else if (error.request) {
            this.$message.error("网络错误，请检查网络连接");
          } else {
            this.$message.error(error.message || "登录失败");
          }
        } finally {
          this.loading = false;
        }
      });
    },
    goToHome() {
      this.$router.push("/");
    },
  },
};
</script>

<style lang="less" scoped>
.container {
  height: 100vh;
  width: 100%;
  position: relative;
  overflow: hidden;
  background-image: url("@/assets/imgs/bgc4.png");
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
}

.login-box {
  width: 400px;
  padding: 40px;
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.login-title {
  text-align: center;
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 40px;
  color: #2a60c9;
  letter-spacing: 2px;
}

.login-btn {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: 10px;

  .el-button {
    width: 100%;
    height: 44px;
    background: linear-gradient(45deg, #2a60c9, #3b7ae4);
    border: none;
    font-size: 16px;
    transition: all 0.3s ease;

    &:hover {
      background: linear-gradient(45deg, #1e4aa0, #2a60c9);
      transform: translateY(-2px);
    }
  }
}

.backToleader {
  position: fixed;
  top: 20px;
  left: 20px;
  padding: 12px 24px;
  background-color: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #2a60c9;
  z-index: 1000;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.backToleader:hover {
  background-color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.register-link {
  text-align: right;
  margin-top: 15px;
  font-size: 14px;
}

.register-link a {
  color: #2a60c9;
  text-decoration: none;
  font-weight: 500;
}

.register-link a:hover {
  color: #1e4aa0;
  text-decoration: underline;
}

/deep/.el-input__inner {
  height: 44px;
  line-height: 44px;
}

/deep/.el-input__prefix {
  line-height: 44px;
}

/deep/.el-form-item {
  margin-bottom: 25px;
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
