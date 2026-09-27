<template>
  <div class="admin-container">
    <div class="admin-login-box">
      <div class="admin-login-title">
        <span class="system-name">WaterSight</span>
        <span class="admin-text">管理系统</span>
      </div>
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item prop="username">
          <el-input size="large" prefix-icon="el-icon-user" placeholder="请输入管理员账号" v-model="form.username"></el-input>
        </el-form-item>

        <el-form-item prop="password">
          <el-input size="large" prefix-icon="el-icon-lock" placeholder="请输入管理员密码" show-password v-model="form.password"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button size="large" type="primary" class="admin-login-btn" @click="login">登 录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import request from '@/utils/request'

export default {
  name: "AdminLogin",
  data() {
    return {
      form: {
        username: '',
        password: '',
        role: 'ADMIN'  // 固定为管理员角色
      },
      rules: {
        username: [
          { required: true, message: '请输入管理员账号', trigger: 'blur' },
        ],
        password: [
          { required: true, message: '请输入管理员密码', trigger: 'blur' },
        ]
      }
    }
  },
  methods: {
    login() {
      this.$refs.formRef.validate((valid) => {
        if (valid) {
          request.post('/admin', this.form).then(res => {
            if (res.code === '200' && res.data) {
              localStorage.setItem('xm-admin', JSON.stringify(res.data))
              this.$router.push('/manager/home')
              this.$message.success('管理员登录成功')
            } else {
              this.$message.error(res.msg || '登录失败')
            }
          }).catch(error => {
            console.error('登录错误：', error)
            this.$message.error('登录失败：' + error.message)
          })
        }
      })
    }
  }
}
</script>

<style lang="less" scoped>
.admin-container {
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

.admin-login-box {
  width: 420px;
  padding: 50px;
  background-color: rgba(255, 255, 255, 0.98);
  border-radius: 15px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(15px);
}

.admin-login-title {
  text-align: center;
  margin-bottom: 45px;
}

.system-name {
  font-size: 32px;
  font-weight: bold;
  color: #1a237e;
  display: block;
  margin-bottom: 8px;
}

.admin-text {
  font-size: 18px;
  color: #5c6bc0;
  letter-spacing: 3px;
}

.admin-login-btn {
  width: 100%;
  height: 46px;
  background: linear-gradient(45deg, #1a237e, #3949ab);
  border: none;
  font-size: 16px;
  margin-top: 15px;
  letter-spacing: 4px;
}

.admin-login-btn:hover {
  background: linear-gradient(45deg, #0d1642, #1a237e);
  transform: translateY(-1px);
}

/deep/.el-input__inner {
  height: 46px;
  line-height: 46px;
  background-color: #f5f7fa;
}

/deep/.el-input__prefix {
  line-height: 46px;
}

/deep/.el-form-item {
  margin-bottom: 25px;
}

/deep/.el-input__inner:focus {
  background-color: #fff;
}
</style> 