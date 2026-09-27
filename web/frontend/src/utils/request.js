import axios from "axios";
import router from "@/router";
import { Message, MessageBox } from "element-ui";
import store from "@/store";

// 定义不需要token的公开接口
const publicPaths = [
  "/blog/selectPage",
  "/blog/selectTop",
  "/activity/selectPage",
  "/activity/selectTop",
  "/category/selectAll",
  "/notice/selectAll",
  "/admin/login",
  "/login",
  "/user/login",
  "/user/register",
  "/error",
];

// 判断是否是公开接口（精确匹配）
const isPublicPath = (url) => {
  // 移除查询参数和baseURL后再比较
  const path = url.replace(request.defaults.baseURL, "").split("?")[0];
  return publicPaths.includes(path);
};

// 获取token（简化token获取逻辑）
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

// 创建axios实例
const request = axios.create({
  baseURL: process.env.VUE_APP_BASE_API || "http://localhost:9090",
  timeout: 30000,
  paramsSerializer: {
    indexes: null,
  },
});

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    console.log("Request:", {
      url: config.url,
      method: config.method,
      data: config.data,
    });

    // 设置默认Content-Type
    if (!config.headers["Content-Type"]) {
      config.headers["Content-Type"] = "application/json;charset=utf-8";
    }

    // 处理请求数据
    if (config.data && typeof config.data === "object") {
      // 移除空字符串和undefined值
      Object.keys(config.data).forEach((key) => {
        if (config.data[key] === "" || config.data[key] === undefined) {
          delete config.data[key];
        }
      });

      // 确保数字类型字段为数字
      if (config.data.userId) {
        config.data.userId = parseInt(config.data.userId);
      }
      if (config.data.id) {
        config.data.id = parseInt(config.data.id);
      }
    }

    // 如果不是公开接口，添加token
    if (!isPublicPath(config.url)) {
      const token = getToken();
      if (token) {
        config.headers["token"] = token;
      }
    }

    return config;
  },
  (error) => {
    console.error("Request Error:", error);
    return Promise.reject(error);
  }
);

// token刷新相关变量
let isRefreshing = false;
let refreshSubscribers = [];

// 添加一个请求到队列
const subscribeTokenRefresh = (callback) => {
  refreshSubscribers.push(callback);
};

// 执行队列中的请求
const onRefreshed = (token) => {
  refreshSubscribers.forEach((callback) => callback(token));
  refreshSubscribers = [];
};

// 记录是否已经显示了登录对话框，避免重复显示
let loginDialogShown = false;

// 显示登录对话框
const showLoginDialog = (currentPath) => {
  if (loginDialogShown) return;

  loginDialogShown = true;

  MessageBox.confirm(
    "登录状态已过期，您可以继续留在该页面，或者重新登录",
    "系统提示",
    {
      confirmButtonText: "重新登录",
      cancelButtonText: "取消",
      type: "warning",
      callback: (action) => {
        loginDialogShown = false;
        if (action === "confirm") {
          router.push("/login?redirect=" + encodeURIComponent(currentPath));
        }
      },
    }
  );
};

// 清除用户信息
const clearUserInfo = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("xm-user");
  localStorage.removeItem("xm-admin");
  if (store.state.user) {
    store.commit("user/RESET_STATE");
  }
};

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    const res = response.data;

    // 处理文件流
    if (response.config.responseType === "blob") {
      return response;
    }

    // 处理业务状态码
    if (res.code === "401") {
      // 如果是公开接口，直接返回
      if (isPublicPath(response.config.url)) {
        return res;
      }

      // 清除用户信息
      clearUserInfo();

      // 返回401错误响应，让具体业务处理登录跳转
      return res;
    }

    if (res.code !== "200") {
      Message.error(res.msg || "操作失败");
      return Promise.reject(new Error(res.msg || "操作失败"));
    }

    return res;
  },
  (error) => {
    console.error("Response Error:", error);

    // 如果请求被取消，不显示错误
    if (axios.isCancel(error)) {
      return Promise.reject(error);
    }

    if (error.response) {
      const res = error.response.data;
      switch (error.response.status) {
        case 401:
          // 清除用户信息
          clearUserInfo();

          // 获取当前路由
          const currentPath = router.currentRoute.path;
          const restrictedPaths = [
            // "/front/person",
            "/front/newBlog",
            "/profession",
          ];

          // 只在受限页面显示提示和跳转
          if (restrictedPaths.some((path) => currentPath.startsWith(path))) {
            showLoginDialog(currentPath);
          }
          break;

        case 403:
          Message.error(res.msg || "没有权限进行此操作");
          break;

        case 404:
          Message.error(res.msg || "请求的资源不存在");
          break;

        case 500:
          Message.error(res.msg || "服务器内部错误");
          break;

        default:
          // 对于博客详情页的请求，使用更友好的错误提示
          if (
            error.config &&
            error.config.url &&
            error.config.url.includes("/blog/selectById")
          ) {
            Message.error("获取博客详情失败，该博客可能已被删除");
          } else if (
            error.config &&
            error.config.url &&
            error.config.url.includes("/blog/updateReadCount")
          ) {
            // 更新阅读量失败时不显示错误，静默处理
            console.warn("更新阅读量失败", error);
            return Promise.resolve({ code: "200", data: null });
          } else {
            // 其他错误使用通用提示
            Message.error(res?.msg || error.message || "请求失败");
          }
      }
    } else if (error.request) {
      Message.error("服务器无响应");
    } else {
      Message.error("请求配置错误");
    }

    return Promise.reject(error);
  }
);

// 修改：刷新token函数
async function refreshToken() {
  const userType = getCurrentUserType();
  const currentToken = getToken();
  if (!userType || !currentToken) return null;

  try {
    const response = await axios.post(
      "/auth/refresh",
      {
        userType,
        token: currentToken,
      },
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: currentToken,
        },
      }
    );

    if (
      response.data.code === "200" &&
      response.data.data &&
      response.data.data.token
    ) {
      return response.data.data.token;
    }
    return null;
  } catch (error) {
    console.error("Refresh token failed:", error);
    return null;
  }
}

// 获取当前用户类型
function getCurrentUserType() {
  if (localStorage.getItem("xm-admin")) return "admin";
  if (localStorage.getItem("xm-user")) return "user";
  return null;
}

// 定时刷新token
let refreshTokenInterval;

export function startTokenRefresh() {
  stopTokenRefresh();

  // 每15分钟刷新一次token
  refreshTokenInterval = setInterval(async () => {
    const token = getToken();
    if (token) {
      const newToken = await refreshToken();
      if (newToken) {
        const userType = getCurrentUserType();
        const storage = localStorage.getItem(`xm-${userType}`);
        if (storage) {
          const data = JSON.parse(storage);
          data.token = newToken;
          localStorage.setItem(`xm-${userType}`, JSON.stringify(data));
        }
      }
    } else {
      stopTokenRefresh();
    }
  }, 15 * 60 * 1000);
}

export function stopTokenRefresh() {
  if (refreshTokenInterval) {
    clearInterval(refreshTokenInterval);
    refreshTokenInterval = null;
  }
}

export default request;
