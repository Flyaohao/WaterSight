import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

// 解决导航栏或者底部导航tabBar中的vue-router在3.0版本以上频繁点击菜单报错的问题。
const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err);
};

const routes = [
  {
    path: '/admin',
    name: 'AdminLogin',
    meta: { name: '管理员登录' },
    component: () => import('../views/AdminLogin.vue')
  },
  {
    path: '/manager',
    name: 'Manager',
    component: () => import('../views/Manager.vue'),
    redirect: '/manager/home',
    children: [
      { path: '403', name: 'NoAuth', meta: { name: '无权限' }, component: () => import('../views/manager/403') },
      { path: 'home', name: 'Home', meta: { name: '系统首页' }, component: () => import('../views/manager/Home') },
      { path: 'admin', name: 'Admin', meta: { name: '管理员信息' }, component: () => import('../views/manager/Admin') },
      { path: 'adminPerson', name: 'AdminPerson', meta: { name: '个人信息' }, component: () => import('../views/manager/AdminPerson') },
      { path: 'password', name: 'Password', meta: { name: '修改密码' }, component: () => import('../views/manager/Password') },
      { path: 'notice', name: 'Notice', meta: { name: '公告信息' }, component: () => import('../views/manager/Notice') },
      { path: 'user', name: 'User', meta: { name: '用户信息' }, component: () => import('../views/manager/User') },
      { path: 'category', name: 'Category', meta: { name: '博客分类' }, component: () => import('../views/manager/Category') },
      { path: 'blog', name: 'Blog', meta: { name: '博客信息' }, component: () => import('../views/manager/Blog') },
      { path: 'activity', name: 'Activity', meta: { name: '活动信息' }, component: () => import('../views/manager/Activity') },
      { path: 'comment', name: 'Comment', meta: { name: '评论信息' }, component: () => import('../views/manager/Comment') },
      { path: 'activitySign', name: 'ActivitySign', meta: { name: '活动报名' }, component: () => import('../views/manager/ActivitySign') },
    ]
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置浏览器标签页标题
  if (to.meta && to.meta.name) {
    document.title = `${to.meta.name} - WaterSight管理系统`;
  } else {
    document.title = 'WaterSight管理系统';
  }
  
  let admin = JSON.parse(localStorage.getItem("xm-admin") || '{}');
  
  // 管理员系统路由守卫
  if (to.path.startsWith('/manager')) {
    if (!admin.token) {
      next('/admin');
      return;
    }
    next();
    return;
  }

  // 管理员登录页面
  if (to.path === '/admin') {
    if (admin.token) {
      next('/manager/home');
      return;
    }
    next();
    return;
  }

  // 对于其他路径，重定向到管理员登录页
  if (!to.matched.length) {
    next('/admin');
    return;
  }

  next();
});

export default router; 