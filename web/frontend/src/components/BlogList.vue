<template>
  <div class="blog-list-container" :class="themeClass">
    <!-- 博客列表 -->
    <div v-if="initialLoading" class="loading-container">
      <el-skeleton :rows="5" animated />
    </div>
    <div v-else-if="blogs.length === 0" class="empty-container">
      <i class="el-icon-document"></i>
      <p>暂无博客</p>
    </div>
    <div v-else>
      <transition-group name="blog-list" tag="div" class="blog-list">
        <div v-for="blog in blogs" :key="blog.id" class="blog-card">
          <!-- 博客封面 - 在研究模式下隐藏 -->
          <div
            class="blog-cover"
            @click="viewBlog(blog.id)"
            v-if="!isResearchMode"
          >
            <img
              :src="blog.cover"
              @error="handleImageError($event)"
              alt="博客封面"
              class="cover-image"
            />
          </div>

          <!-- 博客内容 -->
          <div class="blog-content">
            <h3 class="blog-title" @click="viewBlog(blog.id)">
              {{ blog.title }}
            </h3>

            <p class="blog-description" v-if="!isResearchMode">
              {{ blog.descr }}
            </p>

            <div class="blog-meta">
              <div class="meta-left">
                <span
                  class="blog-author"
                  @click.stop="goToAuthorHome(blog.userId)"
                >
                  <i class="el-icon-user"></i> {{ blog.userName }}
                </span>
                <span class="blog-date">
                  <i class="el-icon-date"></i> {{ formatDate(blog.date) }}
                </span>
                <span class="blog-category" v-if="blog.categoryName">
                  <i class="el-icon-collection-tag"></i> {{ blog.categoryName }}
                </span>
                <span class="blog-tags" v-if="blog.tags">
                  <i class="el-icon-price-tag"></i>
                  {{ formatTags(blog.tags) }}
                </span>
              </div>

              <div class="meta-right">
                <span class="blog-views">
                  <i class="el-icon-view"></i> {{ blog.readCount || 0 }}
                </span>
                <span class="blog-likes">
                  <i class="el-icon-star-off"></i> {{ blog.likesCount || 0 }}
                </span>
              </div>
            </div>

            <!-- 操作按钮 (仅在需要时显示) -->
            <div
              v-if="showOpt && currentUser.id === blog.userId"
              class="blog-actions"
            >
              <el-button type="primary" size="mini" @click="handleEdit(blog)"
                >编辑</el-button
              >
              <el-button type="danger" size="mini" @click="handleDelete(blog)"
                >删除</el-button
              >
            </div>
          </div>
        </div>
      </transition-group>

      <!-- 加载更多按钮 -->
      <div class="load-more-container" v-if="hasMore">
        <el-button
          type="primary"
          :loading="loading"
          @click="loadMore"
          class="load-more-btn"
        >
          <i class="el-icon-loading" v-if="loading"></i>
          <span>{{ loading ? "加载中..." : "加载更多" }}</span>
        </el-button>
      </div>

      <!-- 全部加载完成提示 -->
      <div class="load-more-container" v-if="blogs.length > 0 && !hasMore">
        <div class="all-loaded-message">
          <i class="el-icon-check"></i> 暂无更多内容
        </div>
      </div>

      <!-- 加载中的骨架屏 -->
      <div v-if="loading && !initialLoading" class="loading-more-skeleton">
        <el-skeleton :rows="3" animated />
      </div>
    </div>

    <!-- 编辑对话框 -->
    <el-dialog
      title="编辑博客"
      :visible.sync="editDialogVisible"
      width="50%"
      @close="handleDialogClose"
    >
      <el-form
        :model="editForm"
        :rules="rules"
        ref="editFormRef"
        label-width="80px"
      >
        <el-form-item label="标题" prop="title">
          <el-input
            v-model="editForm.title"
            placeholder="请输入标题"
          ></el-input>
        </el-form-item>
        <el-form-item label="简介" prop="descr">
          <el-input
            type="textarea"
            v-model="editForm.descr"
            :rows="3"
            placeholder="请输入简介"
          ></el-input>
        </el-form-item>
        <el-form-item label="封面" prop="cover">
          <el-upload
            class="cover-uploader"
            :action="$baseUrl + '/files/upload'"
            :headers="{ token: currentUser.token }"
            :show-file-list="false"
            :on-success="handleCoverSuccess"
            :before-upload="beforeCoverUpload"
          >
            <img
              v-if="editForm.cover"
              :src="editForm.cover"
              class="cover-image"
            />
            <i v-else class="el-icon-plus cover-uploader-icon"></i>
          </el-upload>
        </el-form-item>
        <el-form-item label="分类" prop="categoryId">
          <el-select v-model="editForm.categoryId" placeholder="请选择分类">
            <el-option
              v-for="item in categoryList"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="标签" prop="tags">
          <el-select
            v-model="editForm.tagsArr"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="请选择标签"
          >
            <el-option
              v-for="item in defaultTags"
              :key="item"
              :label="item"
              :value="item"
            >
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="handleDialogClose">取 消</el-button>
        <el-button type="primary" @click="submitEdit">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import request from "@/utils/request";
import { formatDate } from "@/utils/date";

export default {
  name: "BlogList",
  props: {
    categoryName: {
      type: String,
      default: "",
    },
    showOpt: {
      type: Boolean,
      default: false,
    },
    searchTitle: {
      type: String,
      default: "",
    },
    type: {
      type: String,
      default: "",
    },
    userName: {
      type: String,
      default: "",
    },
    customApi: {
      type: String,
      default: "",
    },
    customParams: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    const savedState = JSON.parse(
      sessionStorage.getItem("blog-list-state") || "{}"
    );
    return {
      blogs: savedState.blogs || [],
      pageNum: savedState.pageNum || 1,
      pageSize: 15,
      total: savedState.total || 0,
      loading: false,
      initialLoading: !savedState.blogs,
      scrollPosition: savedState.scrollPosition || 0,
      currentUser: JSON.parse(localStorage.getItem("xm-user") || "{}"),
      editDialogVisible: false,
      editForm: {
        id: "",
        title: "",
        descr: "",
        cover: "",
        categoryId: "",
        tagsArr: [],
      },
      categoryList: [],
      defaultTags: [
        "水下摄影",
        "水产养殖",
        "水下图像",
        "目标识别",
        "科学研究",
        "教育资源",
        "法规政策",
      ],
      rules: {
        title: [
          { required: true, message: "请输入标题", trigger: "blur" },
          {
            min: 2,
            max: 50,
            message: "长度在 2 到 50 个字符",
            trigger: "blur",
          },
        ],
        descr: [
          { required: true, message: "请输入简介", trigger: "blur" },
          {
            min: 10,
            max: 500,
            message: "长度在 10 到 500 个字符",
            trigger: "blur",
          },
        ],
        categoryId: [
          { required: true, message: "请选择分类", trigger: "change" },
        ],
      },
    };
  },
  computed: {
    isResearchMode() {
      return this.currentUser.browseRole === "RESEARCHER";
    },
    isHobbyistMode() {
      return this.currentUser.browseRole === "HOBBYIST";
    },
    themeClass() {
      return {
        "research-theme": this.isResearchMode,
        "hobbyist-theme": this.isHobbyistMode,
      };
    },
    hasMore() {
      // 有总数且已加载的博客数量小于总数时返回true
      return this.total > 0 && this.blogs.length < this.total;
    },
  },
  watch: {
    $route(to, from) {
      if (
        to.path !== from.path &&
        !to.path.includes("blogDetail") &&
        !from.path.includes("blogDetail")
      ) {
        this.reset();
        this.load();
      }
    },
    // 监听用户角色变化
    "currentUser.browseRole": {
      handler(newRole, oldRole) {
        if (newRole !== oldRole && oldRole) {
          console.log("用户角色已变更，重新加载博客列表");
          this.reset();
          this.load();

          // 角色切换后刷新页面以确保所有组件正确加载
          setTimeout(() => {
            console.log("角色切换刷新页面");
            window.location.reload();
          }, 300);
        }
      },
    },
  },
  updated() {
    // 在组件更新后发送高度变化事件
    this.$nextTick(() => {
      const height = this.$el.offsetHeight;
      this.$emit("height-change", height);
    });
  },
  created() {
    this.debouncedLoad = this.debounce(this.load, 200);
    this.load();

    // 添加事件监听
    this.$root.$on("blog-search", this.handleSearchUpdate);
    this.$root.$on("blog-refresh", () => {
      console.log("刷新博客列表");
      this.reset();
      this.load();
    });

    this.loadCategories();

    // 监听存储变化，检测用户角色变化
    window.addEventListener("storage", this.handleStorageChange);

    if (!this.blogs.length) {
      this.load();
    } else {
      this.$nextTick(() => {
        window.scrollTo({
          top: this.scrollPosition,
          behavior: "instant",
        });
      });
    }
  },
  mounted() {
    // 添加滚动位置监听
    window.addEventListener("scroll", this.debounce(this.handleScroll, 100));

    // 检查当前状态是否需要重新加载
    this.checkUserAndReload();
  },
  beforeDestroy() {
    // 移除滚动监听
    window.removeEventListener("scroll", this.handleScroll);
    // 移除存储监听
    window.removeEventListener("storage", this.handleStorageChange);
    // 移除事件监听
    this.$root.$off("blog-search", this.handleSearchUpdate);
    this.$root.$off("blog-refresh");
  },
  beforeRouteLeave(to, from, next) {
    if (!to.path.includes("blogDetail")) {
      this.reset();
    }
    next();
  },
  methods: {
    debounce(fn, delay) {
      let timer = null;
      return function () {
        const context = this;
        const args = arguments;
        clearTimeout(timer);
        timer = setTimeout(() => {
          fn.apply(context, args);
        }, delay);
      };
    },
    handleScroll() {
      if (!this.$route.path.includes("blogDetail")) {
        this.saveState();
      }
    },
    saveState() {
      const state = {
        blogs: this.blogs,
        pageNum: this.pageNum,
        total: this.total,
        scrollPosition: window.pageYOffset,
      };
      sessionStorage.setItem("blog-list-state", JSON.stringify(state));
    },
    reset() {
      this.blogs = [];
      this.pageNum = 1;
      this.total = 0;
      sessionStorage.removeItem("blog-list-state");

      // 更新当前用户信息
      this.currentUser = JSON.parse(localStorage.getItem("xm-user") || "{}");
    },
    handleCurrentChange(pageNum) {
      this.pageNum = pageNum;
      this.load();
    },
    handleSizeChange(pageSize) {
      this.pageSize = pageSize;
      this.pageNum = 1;
      this.load();
    },
    async loadMore() {
      if (this.loading) return;

      if (!this.hasMore) {
        // 已经显示在UI上了，不需要额外提示
        return;
      }

      this.pageNum += 1;
      const result = await this.load(true);

      // 如果没有加载到新的博客，更新total使hasMore计算正确
      if (result && result.newBlogsCount === 0) {
        // 更新total确保hasMore计算为false
        this.total = this.blogs.length;
      }

      this.saveState();
    },
    async loadCategories() {
      try {
        // 获取当前用户角色
        const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
        const role = user.browseRole;

        // 如果用户未登录，使用不需要role参数的API
        if (!role) {
          const res = await request.get("/category/selectAll");
          if (res.code === "200") {
            this.categoryList = Array.isArray(res.data) ? res.data : [];
          }
          return;
        }

        // 根据角色获取分类
        let url = "/category/selectByRole";
        let params = {};

        // 设置对应的角色参数
        if (role === "RESEARCHER") {
          params.role = "RESEARCHER";
          console.log("加载科研人员分类");
        } else if (role === "ALL" || role === "HOBBYIST") {
          params.role = "HOBBYIST";
          console.log("加载业余爱好者分类");
        }

        console.log("请求分类API参数:", params);
        const res = await request.get(url, { params });

        if (res.code === "200") {
          this.categoryList = Array.isArray(res.data) ? res.data : [];
          console.log(
            `加载分类成功: ${this.categoryList.length}个类别, 角色: ${
              params.role || "全部"
            }`
          );

          // 输出分类详情以便调试
          if (this.categoryList.length > 0) {
            console.log("分类示例:", this.categoryList[0]);
          }
        }
      } catch (error) {
        console.error("加载分类失败:", error);
        this.categoryList = [];
      }
    },
    async load(append = false) {
      if (this.loading) return;

      this.loading = true;
      try {
        let url = this.customApi || "/blog/selectPage";
        let params = {
          pageNum: this.pageNum,
          pageSize: this.pageSize,
          ...this.customParams,
        };

        // 获取当前用户角色
        const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
        const role = user.browseRole;

        // 更新当前用户信息以确保计算属性正确
        if (JSON.stringify(this.currentUser) !== JSON.stringify(user)) {
          this.currentUser = user;
        }

        // 设置角色参数
        if (role === "RESEARCHER") {
          params.role = "RESEARCHER";
          console.log("正在加载科研人员相关博客");
        } else if (role === "ALL" || role === "HOBBYIST") {
          params.role = "HOBBYIST";
          console.log("正在加载业余爱好者相关博客");
        }

        // 设置搜索参数 - 确保搜索参数正确传递
        if (this.searchTitle && this.searchTitle.trim()) {
          params.title = this.searchTitle.trim(); // 使用title作为参数名
          console.log("设置搜索关键词:", params.title);
        }

        if (this.type) {
          if (!user.id) {
            this.$message.warning("请先登录");
            return;
          }
          params.userId = user.id;
        }

        // 处理分类名称，确保全部博客标签页也能正确加载
        if (this.categoryName && this.categoryName !== "全部博客") {
          params.categoryName = this.categoryName;
        }

        if (this.userName) {
          params.userName = this.userName;
        }

        console.log("加载博客，参数:", params);

        const res = await request.get(url, { params });

        if (res.code === "200") {
          let newBlogs = res.data?.list || [];
          const originalTotal = res.data?.total || 0;

          console.log(`从后端接收到${newBlogs.length}篇博客，准备筛选`);

          // 使用原始的分类筛选逻辑
          if (role) {
            newBlogs = newBlogs.filter((blog) => {
              // 找到博客对应的分类
              const blogCategory = this.categoryList.find(
                (c) => c.id === blog.categoryId
              );
              // 只保留当前角色对应的分类博客
              const match = blogCategory && blogCategory.role === params.role;
              if (match) {
                console.log(
                  `保留博客: ID=${blog.id}, 标题=${blog.title}, 分类=${blog.categoryName}, 角色=${blogCategory?.role}`
                );
              }
              return match;
            });
            console.log(`筛选后剩余${newBlogs.length}篇博客`);
          }

          // 检查是否有重复的博客
          let uniqueNewBlogs = newBlogs;
          if (append) {
            const existingIds = new Set(this.blogs.map((blog) => blog.id));
            uniqueNewBlogs = newBlogs.filter(
              (blog) => !existingIds.has(blog.id)
            );
            this.blogs = [...this.blogs, ...uniqueNewBlogs];
          } else {
            this.blogs = newBlogs;
          }

          // 更新总数，确保加载更多按钮的显示逻辑正确
          this.total = originalTotal; // 使用后端返回的总数

          // 保存状态
          if (!append) {
            this.saveState();
          }

          // 如果是追加模式且没有新的博客，调整total使hasMore计算为false
          if (append && uniqueNewBlogs.length === 0) {
            this.total = this.blogs.length;
          }

          // 输出加载完成后的状态
          console.log(
            `加载完成: 显示${this.blogs.length}/${
              this.total
            }条博客，原始总数${originalTotal}，当前页码: ${
              this.pageNum
            }, 角色: ${params.role || "全部"}`
          );

          // 返回加载结果信息
          return {
            newBlogsCount: append ? uniqueNewBlogs.length : newBlogs.length,
            totalCount: this.total,
          };
        } else {
          throw new Error(res.msg || "加载失败");
        }
      } catch (error) {
        console.error("加载博客列表失败:", error);
        this.$message.error(error.message || "加载失败");
        return { newBlogsCount: 0, totalCount: 0 };
      } finally {
        this.loading = false;
        this.initialLoading = false;
      }
    },
    handleImageError(e) {
      e.target.src = require("@/assets/imgs/bgc2.jpg");
    },
    handleEdit(blog) {
      // 跳转到博客编辑页面，并传递博客ID
      this.$router.push({
        path: '/front/newBlog',
        query: { blogId: blog.id }
      });
    },
    handleDelete(blog) {
      if (blog.userId !== this.currentUser.id) {
        this.$message.warning("您没有权限删除此博客");
        return;
      }

      this.$confirm("确认删除该博客吗？此操作不可恢复", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          request.delete("/blog/delete/" + blog.id).then((res) => {
            if (res.code === "200") {
              this.$message.success("删除成功");
              this.load();
            } else {
              this.$message.error(res.msg || "删除失败");
            }
          });
        })
        .catch(() => {});
    },
    handleBlogClick(blog) {
      this.$router.push(`/front/blogDetail?blogId=${blog.id}`);
    },
    handleDialogClose() {
      this.$refs.editFormRef?.resetFields();
      this.editDialogVisible = false;
      this.editForm = {
        id: "",
        title: "",
        descr: "",
        cover: "",
        categoryId: "",
        tagsArr: [],
      };
    },
    handleCoverSuccess(res) {
      if (res.code === "200") {
        this.editForm.cover = res.data;
      } else {
        this.$message.error("封面上传失败");
      }
    },
    beforeCoverUpload(file) {
      const isImage = file.type.startsWith("image/");
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isImage) {
        this.$message.error("上传封面图片只能是图片格式!");
      }
      if (!isLt2M) {
        this.$message.error("上传封面图片大小不能超过 2MB!");
      }

      return isImage && isLt2M;
    },
    submitEdit() {
      this.$refs.editFormRef.validate(async (valid) => {
        if (valid) {
          const submitData = {
            ...this.editForm,
            tags: JSON.stringify(this.editForm.tagsArr),
          };

          try {
            const res = await request.put("/blog/update", submitData);
            if (res.code === "200") {
              this.$message.success("更新成功");
              this.editDialogVisible = false;
              this.load();
            } else {
              this.$message.error(res.msg || "更新失败");
            }
          } catch (error) {
            console.error("更新博客失败:", error);
            this.$message.error("更新失败");
          }
        }
      });
    },
    formatDate,
    viewBlog(blogId) {
      // 保存当前状态和滚动位置
      this.saveState();

      // 更新阅读量并跳转
      request
        .put(`/blog/updateReadCount/${blogId}`)
        .then(() => {
          this.$router.push({
            path: "/front/blogDetail",
            query: { blogId: blogId },
          });
        })
        .catch((error) => {
          console.error("更新阅读量失败", error);
          this.$router.push({
            path: "/front/blogDetail",
            query: { blogId: blogId },
          });
        });
    },
    goToAuthorHome(userId) {
      if (userId) {
        this.$router.push({
          path: "/front/authorHome",
          query: { authorId: userId },
        });
      }
    },
    refreshList(categoryName, sortType) {
      console.log("刷新博客列表，分类:", categoryName, "排序:", sortType);

      if (categoryName) {
        this.categoryName = categoryName;
      }

      // 添加排序参数
      if (sortType) {
        this.customParams = {
          ...this.customParams,
          sortType: sortType,
        };
      }

      this.reset();
      this.load();
    },
    formatTags(tags) {
      try {
        const tagArray = JSON.parse(tags);
        return tagArray.join(", ");
      } catch {
        return tags;
      }
    },
    // 监听存储变化，检测用户角色变化
    handleStorageChange(event) {
      if (event.key === "xm-user") {
        console.log("用户信息已变更，重新加载博客列表");
        const newUserData = JSON.parse(event.newValue || "{}");
        const oldUserData = JSON.parse(event.oldValue || "{}");

        if (newUserData.browseRole !== oldUserData.browseRole) {
          this.currentUser = newUserData;
          this.reset();
          this.load();

          // 角色切换后刷新页面以确保所有组件正确加载
          setTimeout(() => {
            console.log("存储变化导致角色切换，刷新页面");
            window.location.reload();
          }, 300);
        }
      }
    },
    // 检查当前状态是否需要重新加载
    checkUserAndReload() {
      const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
      if (user.browseRole !== this.currentUser.browseRole) {
        console.log("用户角色不匹配，更新为:", user.browseRole);
        this.currentUser = user;
        this.reset();
        this.load();

        // 角色不匹配时刷新页面以确保所有组件正确加载
        setTimeout(() => {
          console.log("检测到角色不匹配，刷新页面");
          window.location.reload();
        }, 300);
      }
    },
    handleChangeBrowsingRole() {
      if (this.searchTitle) {
        this.reset();
        this.load();

        // 手动更改浏览角色后刷新页面
        setTimeout(() => {
          console.log("手动更改浏览角色，刷新页面");
          window.location.reload();
        }, 300);
      }
    },
    // 添加新方法处理搜索更新
    handleSearchUpdate(searchTitle) {
      console.log("处理搜索更新:", searchTitle);
      this.searchTitle = searchTitle;
      this.reset();
      this.load();
    },
  },
};
</script>

<style lang="less" scoped>
.blog-list-container {
  width: 100%;
}

.loading-container,
.empty-container {
  padding: 30px;
  background-color: var(--bg-color-secondary);
  border-radius: 8px;
  box-shadow: var(--card-shadow);
  text-align: center;
}

.empty-container {
  color: var(--text-color-secondary);

  i {
    font-size: 48px;
    margin-bottom: 10px;
  }

  p {
    font-size: 16px;
  }
}

.blog-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.blog-card {
  display: flex;
  height: 100%;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  background-color: var(--bg-color-secondary);

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px var(--shadow-color-hover);
    border-color: var(--primary-color);

    .blog-cover img {
      transform: scale(1.05);
    }
  }
}

.blog-cover {
  flex: 0 0 200px;
  width: 200px;
  height: auto;
  position: relative;
  overflow: hidden;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
  }

  .placeholder-img {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--bg-color-tertiary);
    color: var(--text-color-secondary);
    font-size: 24px;
  }
}

.blog-content {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-color-secondary);
}

.blog-title {
  margin: 0 0 15px;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color-primary);
  cursor: pointer;
  transition: color 0.3s;

  &:hover {
    color: var(--primary-color);
  }

  // 多行文本溢出省略
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.blog-description {
  margin: 0 0 15px;
  color: var(--text-color-regular);
  font-size: 14px;
  line-height: 1.6;
  flex: 1;

  // 多行文本溢出省略
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.blog-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: var(--text-color-secondary);
  margin-top: auto;

  .meta-left,
  .meta-right {
    display: flex;
    align-items: center;
    gap: 15px;
  }

  i {
    margin-right: 4px;
  }

  .blog-author,
  .blog-category {
    color: var(--primary-color);
    cursor: pointer;
    transition: color 0.3s;

    &:hover {
      color: var(--primary-color-hover);
    }
  }

  .blog-date,
  .blog-tags,
  .blog-views,
  .blog-likes {
    color: var(--text-color-secondary);
  }
}

.blog-actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}

.load-more-container {
  display: flex;
  justify-content: center;
  margin: 30px 0;
}

.load-more-btn {
  padding: 12px 30px;
  font-size: 16px;
  border-radius: 25px;
  background: var(--primary-gradient);
  border: none;
  color: var(--white);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--primary-shadow);
  }

  &:active {
    transform: translateY(0);
  }
}

/* 研究模式主题 - 知网风格 */
.research-theme {
  .blog-list {
    display: block;
    background: var(--bg-color-secondary);
    padding: 15px;
    border: 1px solid var(--border-color);
  }

  .blog-card {
    margin-bottom: 15px;
    border-radius: 4px;

    &:hover {
      transform: none;
      border-color: var(--primary-color);
    }
  }

  .blog-title {
    font-size: 16px;
    margin-bottom: 10px;
  }

  .blog-meta {
    font-size: 12px;
  }
}

/* 业余爱好者模式主题 - 摄影社区风格 */
.hobbyist-theme {
  .blog-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 25px;
    padding: 20px;
  }

  .blog-card {
    flex-direction: column;
    border-radius: 15px;
    overflow: hidden;
    background: var(--bg-color-secondary);
    transition: all 0.3s ease;

    &:hover {
      transform: translateY(-10px);
      box-shadow: 0 15px 30px var(--shadow-color-hover);
    }
  }

  .blog-cover {
    width: 100%;
    height: 220px;
    position: relative;

    &::after {
      content: "";
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 50%;
      background: linear-gradient(to top, var(--bg-color-alpha), transparent);
    }

    img {
      transition: transform 0.5s ease;
    }
  }

  .blog-content {
    padding: 20px;
    background: var(--bg-color-gradient);
  }

  .blog-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-color-primary);
    margin-bottom: 15px;
  }

  .blog-description {
    color: var(--text-color-regular);
    font-size: 14px;
    line-height: 1.6;
  }

  .blog-meta {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid var(--border-color-light);
  }

  .blog-author {
    color: var(--primary-color);
    font-weight: 500;
  }

  .load-more-btn {
    background: var(--primary-gradient);

    &:hover {
      background: var(--primary-gradient-hover);
    }
  }
}

/* 添加标签样式 */
.blog-tags {
  margin-left: 15px;
  color: var(--primary-color);

  i {
    margin-right: 4px;
  }
}

/* 全部加载完成提示样式 */
.all-loaded-message {
  color: var(--text-color-secondary);
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;

  i {
    color: var(--success-color);
  }
}

/* 编辑对话框样式 */
.el-dialog {
  background-color: var(--bg-color-secondary);
  border-radius: 8px;
  box-shadow: var(--card-shadow);

  .el-dialog__title {
    color: var(--text-color-primary);
  }

  .el-dialog__body {
    color: var(--text-color-regular);
  }
}

.cover-uploader {
  border: 1px dashed var(--border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;

  &:hover {
    border-color: var(--primary-color);
  }

  .cover-uploader-icon {
    font-size: 28px;
    color: var(--text-color-secondary);
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }

  .cover-image {
    width: 178px;
    height: 178px;
    display: block;
  }
}

/* 动画效果 */
.blog-list-enter-active,
.blog-list-leave-active {
  transition: all 0.5s ease;
}

.blog-list-enter,
.blog-list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

/* 加载更多按钮动画 */
.load-more-btn {
  font-size: 14px;
  position: relative;
  overflow: hidden;
  background: var(--bg-color-alpha);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-color-light);
  border-radius: 8px;
  padding: 8px 18px;
  color: var(--text-color-primary);
  transition: all 0.3s ease;
  margin: -10px auto;
  display: block;
  width: fit-content;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px var(--shadow-color);
    border-color: var(--primary-color);
    color: var(--primary-color);
  }

  &:active {
    transform: translateY(0);
  }

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      var(--highlight-color-alpha),
      transparent
    );
    animation: loading-shine 1.5s infinite;
  }

  i {
    margin-right: 5px;
  }
}

@keyframes loading-shine {
  100% {
    left: 100%;
  }
}

.loading-more-skeleton {
  margin-top: 20px;
  padding: 0 20px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 研究模式主题下的动画调整 */
.research-theme {
  .blog-list-enter {
    opacity: 0;
    transform: translateX(-20px);
  }

  .blog-list-leave-to {
    opacity: 0;
    transform: translateX(20px);
  }

  .load-more-btn {
    &::before {
      background: linear-gradient(
        90deg,
        transparent,
        var(--highlight-color-alpha-light),
        transparent
      );
    }
  }
}

/* 业余爱好者模式主题下的动画调整 */
.hobbyist-theme {
  .blog-list-enter {
    opacity: 0;
    transform: scale(0.95);
  }

  .blog-list-leave-to {
    opacity: 0;
    transform: scale(1.05);
  }

  .load-more-btn {
    &::before {
      background: linear-gradient(
        90deg,
        transparent,
        var(--highlight-color-alpha),
        transparent
      );
    }
  }
}

/* 加载容器样式优化 */
.loading-container {
  padding: 20px;
  background: var(--bg-color-alpha);
  border-radius: 8px;
  box-shadow: var(--card-shadow);
  backdrop-filter: blur(10px);
  animation: fadeIn 0.3s ease;
}

.edit-dialog {
  .el-dialog__body {
    padding: 20px;
  }

  .dialog-form {
    .form-item {
      margin-bottom: 20px;
    }

    .label {
      display: block;
      margin-bottom: 8px;
      font-weight: 500;
      color: var(--text-color-primary);
    }

    .input,
    .textarea,
    .select {
      width: 100%;
      padding: 10px;
      border: 1px solid var(--border-color);
      border-radius: 4px;
      background-color: var(--bg-color);
      color: var(--text-color-primary);

      &:focus {
        border-color: var(--primary-color);
        outline: none;
      }
    }

    .textarea {
      min-height: 100px;
      resize: vertical;
    }

    .tags-container {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 10px;
    }

    .tag {
      display: inline-flex;
      align-items: center;
      padding: 5px 10px;
      background-color: var(--bg-color-tertiary);
      color: var(--text-color-primary);
      border-radius: 15px;
      font-size: 13px;

      .remove-tag {
        margin-left: 5px;
        cursor: pointer;
        color: var(--text-color-secondary);

        &:hover {
          color: var(--danger-color);
        }
      }
    }

    .add-tag-input {
      display: flex;
      margin-top: 10px;

      input {
        flex: 1;
        padding: 8px;
        border: 1px solid var(--border-color);
        border-radius: 4px 0 0 4px;
        background-color: var(--bg-color);
        color: var(--text-color-primary);
      }

      button {
        padding: 8px 15px;
        background-color: var(--primary-color);
        color: var(--white);
        border: none;
        border-radius: 0 4px 4px 0;
        cursor: pointer;

        &:hover {
          background-color: var(--primary-color-hover);
        }
      }
    }
  }

  .dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;

    .cancel-btn {
      padding: 8px 15px;
      background-color: var(--bg-color-tertiary);
      color: var(--text-color-primary);
      border: 1px solid var(--border-color);
      border-radius: 4px;
      cursor: pointer;

      &:hover {
        background-color: var(--bg-color-hover);
      }
    }

    .submit-btn {
      padding: 8px 15px;
      background-color: var(--primary-color);
      color: var(--white);
      border: none;
      border-radius: 4px;
      cursor: pointer;

      &:hover {
        background-color: var(--primary-color-hover);
      }
    }
  }
}

.empty-state {
  text-align: center;
  padding: 50px 20px;
  background-color: var(--bg-color-secondary);
  border-radius: 8px;

  .empty-icon {
    font-size: 60px;
    color: var(--text-color-placeholder);
    margin-bottom: 20px;
  }

  .empty-text {
    font-size: 16px;
    color: var(--text-color-secondary);
    margin-bottom: 20px;
  }

  .create-btn {
    padding: 10px 20px;
    background-color: var(--primary-color);
    color: var(--white);
    border: none;
    border-radius: 4px;
    cursor: pointer;

    &:hover {
      background-color: var(--primary-color-hover);
    }
  }
}
</style>
