import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import adminRouter from "./router/admin";
import store from "./store";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import "@/assets/css/global.css";
import "@/assets/css/theme/index.css";
import "@/assets/styles/theme.less";
import "@/assets/styles/dark-theme.css";
import request from "@/utils/request";
import storage from "@/utils/storage";
import config from "@/config";
import ripple from "./mouse/ripple";
import "@/assets/css/ripple.css";
import "@/assets/css/confirm.css";
import moment from "moment";
import "moment/locale/zh-cn";

Vue.config.productionTip = false;
Vue.use(ElementUI, { size: "small" });
Vue.directive("ripple", ripple);

// 配置 moment.js
moment.locale("zh-cn");
Vue.prototype.$moment = moment;

// 全局注册 request
Vue.prototype.$request = request;
Vue.prototype.$storage = storage;
Vue.prototype.$baseUrl = config.baseUrl;

// 初始化主题
store.dispatch("initTheme");

// 根据路径选择路由配置
const currentPath = window.location.pathname;
const useAdminRouter =
  currentPath.startsWith("/admin") || currentPath.startsWith("/manager");
const selectedRouter = useAdminRouter ? adminRouter : router;

// 创建路由实例
const vueInstance = new Vue({
  router: selectedRouter,
  store,
  render: (h) => h(App),
});

// 全局路由守卫，处理特殊路径
selectedRouter.beforeEach((to, from, next) => {
  // 如果是访问 /login，确保使用社区版路由
  if (to.path === "/login" && useAdminRouter) {
    window.location.href = "/login";
    return;
  }
  next();
});

vueInstance.$mount("#app");
