import Vue from "vue";
import VueRouter from "vue-router";
import { MessageBox, ElMessage } from "element-ui";
import store from "../store";

Vue.use(VueRouter);

// 解决导航栏或者底部导航tabBar中的vue-router在3.0版本以上频繁点击菜单报错的问题。
const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch((err) => err);
};

// 主题处理函数
const handleTheme = (to) => {
  // 从 localStorage 获取当前主题
  const theme = localStorage.getItem("theme") || "light";
  const isProfessionPath =
    to.path.includes("/front/") &&
    (to.path.includes("/enhance") ||
      to.path.includes("/datasetPreprocessing") ||
      to.path.includes("/fishyolo") ||
      to.path.includes("/coralyolo"));

  // 如果不是专业功能页面，应用主题
  if (!isProfessionPath) {
    document.body.classList.toggle("dark", theme === "dark");
  } else {
    // 在专业功能页面移除主题类
    document.body.classList.remove("dark");
  }
};

const routes = [
  {
    path: "/",
    // 修改重定向路径到 IndexPage 对应的路由
    redirect: "/index",
  },
  {
    path: "/index",
    name: "IndexPage",
    meta: { name: "导引页" },
    component: () => import("../views/IndexPage.vue"),
    beforeEnter: (to, from, next) => {
      handleTheme(to);
      next();
    },
  },
  {
    path: "/front",
    name: "Front",
    component: () => import("../views/Front.vue"),
    beforeEnter: (to, from, next) => {
      handleTheme(to);
      next();
    },
    children: [
      {
        path: "home",
        name: "FHome",
        meta: { name: "交流中心" },
        component: () => import("../views/front/Home"),
        beforeEnter: (to, from, next) => {
          handleTheme(to);
          next();
        },
      },
      // {
      //   path: "person",
      //   name: "Person",
      //   meta: { name: "个人信息", requiresAuth: true },
      //   component: () => import("../views/front/Person"),
      //   beforeEnter: (to, from, next) => {
      //     handleTheme(to);
      //     next();
      //   },
      // },
      {
        path: "blogDetail",
        name: "BlogDetail",
        meta: { name: "博客详情" },
        component: () => import("../views/front/BlogDetail"),
        beforeEnter: (to, from, next) => {
          handleTheme(to);
          next();
        },
      },
      {
        path: "authorHome",
        name: "AuthorHome",
        meta: { name: "作者主页" },
        component: () => import("../views/front/AuthorHome"),
        beforeEnter: (to, from, next) => {
          handleTheme(to);
          next();
        },
      },
      {
        path: "search",
        name: "Search",
        meta: { name: "博客搜索" },
        component: () => import("../views/front/Search"),
        beforeEnter: (to, from, next) => {
          handleTheme(to);
          next();
        },
      },
      {
        path: "activity",
        name: "FrontActivity",
        meta: { name: "活动中心" },
        component: () => import("../views/front/Activity"),
        beforeEnter: (to, from, next) => {
          handleTheme(to);
          next();
        },
      },
      {
        path: "activityDetail",
        name: "ActivityDetail",
        meta: { name: "活动详情" },
        component: () => import("../views/front/ActivityDetail"),
        beforeEnter: (to, from, next) => {
          handleTheme(to);
          next();
        },
      },
      {
        path: "newBlog",
        name: "NewBlog",
        meta: { name: "发表博客", requiresAuth: true },
        component: () => import("../views/front/NewBlog"),
        beforeEnter: (to, from, next) => {
          handleTheme(to);
          next();
        },
      },
      {
        path: "resources",
        name: "Resources",
        meta: { name: "研究资源" },
        component: () => import("../views/front/Resources"),
        beforeEnter: (to, from, next) => {
          handleTheme(to);
          next();
        },
      },
      {
        path: "enhance",
        name: "Enhance",
        meta: { name: "图像增强", requiresAuth: true },
        component: () => import("../views/profession/Enhance.vue"),
      },
      {
        path: "datasetPreprocessing",
        name: "DatasetPreprocessing",
        meta: { name: "数据集生成", requiresAuth: true },
        component: () => import("../views/profession/DatasetPreprocessing.vue"),
      },
      {
        path: "fishyolo",
        name: "FishYolo",
        meta: { name: "鱼类目标识别", requiresAuth: true },
        component: () => import("../views/profession/FishYolo"),
      },
      {
        path: "coralyolo",
        name: "CoralYolo",
        meta: { name: "珊瑚健康监测", requiresAuth: true },
        component: () => import("../views/profession/CoralYolo"),
      },
      {
        path: "messageCenter",
        name: "MessageCenter",
        meta: { name: "消息中心", requiresAuth: true },
        component: () => import("../views/front/MessageCenter"),
        beforeEnter: (to, from, next) => {
          handleTheme(to);
          next();
        },
      },
      {
        path: "researcherHome",
        name: "ReSearcherHome",
        meta: { name: "科研工作者主页", requiresAuth: true },
        component: () => import("../views/front/ReSearcherHome"),
        beforeEnter: (to, from, next) => {
          handleTheme(to);
          next();
        },
      },
    ],
  },
  {
    path: "/login",
    name: "Login",
    meta: { name: "登录" },
    component: () => import("../views/Login.vue"),
    beforeEnter: (to, from, next) => {
      handleTheme(to);
      next();
    },
  },
  {
    path: "/register",
    name: "Register",
    meta: { name: "注册" },
    component: () => import("../views/Register.vue"),
    beforeEnter: (to, from, next) => {
      handleTheme(to);
      next();
    },
  },
  {
    path: "*",
    name: "NotFound",
    meta: { name: "无法访问" },
    component: () => import("../views/404.vue"),
    beforeEnter: (to, from, next) => {
      handleTheme(to);
      next();
    },
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { x: 0, y: 0 };
    }
  },
});

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置浏览器标签页标题
  if (to.meta && to.meta.name) {
    document.title = `${to.meta.name} - WaterSight`;
  } else {
    document.title = 'WaterSight 水下研究平台';
  }

  // 获取token，使用与request.js相同的逻辑
  const getToken = () => {
    const admin = localStorage.getItem("xm-admin");
    const user = localStorage.getItem("xm-user");

    if (admin) {
      try {
        return JSON.parse(admin).token;
      } catch (e) {}
    }

    if (user) {
      try {
        return JSON.parse(user).token;
      } catch (e) {}
    }

    return null;
  };

  const token = getToken();

  // 如果是登录页或注册页，直接通过
  if (to.path === "/login" || to.path === "/register" || to.path === "/index") {
    next();
    return;
  }

  // 如果没有token且不是登录页，重定向到登录页
  if (!token) {
    next("/login");
    return;
  }

  // 有token，检查是否是科研工作者角色且正在访问首页
  const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
  if (
    user.browseRole === "RESEARCHER" &&
    to.path === "/front/home" &&
    from.path === "/"
  ) {
    next("/front/researcherHome");
    return;
  }

  // 其他情况正常通行
  next();
});

export default router;
