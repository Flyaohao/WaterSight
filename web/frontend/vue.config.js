const { defineConfig } = require("@vue/cli-service");

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8080,
    client: {
      overlay: {
        warnings: false,
        errors: true,
      },
    },
    proxy: {
      "/api": {
        target: process.env.VUE_APP_BASE_API,
        changeOrigin: true,
        pathRewrite: {
          "^/api": "",
        },
      },
    },
  },
  chainWebpack: (config) => {
    config.plugin("html").tap((args) => {
      args[0].title = "管理系统";
      return args;
    });
  },
  css: {
    loaderOptions: {
      postcss: {
        postcssOptions: {
          plugins: [require("autoprefixer")],
        },
      },
      scss: {
        additionalData: `@import "@/styles/variables.scss";`,
      },
      sass: {
        additionalData: `@import "@/styles/variables.sass";`,
      },
    },
  },
  runtimeCompiler: true,
});
