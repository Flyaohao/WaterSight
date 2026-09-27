<template>
  <div class="manager-container">
    <!--  头部  -->
    <div class="manager-header">
      <div class="manager-header-left">
        <img src="@/assets/imgs/logo1.png" />
        <div class="title">后台管理系统</div>
      </div>

      <div class="manager-header-center">
        <el-breadcrumb separator-class="el-icon-arrow-right">
          <el-breadcrumb-item :to="{ path: '/manager' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item :to="{ path: $route.path }">{{ $route.meta.name }}</el-breadcrumb-item>
        </el-breadcrumb>
      </div>

      <div class="manager-header-right">
        <el-dropdown placement="bottom">
          <div class="avatar">
            <img :src="user.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'" />
            <div>{{ user.name ||  '管理员' }}</div>
          </div>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item @click.native="goToPerson">个人信息</el-dropdown-item>
            <el-dropdown-item @click.native="$router.push('/password')">修改密码</el-dropdown-item>
            <el-dropdown-item @click.native="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>

    <!--  主体  -->
    <div class="manager-main">
      <!--  侧边栏  -->
      <div class="manager-main-left">
        <el-menu :default-openeds="['info', 'user']" router style="border: none" :default-active="$route.path">
          <el-menu-item index="/manager/home">
            <i class="el-icon-s-home"></i>
            <span slot="title">系统首页</span>
          </el-menu-item>
          <el-submenu index="info">
            <template slot="title">
              <i class="el-icon-menu"></i><span>信息管理</span>
            </template>
            <el-menu-item index="/manager/category">博客分类</el-menu-item>
            <el-menu-item index="/manager/blog">博客信息</el-menu-item>
            <el-menu-item index="/manager/activity">活动信息</el-menu-item>
            <el-menu-item index="/manager/comment">评论信息</el-menu-item>
            <el-menu-item index="/manager/activitySign">活动报名</el-menu-item>
            <el-menu-item index="/manager/notice">公告信息</el-menu-item>
          </el-submenu>

          <el-submenu index="user">
            <template slot="title">
              <i class="el-icon-menu"></i><span>用户管理</span>
            </template>
            <el-menu-item index="/manager/admin">管理员信息</el-menu-item>
            <el-menu-item index="/manager/user">用户信息</el-menu-item>
          </el-submenu>
        </el-menu>
      </div>

      <!--  数据表格  -->
      <div class="manager-main-right">
        <router-view @update:user="updateUser" />
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: "Manager",
  data() {
    return {
      user: JSON.parse(localStorage.getItem('xm-admin') || '{}'),
    }
  },
  created() {
    if (!this.user.token) {
      this.$router.push('/admin')
    }
  },
  methods: {
    updateUser() {
      this.user = JSON.parse(localStorage.getItem('xm-admin') || '{}')
    },
    goToPerson() {
      // 获取当前登录的管理员信息
      const adminUser = JSON.parse(localStorage.getItem('xm-admin') || '{}');
      
      // 检查是否有用户ID
      if (adminUser && adminUser.id) {
        this.$router.push({
          path: '/manager/adminPerson',
          query: { adminId: adminUser.id }
        });
      } else {
        this.$message.warning("请先登录");
        this.$router.push('/admin');
      }
    },
    logout() {
      localStorage.removeItem('xm-admin')
      this.$router.push('/admin')
    }
  }
}
</script>

<style scoped>
@import "@/assets/css/manager.css";

</style>