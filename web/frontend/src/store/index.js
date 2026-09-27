import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isLoggedIn: false,
    userInfo: null,
    user: JSON.parse(localStorage.getItem("xm-user") || "{}"),
    admin: JSON.parse(localStorage.getItem("xm-admin") || "{}"),
    theme: localStorage.getItem("theme") || "light",
  },
  getters: {
    getUser: (state) => state.user,
    getAdmin: (state) => state.admin,
    isUserLoggedIn: (state) => !!state.user.token,
    isAdminLoggedIn: (state) => !!state.admin.token,
    isDarkTheme: (state) => state.theme === "dark",
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user;
      localStorage.setItem("xm-user", JSON.stringify(user));
    },
    SET_ADMIN(state, admin) {
      state.admin = admin;
      localStorage.setItem("xm-admin", JSON.stringify(admin));
    },
    CLEAR_USER(state) {
      state.user = {};
      localStorage.removeItem("xm-user");
    },
    CLEAR_ADMIN(state) {
      state.admin = {};
      localStorage.removeItem("xm-admin");
    },
    SET_LOGIN_STATE(state, status) {
      state.isLoggedIn = status;
    },
    CLEAR_USER_STATE(state) {
      state.isLoggedIn = false;
      state.userInfo = null;
    },
    setUnreadMessageCount(state, count) {
      if (state.user && typeof state.user === "object") {
        state.user.unreadMessageCount = count;
      }
    },
    SET_THEME(state, theme) {
      state.theme = theme;
      localStorage.setItem("theme", theme);
      // 添加或移除 dark 类到 body 元素
      if (theme === "dark") {
        document.body.classList.add("dark");
      } else {
        document.body.classList.remove("dark");
      }
    },
  },
  actions: {
    setUser({ commit }, user) {
      commit("SET_USER", user);
    },
    setAdmin({ commit }, admin) {
      commit("SET_ADMIN", admin);
    },
    logout({ commit }) {
      commit("CLEAR_USER");
    },
    adminLogout({ commit }) {
      commit("CLEAR_ADMIN");
    },
    checkLoginStatus({ commit }) {
      const token = localStorage.getItem("token");
      if (!token) {
        commit("CLEAR_USER_STATE");
        return false;
      }
      return true;
    },
    toggleTheme({ commit, state }) {
      const newTheme = state.theme === "light" ? "dark" : "light";
      commit("SET_THEME", newTheme);
    },
    initTheme({ commit }) {
      const savedTheme = localStorage.getItem("theme") || "light";
      commit("SET_THEME", savedTheme);
    },
  },
  modules: {},
});
