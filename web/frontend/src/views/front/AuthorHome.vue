<template>
  <div class="author-page">
    <div class="profile-container" v-loading="loading">
      <!-- 顶部背景区域 - 改进版的水下主题 -->
      <div class="csdn-header-background">
        <div class="wave-container">
          <div class="wave wave1"></div>
          <div class="wave wave2"></div>
          <div class="wave wave3"></div>
        </div>
        <div class="floating-bubbles">
          <div class="bubble bubble1"></div>
          <div class="bubble bubble2"></div>
          <div class="bubble bubble3"></div>
          <div class="bubble bubble4"></div>
          <div class="bubble bubble5"></div>
          <div class="bubble bubble6"></div>
          <div class="bubble bubble7"></div>
          <div class="bubble bubble8"></div>
        </div>
        <div class="swimming-fish">
          <div class="fish fish1"></div>
          <div class="fish fish2"></div>
          <div class="fish fish3"></div>
        </div>
        <div class="header-content-overlay"></div>
        <div class="csdn-container-width">
          <div class="header-content">
            <div class="author-brief">
              <div class="author-brief-title">
                {{ isOwnProfile ? "我的个人空间" : author.name + "的个人空间" }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 个人信息区 - 重构后的语义化结构 -->
      <div class="csdn-container-width">
        <section class="csdn-profile-card">
          <!-- 是否为自己的主页标识 -->
          <div v-if="isOwnProfile" class="csdn-badge">
            <i class="el-icon-user"></i> 我的主页
          </div>

          <div class="csdn-profile-layout">
            <!-- 左侧: 头像和基础数据 -->
            <aside class="csdn-profile-left">
              <header class="csdn-avatar-wrapper">
                <template v-if="isOwnProfile">
                  <div class="avatar-uploader">
                    <el-upload
                      class="avatar-upload"
                      :action="$baseUrl + '/files/upload'"
                      :headers="{ token: user.token }"
                      :show-file-list="false"
                      :on-success="handleAvatarSuccess"
                      :before-upload="beforeAvatarUpload"
                    >
                      <div class="csdn-avatar-container">
                        <img
                          v-if="author.avatar"
                          :src="author.avatar"
                          class="avatar-image"
                          alt="作者头像"
                        />
                        <i v-else class="el-icon-plus avatar-placeholder"></i>
                        <div class="avatar-hover-overlay">
                          <i class="el-icon-camera upload-icon"></i>
                          <span>更换头像</span>
                        </div>
                      </div>
                    </el-upload>
                  </div>
                </template>
                <template v-else>
                  <div class="csdn-avatar-container">
                    <img
                      :src="author.avatar || require('@/assets/imgs/bgc2.jpg')"
                      @error="handleAvatarError($event)"
                      alt="作者头像"
                      class="avatar-image"
                    />
                  </div>
                </template>
              </header>

              <!-- 完整统计数据 -->
              <div class="csdn-stats-detail">
                <section class="stat-card">
                  <div class="stat-grid">
                    <dl class="stat-grid-item">
                      <dd class="stat-value">{{ author.blogCount || 0 }}</dd>
                      <dt class="stat-label">文章</dt>
                    </dl>
                    <dl class="stat-grid-item">
                      <dd class="stat-value">{{ author.likesCount || 0 }}</dd>
                      <dt class="stat-label">获赞</dt>
                    </dl>
                    <dl class="stat-grid-item">
                      <dd class="stat-value">{{ author.collectCount || 0 }}</dd>
                      <dt class="stat-label">被收藏</dt>
                    </dl>
                    <dl class="stat-grid-item">
                      <dd class="stat-value">{{ author.followCount || 0 }}</dd>
                      <dt class="stat-label">关注</dt>
                    </dl>
                    <dl class="stat-grid-item">
                      <dd class="stat-value">{{ author.fansCount || 0 }}</dd>
                      <dt class="stat-label">粉丝</dt>
                    </dl>
                  </div>
                </section>

                <!-- 联系信息卡片 -->
                <address
                  class="contact-card"
                  v-if="author.phone || author.email"
                >
                  <h3 class="card-title">联系方式</h3>
                  <div class="contact-item" v-if="author.phone">
                    <i class="el-icon-phone"></i>
                    <span>{{ author.phone }}</span>
                  </div>
                  <div class="contact-item" v-if="author.email">
                    <i class="el-icon-message"></i>
                    <span>{{ author.email }}</span>
                  </div>
                </address>
              </div>
            </aside>

            <!-- 右侧: 用户信息和内容区 -->
            <main class="csdn-profile-right">
              <!-- 用户基本信息 -->
              <article class="csdn-user-info">
                <header class="user-header">
                  <h1 class="user-name">{{ author.name || "加载中..." }}</h1>
                  <div class="user-badges">
                    <span class="badge-item">
                      <i class="el-icon-user"></i> 博主
                    </span>
                    <span class="badge-item" v-if="author.blogCount > 10">
                      <i class="el-icon-medal"></i> 优质创作者
                    </span>
                  </div>
                </header>

                <p class="user-bio">
                  {{ author.info || "这个人很懒，什么都没留下" }}
                </p>

                <!-- 用户操作按钮 -->
                <div class="csdn-action-bar">
                  <template v-if="isOwnProfile">
                    <div class="primary-actions">
                      <el-button
                        type="success"
                        icon="el-icon-plus"
                        @click="$router.push('/front/newBlog')"
                        >写文章</el-button
                      >
                    </div>
                    <div class="secondary-actions">
                      <el-button
                        type="primary"
                        icon="el-icon-edit"
                        @click="showProfileDialog"
                        >编辑资料</el-button
                      >
                      <el-button
                        type="warning"
                        icon="el-icon-lock"
                        @click="updatePassword"
                        >修改密码</el-button
                      >
                    </div>
                  </template>
                  <template v-else>
                    <div class="primary-actions">
                      <el-button
                        v-if="
                          !isOwnProfile &&
                          author.id !== currentUserId &&
                          !isFollowing
                        "
                        class="csdn-follow-btn"
                        @click="toggleFollow"
                      >
                        <i class="el-icon-plus"></i>
                        关注
                      </el-button>
                      <el-button
                        v-else-if="
                          !isOwnProfile &&
                          author.id !== currentUserId &&
                          isFollowing
                        "
                        class="csdn-follow-btn already-following"
                        @click="toggleFollow"
                      >
                        <i class="el-icon-check"></i>
                        已关注
                      </el-button>
                    </div>
                    <div class="secondary-actions">
                      <el-button
                        type="text"
                        class="csdn-share-btn"
                        @click="shareProfile"
                      >
                        <i class="el-icon-share"></i> 分享
                      </el-button>
                    </div>
                  </template>
                </div>
              </article>

              <!-- 内容标签页导航 -->
              <nav class="csdn-tabs">
                <div class="scroll-container">
                  <div
                    v-for="tab in visibleTabs"
                    :key="tab.name"
                    class="csdn-tab-item"
                    :class="{ active: activeName === tab.name }"
                    @click="handleClick(tab)"
                  >
                    {{ tab.label }}
                    <span v-if="getTabCount(tab.name)" class="count-badge">
                      {{ getTabCount(tab.name) }}
                    </span>
                  </div>
                </div>
              </nav>

              <!-- 内容区 -->
              <div class="csdn-content-area">
                <div v-if="activeName === 'blogs'">
                  <blog-list
                    :custom-api="'/blog/selectUser'"
                    :custom-params="{ userId: Number(authorId) }"
                    :show-opt="isOwnProfile"
                    ref="blogList"
                    @data-loaded="handleBlogDataLoaded"
                  />
                </div>

                <div v-if="activeName === 'activities'">
                  <activity-list
                    :span="8"
                    :custom-api="'/activity/selectUser'"
                    :custom-params="{ userId: Number(authorId) }"
                    ref="activityList"
                    @data-loaded="handleActivityDataLoaded"
                  />
                </div>

                <!-- 显示作者关注的用户列表 -->
                <div v-if="activeName === 'follows'">
                  <div class="follows-container">
                    <div
                      v-if="followList.length === 0 && !followsLoading"
                      class="empty-follows"
                    >
                      <i class="el-icon-user"></i>
                      <p>暂无关注的用户</p>
                    </div>
                    <div v-else-if="followsLoading" class="follows-loading">
                      <i class="el-icon-loading"></i>
                      <p>正在加载关注列表...</p>
                    </div>
                    <div v-else class="follows-list">
                      <div
                        v-for="(user, index) in followList"
                        :key="index"
                        class="follow-item"
                      >
                        <div class="follow-user-avatar">
                          <img
                            :src="
                              user.avatar || require('@/assets/imgs/bgc2.jpg')
                            "
                            @error="handleAvatarError($event)"
                            alt="用户头像"
                          />
                        </div>
                        <div class="follow-user-info">
                          <div
                            class="follow-user-name"
                            @click="viewUserProfile(user.id)"
                          >
                            {{ user.name }}
                          </div>
                          <div class="follow-user-bio">
                            {{ user.info || "这个人很懒，什么都没留下" }}
                          </div>
                        </div>
                        <div class="follow-actions">
                          <el-button
                            v-if="
                              user.id !== currentUserId && !user.isFollowing
                            "
                            size="small"
                            type="primary"
                            @click="toggleFollowUser(user)"
                            :loading="user.loading"
                          >
                            关注
                          </el-button>
                          <el-button
                            v-else-if="
                              user.id !== currentUserId && user.isFollowing
                            "
                            size="small"
                            type="primary"
                            class="already-following"
                            @click="toggleFollowUser(user)"
                            :loading="user.loading"
                          >
                            已关注
                          </el-button>
                          <span
                            v-else-if="user.id === currentUserId"
                            class="self-tag"
                          >
                            <i class="el-icon-user"></i> 我
                          </span>
                        </div>
                      </div>

                      <!-- 分页控制 -->
                      <el-pagination
                        v-if="followList.length > 0"
                        @current-change="handleFollowsPageChange"
                        :current-page.sync="followsPage"
                        :page-size="followsPageSize"
                        layout="prev, pager, next"
                        :total="followsTotal"
                        class="follows-pagination"
                      >
                      </el-pagination>
                    </div>
                  </div>
                </div>

                <!-- 显示粉丝列表 -->
                <div v-if="activeName === 'fans'">
                  <div class="follows-container">
                    <div
                      v-if="fansList.length === 0 && !fansLoading"
                      class="empty-follows"
                    >
                      <i class="el-icon-user"></i>
                      <p>暂无粉丝</p>
                    </div>
                    <div v-else-if="fansLoading" class="follows-loading">
                      <i class="el-icon-loading"></i>
                      <p>正在加载粉丝列表...</p>
                    </div>
                    <div v-else class="follows-list">
                      <div
                        v-for="(user, index) in fansList"
                        :key="index"
                        class="follow-item"
                      >
                        <div class="follow-user-avatar">
                          <img
                            :src="
                              user.avatar || require('@/assets/imgs/bgc2.jpg')
                            "
                            @error="handleAvatarError($event)"
                            alt="用户头像"
                          />
                        </div>
                        <div class="follow-user-info">
                          <div
                            class="follow-user-name"
                            @click="viewUserProfile(user.id)"
                          >
                            {{ user.name }}
                          </div>
                          <div class="follow-user-bio">
                            {{ user.info || "这个人很懒，什么都没留下" }}
                          </div>
                        </div>
                        <div class="follow-actions">
                          <el-button
                            v-if="
                              user.id !== currentUserId && !user.isFollowing
                            "
                            size="small"
                            type="primary"
                            @click="toggleFollowUser(user)"
                            :loading="user.loading"
                          >
                            关注
                          </el-button>
                          <el-button
                            v-else-if="
                              user.id !== currentUserId && user.isFollowing
                            "
                            size="small"
                            type="primary"
                            class="already-following"
                            @click="toggleFollowUser(user)"
                            :loading="user.loading"
                          >
                            已关注
                          </el-button>
                          <span
                            v-else-if="user.id === currentUserId"
                            class="self-tag"
                          >
                            <i class="el-icon-user"></i> 我
                          </span>
                        </div>
                      </div>

                      <!-- 分页控制 -->
                      <el-pagination
                        v-if="fansList.length > 0"
                        @current-change="handleFansPageChange"
                        :current-page.sync="fansPage"
                        :page-size="fansPageSize"
                        layout="prev, pager, next"
                        :total="fansTotal"
                        class="follows-pagination"
                      >
                      </el-pagination>
                    </div>
                  </div>
                </div>

                <!-- 如果是本人，显示更多选项卡内容 -->
                <div v-if="activeName === 'likes' && isOwnProfile">
                  <div class="csdn-content-filter">
                    <el-radio-group v-model="likesCurrent" size="medium">
                      <el-radio-button label="博客">博客</el-radio-button>
                      <el-radio-button label="活动">活动</el-radio-button>
                    </el-radio-group>
                  </div>
                  <blog-list
                    v-if="likesCurrent === '博客'"
                    :custom-api="'/blog/selectLike'"
                    :custom-params="{ userId: authorId }"
                    ref="blogLikesList"
                    @data-loaded="handleBlogLikesDataLoaded"
                  ></blog-list>
                  <activity-list
                    v-if="likesCurrent === '活动'"
                    :span="8"
                    :custom-api="'/activity/selectLike'"
                    :custom-params="{ userId: authorId }"
                    ref="activityLikesList"
                  ></activity-list>
                </div>

                <div v-if="activeName === 'collections' && isOwnProfile">
                  <div class="csdn-content-filter">
                    <el-radio-group v-model="collectCurrent" size="medium">
                      <el-radio-button label="博客">博客</el-radio-button>
                      <el-radio-button label="活动">活动</el-radio-button>
                    </el-radio-group>
                  </div>
                  <blog-list
                    v-if="collectCurrent === '博客'"
                    :custom-api="'/blog/selectCollect'"
                    :custom-params="{ userId: authorId }"
                    ref="blogCollectionsList"
                    @data-loaded="handleBlogCollectionsDataLoaded"
                  ></blog-list>
                  <activity-list
                    v-if="collectCurrent === '活动'"
                    :span="8"
                    :custom-api="'/activity/selectCollect'"
                    :custom-params="{ userId: authorId }"
                    ref="activityCollectionsList"
                  ></activity-list>
                </div>

                <div v-if="activeName === 'comments' && isOwnProfile">
                  <div class="csdn-content-filter">
                    <el-radio-group v-model="commentCurrent" size="medium">
                      <el-radio-button label="博客">博客</el-radio-button>
                      <el-radio-button label="活动">活动</el-radio-button>
                    </el-radio-group>
                  </div>
                  <blog-list
                    v-if="commentCurrent === '博客'"
                    :custom-api="'/blog/selectComment'"
                    :custom-params="{ userId: authorId }"
                    ref="blogCommentsList"
                    @data-loaded="handleBlogCommentsDataLoaded"
                  ></blog-list>
                  <activity-list
                    v-if="commentCurrent === '活动'"
                    :span="8"
                    :custom-api="'/activity/selectComment'"
                    :custom-params="{ userId: authorId }"
                    ref="activityCommentsList"
                  ></activity-list>
                </div>
              </div>
            </main>
          </div>
        </section>
      </div>
    </div>

    <!-- 编辑个人资料对话框 -->
    <el-dialog
      title="编辑个人资料"
      :visible.sync="profileDialogVisible"
      width="500px"
      :close-on-click-modal="false"
      custom-class="csdn-dialog"
    >
      <el-form :model="user" label-width="80px" class="person-form">
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="user.username"
            placeholder="用户名"
            disabled
          ></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="user.name" placeholder="姓名"></el-input>
        </el-form-item>
        <el-form-item label="简介" prop="info">
          <el-input
            type="textarea"
            :rows="3"
            v-model="user.info"
            placeholder="个人简介"
          ></el-input>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="user.phone" placeholder="电话"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="user.email" placeholder="邮箱"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="profileDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="updateProfile">保存</el-button>
      </div>
    </el-dialog>

    <!-- 修改密码对话框 -->
    <el-dialog
      title="修改密码"
      :visible.sync="passwordDialogVisible"
      width="500px"
      :close-on-click-modal="false"
      destroy-on-close
      custom-class="csdn-dialog"
    >
      <el-form
        :model="passwordForm"
        label-width="100px"
        :rules="passwordRules"
        ref="passwordFormRef"
      >
        <el-form-item label="原始密码" prop="password">
          <el-input
            show-password
            v-model="passwordForm.password"
            placeholder="请输入原始密码"
          ></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input
            show-password
            v-model="passwordForm.newPassword"
            placeholder="请输入新密码"
          ></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            show-password
            v-model="passwordForm.confirmPassword"
            placeholder="请再次输入新密码"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="passwordDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="savePassword">确定</el-button>
      </div>
    </el-dialog>

    <!-- 添加角色标识 -->
    <div class="role-badge" :class="userRole">
      {{
        userRole === "RESEARCHER"
          ? "科研人员"
          : userRole === "HOBBYIST"
          ? "爱好者"
          : "全部"
      }}
    </div>
  </div>
</template>

<script>
import BlogList from "@/components/BlogList";
import ActivityList from "@/components/ActivityList";
import request from "@/utils/request";

export default {
  name: "AuthorHome",
  components: {
    BlogList,
    ActivityList,
  },
  data() {
    // 密码确认验证函数
    const validatePassword = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请确认密码"));
      } else if (value !== this.passwordForm.newPassword) {
        callback(new Error("确认密码错误"));
      } else {
        callback();
      }
    };

    return {
      authorId: null,
      author: {},
      activeName: "blogs",
      loading: true,
      isOwnProfile: false,
      isFollowing: false,
      likesCurrent: "博客",
      collectCurrent: "博客",
      commentCurrent: "博客",
      profileDialogVisible: false,
      passwordDialogVisible: false,
      followLoading: false,
      followList: [],
      followsLoading: false,
      followsPage: 1,
      followsPageSize: 10,
      followsTotal: 0,
      fansList: [],
      fansLoading: false,
      fansPage: 1,
      fansPageSize: 10,
      fansTotal: 0,
      user: JSON.parse(localStorage.getItem("xm-user") || "{}"),
      pythonServiceUrl:
        process.env.VUE_APP_PYTHON_URL || "http://localhost:8000",
      passwordForm: {
        password: "",
        newPassword: "",
        confirmPassword: "",
      },
      passwordRules: {
        password: [
          { required: true, message: "请输入原始密码", trigger: "blur" },
        ],
        newPassword: [
          { required: true, message: "请输入新密码", trigger: "blur" },
          { min: 6, message: "密码长度不能小于6位", trigger: "blur" },
        ],
        confirmPassword: [
          { validator: validatePassword, required: true, trigger: "blur" },
        ],
      },
      tabs: [
        { name: "blogs", label: "发布的博客", requireOwner: false },
        { name: "activities", label: "参与的活动", requireOwner: false },
        { name: "follows", label: "关注的用户", requireOwner: false },
        { name: "fans", label: "粉丝", requireOwner: false },
        { name: "likes", label: "我的点赞", requireOwner: true },
        { name: "collections", label: "我的收藏", requireOwner: true },
        { name: "comments", label: "我的评论", requireOwner: true },
      ],
      _activeNameChangedByClick: false,
      currentRole: "", // 当前角色
      currentUserId: null, // 添加当前用户ID
      userRole: "", // 添加用户角色状态
    };
  },
  computed: {
    visibleTabs() {
      return this.tabs.filter((tab) => !tab.requireOwner || this.isOwnProfile);
    },
  },
  created() {
    // 初始化加载用户信息
    this.initUserData();
  },
  mounted() {
    // 监听路由变化，当authorId变化时重新加载数据
    this.$watch(
      () => this.$route.query.authorId,
      (newAuthorId, oldAuthorId) => {
        if (newAuthorId !== oldAuthorId) {
          console.log(
            `路由参数变化: authorId从${oldAuthorId}变为${newAuthorId}`
          );
          this.initUserData();
        }
      }
    );
  },
  methods: {
    // 初始化用户数据的方法
    initUserData() {
      // 从URL获取作者ID
      const authorId = this.$route.query.authorId;

      // 确保authorId是数字类型
      this.authorId = authorId ? parseInt(authorId) : null;

      console.log("初始化用户数据，获取到的authorId:", authorId);
      console.log(
        "转换后的authorId:",
        this.authorId,
        "类型:",
        typeof this.authorId
      );

      // 如果URL中没有指定作者ID，则使用当前登录用户
      if (!this.authorId) {
        const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
        if (user.id) {
          this.authorId = parseInt(user.id);
          console.log("使用当前登录用户ID作为作者ID:", this.authorId);
        } else {
          console.warn("未找到作者ID且用户未登录");
          this.$router.push("/login");
          return;
        }
      }

      // 重置页面状态
      this.isFollowing = false;
      this.followList = [];
      this.fansList = [];
      this.followsPage = 1;
      this.fansPage = 1;

      // 初始化用户数据
      this.user = JSON.parse(localStorage.getItem("xm-user") || "{}");

      // 判断是否是查看自己的主页
      this.isOwnProfile =
        this.user.id && parseInt(this.user.id) === this.authorId;
      console.log("当前登录用户:", this.user);
      console.log("查看的作者ID:", this.authorId);
      console.log("是否查看自己的主页:", this.isOwnProfile);

      // 默认激活选项卡
      this.activeName = "blogs";

      // 加载作者信息
      this.loadAuthorInfo().then(() => {
        // 加载完作者信息后，检查关注状态
        if (!this.isOwnProfile && this.user.token) {
          this.checkFollowStatus();
        }

        // 根据当前激活的标签加载相应数据
        this.$nextTick(() => {
          this.loadActiveTabData();
        });
      });

      // 获取当前用户的浏览角色
      const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
      this.currentRole = user.browseRole || "ALL";

      // 获取当前用户ID
      this.currentUserId = user.id;

      // 确保pythonServiceUrl末尾没有斜杠（如果存在）
      if (this.pythonServiceUrl) {
        this.pythonServiceUrl = this.pythonServiceUrl.replace(/\/$/, "");
        if (process.env.NODE_ENV === "development") {
          console.log("Python服务URL:", this.pythonServiceUrl);
        }
      }
    },
    // 加载作者信息
    async loadAuthorInfo() {
      this.loading = true;
      try {
        const res = await request.get(`/user/selectById/${this.authorId}`);

        if (res.code === "200") {
          this.author = res.data || {};

          // 再次检查是否是当前用户的主页
          const currentUser = JSON.parse(
            localStorage.getItem("xm-user") || "{}"
          );
          if (currentUser.id) {
            // 转为字符串进行比较
            const currentUserId = String(currentUser.id);
            const authorId = String(this.author.id || this.authorId);
            this.isOwnProfile = currentUserId === authorId;
            console.log("数据加载后再次判断是否为个人主页:", this.isOwnProfile);
          }

          // 如果是自己的主页，复制用户信息到user对象（不要覆盖已有的user）
          if (this.isOwnProfile && !this.user.token) {
            this.user = { ...this.author };
          }

          // 确保作者统计数据有默认值
          this.author.blogCount = this.author.blogCount || 0;
          this.author.likesCount = this.author.likesCount || 0;
          this.author.collectCount = this.author.collectCount || 0;
          this.author.fansCount = this.author.fansCount || 0;
          this.author.followCount = this.author.followCount || 0;

          // 从用户资料接口刷新作者统计数据
          try {
            const statsRes = await request.get(
              `/user/refreshStats/${this.authorId}`
            );
            if (statsRes.code === "200") {
              console.log("统计数据刷新成功");

              // 重新获取更新后的作者数据
              const updatedRes = await request.get(
                `/user/selectById/${this.authorId}`
              );
              if (updatedRes.code === "200" && updatedRes.data) {
                // 只更新统计相关字段，保留其他作者信息
                this.author.blogCount =
                  updatedRes.data.blogCount || this.author.blogCount;
                this.author.likesCount =
                  updatedRes.data.likesCount || this.author.likesCount;
                this.author.collectCount =
                  updatedRes.data.collectCount || this.author.collectCount;
                this.author.fansCount =
                  updatedRes.data.fansCount || this.author.fansCount;
                this.author.followCount =
                  updatedRes.data.followCount || this.author.followCount;

                console.log("更新后的作者统计数据:", {
                  blogCount: this.author.blogCount,
                  likesCount: this.author.likesCount,
                  collectCount: this.author.collectCount,
                  fansCount: this.author.fansCount,
                  followCount: this.author.followCount,
                });
              }
            }
          } catch (statsErr) {
            console.warn("刷新统计数据失败:", statsErr);
            // 如果刷新失败，尝试从博客详情或计算方式获取
            await this.tryGetStatsFromBlog();
          }

          console.log("最终的作者信息：", this.author);

          // 设置页面标题
          document.title = `${this.author.name || "作者"} 的主页 - 水下社区`;
        } else {
          this.$message.error(res.msg || "获取作者信息失败");
          this.$router.push("/front/home");
        }
      } catch (err) {
        console.error("获取作者信息失败", err);
        this.$message.error("获取作者信息失败，请稍后重试");
        this.$router.push("/front/home");
      } finally {
        setTimeout(() => {
          this.loading = false;
        }, 300); // 添加小延迟以展示加载效果
      }
    },

    // 尝试从博客详情中获取作者统计数据
    async tryGetStatsFromBlog() {
      try {
        console.log(
          "尝试从博客详情获取作者统计数据，作者ID:",
          this.authorId,
          "类型:",
          typeof this.authorId
        );

        // 首先获取作者的一篇博客
        const blogListRes = await request.get(`/blog/selectUser`, {
          params: {
            userId: Number(this.authorId),
            pageNum: 1,
            pageSize: 1,
          },
        });

        console.log("获取博客列表的API响应:", blogListRes);

        if (blogListRes.code === "200" && blogListRes.data) {
          let blogs = [];

          if (Array.isArray(blogListRes.data)) {
            blogs = blogListRes.data;
          } else if (blogListRes.data.records) {
            blogs = blogListRes.data.records;
          } else if (blogListRes.data.list) {
            blogs = blogListRes.data.list;
          }

          // 如果找到了至少一篇博客
          if (blogs.length > 0) {
            const firstBlog = blogs[0];
            console.log("找到作者博客:", firstBlog);

            // 获取博客详情，以获取包含作者完整信息的响应
            const blogDetailRes = await request.get(
              `/blog/selectById/${firstBlog.id}`
            );

            console.log("获取博客详情的API响应:", blogDetailRes);

            if (
              blogDetailRes.code === "200" &&
              blogDetailRes.data &&
              blogDetailRes.data.user
            ) {
              // 从博客详情中提取作者信息
              const authorInfo = blogDetailRes.data.user;
              console.log("从博客详情中获取的作者信息：", authorInfo);

              // 更新作者统计数据
              this.author.blogCount =
                authorInfo.blogCount || this.author.blogCount;
              this.author.likesCount =
                authorInfo.likesCount || this.author.likesCount;
              this.author.collectCount =
                authorInfo.collectCount || this.author.collectCount;
              this.author.fansCount =
                authorInfo.fansCount || this.author.fansCount;
              this.author.followCount =
                authorInfo.followCount || this.author.followCount;
            } else {
              console.warn("无法从博客详情中获取作者信息，将使用计算方法");
              await this.calculateAuthorStats();
            }
          } else {
            console.warn("该作者没有博客，将使用基本统计数据");
          }
        } else {
          console.warn("获取作者博客列表失败，将使用计算方法");
          await this.calculateAuthorStats();
        }
      } catch (err) {
        console.error("获取作者博客信息失败", err);
        await this.calculateAuthorStats();
      }
    },

    // 计算作者统计数据的方法
    async calculateAuthorStats() {
      try {
        console.log(
          "开始计算作者统计数据，作者ID:",
          this.authorId,
          "类型:",
          typeof this.authorId
        );

        const blogRes = await request.get(`/blog/selectUser`, {
          params: { userId: Number(this.authorId) },
        });

        console.log("计算统计数据的API响应:", blogRes);

        if (blogRes.code === "200" && blogRes.data) {
          // 更新博客数量
          const blogs = Array.isArray(blogRes.data)
            ? blogRes.data
            : blogRes.data.records || blogRes.data.list || [];
          this.author.blogCount = blogs.length;

          // 计算获赞总数和收藏总数
          let totalLikes = 0;
          let totalCollects = 0;

          blogs.forEach((blog) => {
            totalLikes += parseInt(blog.likesCount || 0);
            totalCollects += parseInt(blog.collectCount || 0);
          });

          this.author.likesCount = totalLikes;
          this.author.collectCount = totalCollects;

          console.log("计算的统计数据：", {
            blogCount: this.author.blogCount,
            likesCount: this.author.likesCount,
            collectCount: this.author.collectCount,
          });
        }
      } catch (err) {
        console.error("计算作者统计数据失败", err);
      }
    },

    // 检查是否已关注
    async checkFollowStatus() {
      // 检查是否登录
      if (!this.user.token) {
        return;
      }

      try {
        this.loading = true;

        // 确保ID是数字类型
        const followerId = parseInt(this.user.id);
        const followedId = parseInt(this.authorId);

        console.log("检查关注状态参数:", {
          followerId: followerId,
          followedId: followedId,
          followerId类型: typeof followerId,
          followedId类型: typeof followedId,
        });

        // 实际API调用以检查关注状态
        const res = await request.get("/follow/checkStatus", {
          params: {
            followerId: followerId, // 确保是数字类型
            followedId: followedId, // 确保是数字类型
          },
        });

        if (res.code === "200") {
          this.isFollowing = res.data;
        } else {
          // 如果API不存在，使用模拟数据
          console.warn("关注状态API不可用，使用模拟数据");
          this.isFollowing = Math.random() > 0.5;
        }
      } catch (error) {
        console.error("获取关注状态失败", error);
        // 默认为未关注
        this.isFollowing = false;
      } finally {
        this.loading = false;
      }
    },

    // 处理标签页切换事件
    handleClick(tab) {
      console.log("标签切换到:", tab.name);
      console.log("当前作者ID:", this.authorId, "类型:", typeof this.authorId);
      console.log("切换前activeName:", this.activeName);

      // 设置标志，表示此次activeName变化是由点击触发的
      this._activeNameChangedByClick = true;

      // 更新当前选中的标签
      this.activeName = tab.name;

      console.log("切换后activeName:", this.activeName);
      console.log("当前可见标签:", this.visibleTabs);

      // 在不同标签页之间切换时加载相应数据
      if (tab.name === "follows") {
        console.log("开始加载关注列表...");
        this.loadFollowList();
      } else if (tab.name === "fans") {
        console.log("开始加载粉丝列表...");
        this.loadFansList();
      } else if (tab.name === "blogs") {
        console.log("开始重新加载博客列表...");
        // 使用nextTick确保DOM已更新
        this.$nextTick(() => {
          if (this.$refs.blogList) {
            console.log(
              "重置博客列表并加载，作者ID:",
              this.authorId,
              "类型:",
              typeof this.authorId,
              "数字类型:",
              Number(this.authorId)
            );
            this.$refs.blogList.reset();
            this.$refs.blogList.load();
          } else {
            console.warn("博客列表组件尚未挂载");
          }
        });
      } else if (tab.name === "activities") {
        console.log("开始重新加载活动列表...");
        // 使用nextTick确保DOM已更新
        this.$nextTick(() => {
          if (this.$refs.activityList) {
            console.log(
              "重置活动列表并加载，作者ID:",
              this.authorId,
              "类型:",
              typeof this.authorId,
              "数字类型:",
              Number(this.authorId)
            );
            this.$refs.activityList.reset();
            this.$refs.activityList.load(1);
          } else {
            console.warn("活动列表组件尚未挂载");
          }
        });
      } else if (tab.name === "likes" && this.isOwnProfile) {
        // 处理点赞标签页
        this.$nextTick(() => {
          if (this.likesCurrent === "博客") {
            console.log("加载用户点赞的博客，用户ID:", this.authorId);
            const blogList = this.$refs.blogLikesList;
            if (blogList) {
              blogList.reset();
              blogList.load();
            }
          } else if (this.likesCurrent === "活动") {
            console.log("加载用户点赞的活动，用户ID:", this.authorId);
            const activityList = this.$refs.activityLikesList;
            if (activityList) {
              activityList.reset();
              activityList.load(1);
            }
          }
        });
      } else if (tab.name === "collections" && this.isOwnProfile) {
        // 处理收藏标签页
        this.$nextTick(() => {
          if (this.collectCurrent === "博客") {
            console.log("加载用户收藏的博客，用户ID:", this.authorId);
            const blogList = this.$refs.blogCollectionsList;
            if (blogList) {
              blogList.reset();
              blogList.load();
            }
          } else if (this.collectCurrent === "活动") {
            console.log("加载用户收藏的活动，用户ID:", this.authorId);
            const activityList = this.$refs.activityCollectionsList;
            if (activityList) {
              activityList.reset();
              activityList.load(1);
            }
          }
        });
      } else if (tab.name === "comments" && this.isOwnProfile) {
        // 处理评论标签页
        this.$nextTick(() => {
          if (this.commentCurrent === "博客") {
            console.log("加载用户评论的博客，用户ID:", this.authorId);
            const blogList = this.$refs.blogCommentsList;
            if (blogList) {
              blogList.reset();
              blogList.load();
            }
          } else if (this.commentCurrent === "活动") {
            console.log("加载用户评论的活动，用户ID:", this.authorId);
            const activityList = this.$refs.activityCommentsList;
            if (activityList) {
              activityList.reset();
              activityList.load(1);
            }
          }
        });
      } else {
        console.log("没有为当前标签配置特殊加载逻辑");
      }
    },

    // 处理头像加载失败的情况
    handleAvatarError(e) {
      // 使用正确的相对路径
      e.target.src = require("@/assets/imgs/bgc2.jpg");
      console.log("头像加载失败，使用默认头像");
    },

    // 处理头像上传成功后的逻辑
    handleAvatarSuccess(response) {
      if (response.code === "200") {
        this.user.avatar = response.data;
        this.author.avatar = response.data;
        this.$message.success("头像上传成功");

        // 更新用户信息
        this.updateProfile();
      } else {
        this.$message.error(response.msg || "上传失败");
      }
    },

    // 处理头像上传前的验证
    beforeAvatarUpload(file) {
      const isImage = file.type.startsWith("image/");
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isImage) {
        this.$message.error("上传头像图片只能是图片格式!");
        return false;
      }
      if (!isLt2M) {
        this.$message.error("上传头像图片大小不能超过 2MB!");
        return false;
      }
      return true;
    },

    // 显示编辑个人资料对话框
    showProfileDialog() {
      this.profileDialogVisible = true;
    },

    // 更新用户信息
    updateProfile() {
      request
        .put("/user/update", this.user)
        .then((res) => {
          if (res.code === "200") {
            this.$message.success("保存成功");

            // 更新本地存储
            localStorage.setItem("xm-user", JSON.stringify(this.user));

            // 关闭对话框
            this.profileDialogVisible = false;

            // 更新作者信息
            this.author = { ...this.user };
          } else {
            this.$message.error(res.msg || "保存失败");
          }
        })
        .catch((err) => {
          console.error("保存用户信息失败", err);
          this.$message.error("保存失败，请稍后重试");
        });
    },

    // 显示修改密码对话框
    updatePassword() {
      // 重置表单
      this.passwordForm = {
        password: "",
        newPassword: "",
        confirmPassword: "",
      };
      this.passwordDialogVisible = true;
    },

    // 保存新密码
    savePassword() {
      this.$refs.passwordFormRef.validate((valid) => {
        if (valid) {
          const data = {
            ...this.user,
            password: this.passwordForm.password,
            newPassword: this.passwordForm.newPassword,
          };

          request
            .put("/updatePassword", data)
            .then((res) => {
              if (res.code === "200") {
                this.$message.success("修改密码成功");
                this.passwordDialogVisible = false;

                // 提示重新登录
                this.$confirm("密码已修改，需要重新登录", "提示", {
                  confirmButtonText: "确定",
                  cancelButtonText: "稍后登录",
                  type: "warning",
                })
                  .then(() => {
                    // 清除登录信息并跳转到登录页
                    localStorage.removeItem("xm-user");
                    this.$router.push("/login");
                  })
                  .catch(() => {
                    // 用户选择稍后登录，不做任何操作
                  });
              } else {
                this.$message.error(res.msg || "修改密码失败");
              }
            })
            .catch((err) => {
              console.error("修改密码失败", err);
              this.$message.error("修改密码失败，请稍后重试");
            });
        }
      });
    },

    // 处理关注和取消关注逻辑
    async toggleFollow() {
      // 检查是否登录
      if (!this.user.token) {
        this.$message.warning("请先登录后再关注");
        this.$router.push("/login");
        return;
      }

      if (this.followLoading) return; // 防止重复点击
      this.followLoading = true;

      try {
        const action = this.isFollowing ? "unfollow" : "follow";
        // 保存原有状态，以便恢复
        const originalFollowingState = this.isFollowing;

        // 确保ID是数字类型
        const followerId = parseInt(this.user.id);
        const followedId = parseInt(this.authorId);

        console.log("关注/取消关注参数:", {
          followerId: followerId,
          followedId: followedId,
          followerId类型: typeof followerId,
          followedId类型: typeof followedId,
        });

        // 先乐观地更新UI状态
        this.isFollowing = !originalFollowingState;

        // 同时更新列表中同一用户的关注状态（如果存在）
        this.updateListUserFollowStatus(followedId, !originalFollowingState);

        // 实际API调用
        const res = await request.post(`/follow/${action}`, {
          followerId: followerId, // 确保是数字类型
          followedId: followedId, // 确保是数字类型
        });

        if (res.code === "200") {
          // 操作成功
          if (this.isFollowing) {
            // 更新粉丝数量
            this.author.fansCount = (this.author.fansCount || 0) + 1;
            // 更新当前用户的关注数量
            this.user.followCount = (this.user.followCount || 0) + 1;
            // 更新本地存储的用户信息
            localStorage.setItem("xm-user", JSON.stringify(this.user));
            this.$message.success("关注成功");
          } else {
            // 更新粉丝数量
            this.author.fansCount = Math.max(
              0,
              (this.author.fansCount || 0) - 1
            );
            // 更新当前用户的关注数量
            this.user.followCount = Math.max(
              0,
              (this.user.followCount || 0) - 1
            );
            // 更新本地存储的用户信息
            localStorage.setItem("xm-user", JSON.stringify(this.user));
            this.$message.success("已取消关注");
          }
        } else {
          // 操作失败，恢复状态
          this.isFollowing = originalFollowingState;
          // 同时恢复列表中同一用户的关注状态（如果存在）
          this.updateListUserFollowStatus(followedId, originalFollowingState);

          // 提示用户具体错误
          if (originalFollowingState && action === "follow") {
            this.$message.warning("您已经关注过该用户");
          } else if (!originalFollowingState && action === "unfollow") {
            this.$message.warning("您尚未关注该用户");
          } else {
            this.$message.error(res.msg || "操作失败，请稍后重试");
          }
        }
      } catch (error) {
        console.error("操作关注失败", error);
        // 出错时恢复状态
        this.isFollowing = !this.isFollowing;

        // 同时恢复列表中同一用户的关注状态（如果存在）
        this.updateListUserFollowStatus(
          parseInt(this.authorId),
          !this.isFollowing
        );

        this.$message.error("操作失败，请稍后重试");
      } finally {
        this.followLoading = false;
      }
    },

    // 发送消息
    sendMessage() {
      // 检查是否登录
      if (!this.user.token) {
        this.$message.warning("请先登录后再发送消息");
        this.$router.push("/login");
        return;
      }

      // 模拟发送消息
      this.$message.info("消息功能开发中，敬请期待");
    },

    // 分享个人资料
    shareProfile() {
      // 获取当前页面URL
      const url = window.location.href;

      // 尝试使用现代浏览器API
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard
          .writeText(url)
          .then(() => {
            this.$message({
              message: "链接已复制到剪贴板",
              type: "success",
              duration: 2000,
            });
          })
          .catch(() => {
            this.fallbackCopy(url);
          });
      } else {
        this.fallbackCopy(url);
      }
    },

    // 降级复制方法
    fallbackCopy(text) {
      // 创建临时文本区域
      const textArea = document.createElement("textarea");
      textArea.value = text;
      textArea.style.position = "fixed";
      textArea.style.left = "-9999px";
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();

      try {
        const successful = document.execCommand("copy");
        if (successful) {
          this.$message({
            message: "链接已复制到剪贴板",
            type: "success",
            duration: 2000,
          });
        } else {
          this.$message.error("复制失败，请手动复制链接");
        }
      } catch (err) {
        this.$message.error("复制失败，请手动复制链接");
      }

      document.body.removeChild(textArea);
    },

    // 加载关注列表
    async loadFollowList() {
      this.followsLoading = true;
      try {
        console.log(
          "开始加载关注列表，作者ID:",
          this.authorId,
          "类型:",
          typeof this.authorId
        );

        // 调用API获取关注列表
        const res = await request.get("/follow/getFollows", {
          params: {
            userId: Number(this.authorId),
            pageNum: this.followsPage,
            pageSize: this.followsPageSize,
            currentUserId: this.user.id, // 添加当前登录用户ID，用于后端判断关注状态
          },
        });

        console.log("获取关注列表API响应:", res);

        if (res.code === "200") {
          // 处理API响应数据
          if (res.data && Array.isArray(res.data.records)) {
            // 如果后端已返回isFollowing状态，则直接使用
            this.followList = res.data.records.map((item) => ({
              ...item,
              isFollowing: item.isFollowing || false,
              loading: false,
            }));

            // 如果需要，可以在这里调用批量检查关注状态的API
            if (this.user.token && this.followList.length > 0) {
              await this.checkUsersFollowStatus(this.followList);

              // 检查列表中是否包含当前页面主人（author），如果有则同步全局isFollowing状态
              this.syncFollowingStatus();
            }

            this.followsTotal = res.data.total || 0;
            // 确保更新的是作者的数据
            this.author.followCount = this.followsTotal;
            console.log(
              `更新作者(ID:${this.authorId})的关注数为: ${this.author.followCount}`
            );
          } else if (res.data && Array.isArray(res.data)) {
            this.followList = res.data.map((item) => ({
              ...item,
              isFollowing: item.isFollowing || false,
              loading: false,
            }));

            // 如果需要，可以在这里调用批量检查关注状态的API
            if (this.user.token && this.followList.length > 0) {
              await this.checkUsersFollowStatus(this.followList);

              // 检查列表中是否包含当前页面主人（author），如果有则同步全局isFollowing状态
              this.syncFollowingStatus();
            }

            this.followsTotal = res.data.length;
            // 确保更新的是作者的数据
            this.author.followCount = this.followsTotal;
            console.log(
              `更新作者(ID:${this.authorId})的关注数为: ${this.author.followCount}`
            );
          } else {
            // 没有数据
            this.followList = [];
            this.followsTotal = 0;
            this.author.followCount = 0;
          }
        } else {
          // 模拟关注列表数据
          console.warn("获取关注列表API不可用，使用模拟数据");
          this.generateMockFollowList();
        }
      } catch (error) {
        console.error("获取关注列表失败", error);
        // 失败时使用模拟数据
        this.generateMockFollowList();
      } finally {
        this.followsLoading = false;
      }
    },

    // 生成模拟关注列表数据
    generateMockFollowList() {
      const mockUsers = [
        {
          id: 1,
          name: "水下摄影师",
          info: "专注水下摄影10年，分享水下世界的美丽",
          avatar: require("@/assets/imgs/bgc2.jpg"),
          isFollowing: true,
        },
        {
          id: 2,
          name: "深海探险家",
          info: "热爱深海探险，记录深海生物",
          avatar: require("@/assets/imgs/bgc2.jpg"),
          isFollowing: false,
        },
        {
          id: 3,
          name: "潜水教练",
          info: "PADI认证潜水教练，欢迎交流潜水技巧",
          avatar: require("@/assets/imgs/bgc2.jpg"),
          isFollowing: true,
        },
      ];

      this.followList = mockUsers.map((user) => ({
        ...user,
        loading: false,
      }));

      this.followsTotal = this.followList.length;
      this.author.followCount = this.followsTotal;
    },

    // 处理关注列表分页变化
    handleFollowsPageChange(page) {
      this.followsPage = page;
      this.loadFollowList();
    },

    // 加载粉丝列表
    async loadFansList() {
      this.fansLoading = true;
      try {
        console.log(
          "开始加载粉丝列表，作者ID:",
          this.authorId,
          "类型:",
          typeof this.authorId
        );

        // 调用API获取粉丝列表
        const res = await request.get("/follow/getFans", {
          params: {
            userId: Number(this.authorId),
            pageNum: this.fansPage,
            pageSize: this.fansPageSize,
            currentUserId: this.user.id, // 添加当前登录用户ID，用于后端判断关注状态
          },
        });

        console.log("获取粉丝列表API响应:", res);

        if (res.code === "200") {
          // 处理API响应数据
          if (res.data && Array.isArray(res.data.records)) {
            // 如果后端已返回isFollowing状态，则直接使用
            this.fansList = res.data.records.map((item) => ({
              ...item,
              isFollowing: item.isFollowing || false,
              loading: false,
            }));

            // 如果需要，可以在这里调用批量检查关注状态的API
            if (this.user.token && this.fansList.length > 0) {
              await this.checkUsersFollowStatus(this.fansList);

              // 检查列表中是否包含当前页面主人（author），如果有则同步全局isFollowing状态
              this.syncFollowingStatus();
            }

            this.fansTotal = res.data.total || 0;
            // 确保更新的是作者的数据
            this.author.fansCount = this.fansTotal;
            console.log(
              `更新作者(ID:${this.authorId})的粉丝数为: ${this.author.fansCount}`
            );
          } else if (res.data && Array.isArray(res.data)) {
            this.fansList = res.data.map((item) => ({
              ...item,
              isFollowing: item.isFollowing || false,
              loading: false,
            }));

            // 如果需要，可以在这里调用批量检查关注状态的API
            if (this.user.token && this.fansList.length > 0) {
              await this.checkUsersFollowStatus(this.fansList);

              // 检查列表中是否包含当前页面主人（author），如果有则同步全局isFollowing状态
              this.syncFollowingStatus();
            }

            this.fansTotal = res.data.length;
            // 确保更新的是作者的数据
            this.author.fansCount = this.fansTotal;
            console.log(
              `更新作者(ID:${this.authorId})的粉丝数为: ${this.author.fansCount}`
            );
          } else {
            // 没有数据
            this.fansList = [];
            this.fansTotal = 0;
            this.author.fansCount = 0;
          }
        } else {
          // 模拟粉丝列表数据
          console.warn("获取粉丝列表API不可用，使用模拟数据");
          this.generateMockFansList();
        }
      } catch (error) {
        console.error("获取粉丝列表失败", error);
        // 失败时使用模拟数据
        this.generateMockFansList();
      } finally {
        this.fansLoading = false;
      }
    },

    // 生成模拟粉丝列表数据
    generateMockFansList() {
      const mockUsers = [
        {
          id: 5,
          name: "珊瑚保护者",
          info: "致力于珊瑚礁保护和研究",
          avatar: require("@/assets/imgs/bgc2.jpg"),
          isFollowing: false,
        },
        {
          id: 6,
          name: "水下画家",
          info: "用画笔记录水下世界的色彩",
          avatar: require("@/assets/imgs/bgc2.jpg"),
          isFollowing: true,
        },
        {
          id: 7,
          name: "海洋生物学家",
          info: "专注海洋生态系统研究，发表论文20+",
          avatar: require("@/assets/imgs/bgc2.jpg"),
          isFollowing: false,
        },
        {
          id: 8,
          name: "自由潜水员",
          info: "热爱无氧潜水，分享潜水心得",
          avatar: require("@/assets/imgs/bgc2.jpg"),
          isFollowing: true,
        },
      ];

      this.fansList = mockUsers.map((user) => ({
        ...user,
        loading: false,
      }));

      this.fansTotal = this.fansList.length;
      this.author.fansCount = this.fansTotal;
    },

    // 处理粉丝列表分页变化
    handleFansPageChange(page) {
      this.fansPage = page;
      this.loadFansList();
    },

    // 切换对用户列表中用户的关注状态
    async toggleFollowUser(user) {
      // 检查是否登录
      if (!this.user.token) {
        this.$message.warning("请先登录后再关注");
        this.$router.push("/login");
        return;
      }

      // 防止重复操作
      if (user.loading) return;

      // 设置加载状态
      this.$set(user, "loading", true);

      try {
        const action = user.isFollowing ? "unfollow" : "follow";
        // 保存原始关注状态，以便在出错时恢复
        const originalFollowingState = user.isFollowing;

        // 确保ID是数字类型
        const followerId = parseInt(this.user.id);
        const followedId = parseInt(user.id);

        console.log("关注/取消关注用户参数:", {
          followerId: followerId,
          followedId: followedId,
          action: action,
          currentState: originalFollowingState,
          followerId类型: typeof followerId,
          followedId类型: typeof followedId,
        });

        // 先乐观地更新UI状态
        this.$set(user, "isFollowing", !originalFollowingState);

        // 如果操作的是当前页面的主人，同步更新全局isFollowing状态
        if (user.id === parseInt(this.$route.query.authorId)) {
          this.isFollowing = !originalFollowingState;
          console.log(
            `操作的是当前页面用户(ID:${user.id})，同步更新全局关注状态:`,
            this.isFollowing
          );
        }

        // 实际API调用
        const res = await request.post(`/follow/${action}`, {
          followerId: followerId, // 确保是数字类型
          followedId: followedId, // 确保是数字类型
        });

        if (res.code === "200") {
          // 成功，保持当前状态
          // 更新当前用户的关注数量
          if (user.isFollowing) {
            this.user.followCount = (this.user.followCount || 0) + 1;
          } else {
            this.user.followCount = Math.max(
              0,
              (this.user.followCount || 0) - 1
            );
          }

          // 更新本地存储的用户信息
          localStorage.setItem("xm-user", JSON.stringify(this.user));

          this.$message.success(user.isFollowing ? "关注成功" : "已取消关注");
        } else {
          // 失败，恢复原状态
          this.$set(user, "isFollowing", originalFollowingState);

          // 如果操作的是当前页面的主人，同步恢复全局isFollowing状态
          if (user.id === parseInt(this.$route.query.authorId)) {
            this.isFollowing = originalFollowingState;
            console.log(
              `操作的是当前页面用户(ID:${user.id})，恢复全局关注状态:`,
              this.isFollowing
            );
          }

          // 如果是已关注状态下点击关注按钮，给用户提示
          if (originalFollowingState && action === "follow") {
            this.$message.warning("您已经关注过该用户");
          } else if (!originalFollowingState && action === "unfollow") {
            this.$message.warning("您尚未关注该用户");
          } else {
            this.$message.error(res.msg || "操作失败，请稍后重试");
          }
        }
      } catch (error) {
        console.error("操作关注失败", error);
        // 出错时恢复原状态
        this.$set(user, "isFollowing", !user.isFollowing);

        // 如果操作的是当前页面的主人，同步恢复全局isFollowing状态
        if (user.id === parseInt(this.$route.query.authorId)) {
          this.isFollowing = !this.isFollowing;
          console.log(
            `操作失败，恢复当前页面用户(ID:${user.id})的全局关注状态:`,
            this.isFollowing
          );
        }

        this.$message.error("操作失败，请稍后重试");
      } finally {
        this.$set(user, "loading", false);
      }
    },

    // 查看用户资料
    viewUserProfile(userId) {
      this.$router.push({
        path: "/front/authorHome",
        query: { authorId: userId },
      });
    },

    // 加载当前激活标签的数据
    loadActiveTabData() {
      console.log("加载当前激活标签数据:", this.activeName);

      if (this.activeName === "blogs") {
        console.log("初始加载作者博客列表，作者ID:", this.authorId);
        this.$nextTick(() => {
          if (this.$refs.blogList) {
            this.$refs.blogList.reset();
            this.$refs.blogList.load();
          }
        });
      } else if (this.activeName === "activities") {
        console.log("初始加载作者活动列表，作者ID:", this.authorId);
        this.$nextTick(() => {
          if (this.$refs.activityList) {
            this.$refs.activityList.reset();
            this.$refs.activityList.load(1);
          }
        });
      } else if (this.activeName === "follows") {
        this.loadFollowList();
      } else if (this.activeName === "fans") {
        this.loadFansList();
      } else if (this.activeName === "likes" && this.isOwnProfile) {
        if (this.likesCurrent === "博客" && this.$refs.blogLikesList) {
          this.$refs.blogLikesList.reset();
          this.$refs.blogLikesList.load();
        } else if (
          this.likesCurrent === "活动" &&
          this.$refs.activityLikesList
        ) {
          this.$refs.activityLikesList.reset();
          this.$refs.activityLikesList.load(1);
        }
      } else if (this.activeName === "collections" && this.isOwnProfile) {
        if (this.collectCurrent === "博客" && this.$refs.blogCollectionsList) {
          this.$refs.blogCollectionsList.reset();
          this.$refs.blogCollectionsList.load();
        } else if (
          this.collectCurrent === "活动" &&
          this.$refs.activityCollectionsList
        ) {
          this.$refs.activityCollectionsList.reset();
          this.$refs.activityCollectionsList.load(1);
        }
      } else if (this.activeName === "comments" && this.isOwnProfile) {
        if (this.commentCurrent === "博客" && this.$refs.blogCommentsList) {
          this.$refs.blogCommentsList.reset();
          this.$refs.blogCommentsList.load();
        } else if (
          this.commentCurrent === "活动" &&
          this.$refs.activityCommentsList
        ) {
          this.$refs.activityCommentsList.reset();
          this.$refs.activityCommentsList.load(1);
        }
      }
    },

    // 处理博客列表数据加载完成事件
    handleBlogDataLoaded(data) {
      console.log(
        `博客列表加载完成，作者ID: ${this.authorId}，类型: ${typeof this
          .authorId}，数字类型: ${Number(this.authorId)}，共 ${
          data.total
        } 篇博客`
      );
      console.log("传递给博客列表的参数:", { userId: Number(this.authorId) });
      console.log(
        "博客数据示例:",
        data.list && data.list.length > 0 ? data.list[0] : "无博客"
      );
      // 更新博客计数
      if (data.total !== undefined && data.total >= 0) {
        this.author.blogCount = data.total;
      }
    },

    // 处理博客列表数据加载完成事件
    handleBlogLikesDataLoaded(data) {
      console.log(
        `点赞博客列表加载完成，作者ID: ${this.authorId}，共 ${data.total} 篇博客`
      );
      console.log(
        "点赞博客数据示例:",
        data.list && data.list.length > 0 ? data.list[0] : "无博客"
      );
      // 更新点赞计数
      if (data.total !== undefined && data.total >= 0) {
        this.author.likesCount = data.total;
      }
    },

    // 处理博客列表数据加载完成事件
    handleBlogCollectionsDataLoaded(data) {
      console.log(
        `收藏博客列表加载完成，作者ID: ${this.authorId}，共 ${data.total} 篇博客`
      );
      console.log(
        "收藏博客数据示例:",
        data.list && data.list.length > 0 ? data.list[0] : "无博客"
      );
      // 更新收藏计数
      if (data.total !== undefined && data.total >= 0) {
        this.author.collectCount = data.total;
      }
    },

    // 处理博客列表数据加载完成事件
    handleBlogCommentsDataLoaded(data) {
      console.log(
        `评论博客列表加载完成，作者ID: ${this.authorId}，共 ${data.total} 篇博客`
      );
      console.log(
        "评论博客数据示例:",
        data.list && data.list.length > 0 ? data.list[0] : "无博客"
      );
      // 注意这里不更新评论计数，因为author对象中没有commentCount字段
    },

    // 添加活动列表数据加载完成事件处理
    handleActivityDataLoaded(data) {
      console.log(
        `活动列表加载完成，作者ID: ${this.authorId}，类型: ${typeof this
          .authorId}，数字类型: ${Number(this.authorId)}，共 ${
          data.total || 0
        } 个活动`
      );
      console.log("传递给活动列表的参数:", { userId: Number(this.authorId) });
      // 这里可以根据需要更新作者的活动相关计数
    },

    // 添加标签计数方法
    getTabCount(tabName) {
      switch (tabName) {
        case "blogs":
          return this.author.blogCount || 0;
        case "activities":
          return 0; // 可以根据实际情况返回活动数量
        case "follows":
          return this.author.followCount || 0;
        case "fans":
          return this.author.fansCount || 0;
        default:
          return 0;
      }
    },

    // 处理角色切换
    handleRoleChange(role) {
      this.$request
        .put("/user/updateBrowseRole", {
          userId: JSON.parse(localStorage.getItem("xm-user") || "{}").id,
          browseRole: role,
        })
        .then((res) => {
          if (res.code === "200") {
            // 更新本地存储中的用户信息
            const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
            user.browseRole = role;
            localStorage.setItem("xm-user", JSON.stringify(user));

            this.$message.success("切换成功");
            // 刷新博客列表
            if (this.$refs.blogList) {
              this.$refs.blogList.load();
            }
          } else {
            this.$message.error(res.msg || "切换失败");
          }
        });
    },

    loadBlogs() {
      this.loading = true;
      const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
      this.userRole = user.browseRole || "";

      // 根据角色筛选博客
      request
        .get("/blog/selectByUserId", {
          params: {
            userId: this.authorId,
            role: this.userRole, // 添加角色参数
          },
        })
        .then((res) => {
          if (res.code === "200") {
            this.blogList = res.data || [];
          }
        })
        .finally(() => {
          this.loading = false;
        });
    },

    // 批量检查用户的关注状态
    async checkUsersFollowStatus(userList) {
      if (!this.user.token || !userList || userList.length === 0) {
        return;
      }

      try {
        // 直接使用单个检查API
        console.log(`开始检查${userList.length}位用户的关注状态...`);
        await this.checkIndividualUsersFollowStatus(userList);
      } catch (error) {
        console.error("检查用户关注状态失败", error);
      }
    },

    // 单个检查每个用户的关注状态
    async checkIndividualUsersFollowStatus(userList) {
      if (!this.user.token || !userList || userList.length === 0) {
        return;
      }

      try {
        for (const user of userList) {
          // 跳过当前用户自己
          if (user.id === this.user.id) {
            this.$set(user, "isFollowing", false);
            continue;
          }

          // 为每个用户调用检查关注状态API
          const res = await request.get("/follow/checkStatus", {
            params: {
              followerId: Number(this.user.id),
              followedId: Number(user.id),
            },
          });

          if (res.code === "200") {
            this.$set(user, "isFollowing", res.data);
            console.log(
              `用户(ID:${user.id}, 名称:${user.name})的关注状态:`,
              res.data
            );
          }
        }

        // 同步完成后，检查是否需要更新全局状态
        this.syncFollowingStatus();
      } catch (error) {
        console.error("检查个别用户关注状态失败", error);
      }
    },

    // 同步头部和列表中的关注状态
    syncFollowingStatus() {
      // 查找关注列表中有没有当前所在主页的用户
      const currentPageUser = this.followList.find(
        (user) => user.id === parseInt(this.$route.query.authorId)
      );

      if (currentPageUser) {
        // 如果找到，同步isFollowing状态到全局
        this.isFollowing = currentPageUser.isFollowing;
        console.log(
          `在关注列表中找到当前页面用户(ID:${currentPageUser.id})，同步关注状态:`,
          this.isFollowing
        );
      }

      // 查找粉丝列表中有没有当前所在主页的用户
      const currentPageUserInFans = this.fansList.find(
        (user) => user.id === parseInt(this.$route.query.authorId)
      );

      if (currentPageUserInFans) {
        // 如果找到，同步isFollowing状态到全局
        this.isFollowing = currentPageUserInFans.isFollowing;
        console.log(
          `在粉丝列表中找到当前页面用户(ID:${currentPageUserInFans.id})，同步关注状态:`,
          this.isFollowing
        );
      }
    },

    // 更新列表中的用户关注状态
    updateListUserFollowStatus(userId, isFollowingNew) {
      userId = parseInt(userId);

      // 在关注列表中查找该用户
      const userInFollowList = this.followList.find(
        (user) => parseInt(user.id) === userId
      );
      if (userInFollowList) {
        this.$set(userInFollowList, "isFollowing", isFollowingNew);
        console.log(
          `更新关注列表中用户(ID:${userId})的关注状态为:`,
          isFollowingNew
        );
      }

      // 在粉丝列表中查找该用户
      const userInFansList = this.fansList.find(
        (user) => parseInt(user.id) === userId
      );
      if (userInFansList) {
        this.$set(userInFansList, "isFollowing", isFollowingNew);
        console.log(
          `更新粉丝列表中用户(ID:${userId})的关注状态为:`,
          isFollowingNew
        );
      }
    },
  },

  watch: {
    // 当路由参数变化时重新加载数据
    "$route.query.authorId": function (newVal, oldVal) {
      if (newVal !== oldVal) {
        this.authorId = newVal;
        // 转换为数字类型
        if (typeof this.authorId === "string") {
          this.authorId = parseInt(this.authorId);
        }
        this.loadAuthorInfo();
      }
    },

    activeName(newVal, oldVal) {
      console.log("watch activeName变化:", oldVal, "->", newVal);

      // 仅当不是通过handleClick方法改变时才加载数据（避免重复加载）
      // 这种情况通常是通过路由或其他方式直接改变了activeName
      if (newVal !== oldVal && !this._activeNameChangedByClick) {
        console.log("watch触发loadActiveTabData");
        this.$nextTick(() => {
          this.loadActiveTabData();
        });
      }

      // 重置标志
      this._activeNameChangedByClick = false;
    },

    // 监听点赞类型变化
    likesCurrent: function (newVal, oldVal) {
      if (newVal !== oldVal) {
        console.log("点赞类型切换到:", newVal);
        this.$nextTick(() => {
          if (newVal === "博客") {
            if (this.$refs.blogLikesList) {
              this.$refs.blogLikesList.reset();
              this.$refs.blogLikesList.load();
            }
          } else if (newVal === "活动") {
            if (this.$refs.activityLikesList) {
              this.$refs.activityLikesList.reset();
              this.$refs.activityLikesList.load(1);
            }
          }
        });
      }
    },

    // 监听收藏类型变化
    collectCurrent: function (newVal, oldVal) {
      if (newVal !== oldVal) {
        console.log("收藏类型切换到:", newVal);
        this.$nextTick(() => {
          if (newVal === "博客") {
            if (this.$refs.blogCollectionsList) {
              this.$refs.blogCollectionsList.reset();
              this.$refs.blogCollectionsList.load();
            }
          } else if (newVal === "活动") {
            if (this.$refs.activityCollectionsList) {
              this.$refs.activityCollectionsList.reset();
              this.$refs.activityCollectionsList.load(1);
            }
          }
        });
      }
    },

    // 监听评论类型变化
    commentCurrent: function (newVal, oldVal) {
      if (newVal !== oldVal) {
        console.log("评论类型切换到:", newVal);
        this.$nextTick(() => {
          if (newVal === "博客") {
            if (this.$refs.blogCommentsList) {
              this.$refs.blogCommentsList.reset();
              this.$refs.blogCommentsList.load();
            }
          } else if (newVal === "活动") {
            if (this.$refs.activityCommentsList) {
              this.$refs.activityCommentsList.reset();
              this.$refs.activityCommentsList.load(1);
            }
          }
        });
      }
    },
  },
};
</script>

<style lang="less" scoped>
// 全局变量，统一色彩方案
@primary-color: #316db1; // 主色调
@primary-light: #5aa6f0; // 亮主色
@primary-dark: #2970c3; // 暗主色
@accent-color: #ff6a54; // 强调色
@bg-color: #f7f9fc; // 背景色
@card-bg: #fff; // 卡片背景
@border-color: #e8eef7; // 边框颜色
@text-primary: #333; // 主要文字颜色
@text-secondary: #5a6a85; // 次要文字颜色
@text-hint: #90a0b7; // 提示文字颜色
@hover-bg: rgba(60, 140, 231, 0.05); // 悬停背景色

.author-page {
  min-height: 100vh;
  background-color: var(--bg-color);
  color: var(--text-color-primary);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "PingFang SC", "Helvetica Neue", Arial, sans-serif;
}

.profile-container {
  position: relative;
}

/* 容器宽度控制 */
.csdn-container-width {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  position: relative;
  z-index: 2;
}

/* 顶部背景 */
.csdn-header-background {
  position: relative;
  height: 200px;
  overflow: hidden;
  background: linear-gradient(
    135deg,
    var(--bg-gradient-light) 0%,
    var(--bg-gradient-dark) 100%
  );
}

/* 波浪效果 */
.wave-container {
  position: absolute;
  width: 100%;
  height: 100%;
  bottom: 0;
  left: 0;
  z-index: 1;
}

.wave {
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="white" fill-opacity="0.1" d="M0,160L60,138.7C120,117,240,75,360,80C480,85,600,139,720,165.3C840,192,960,192,1080,170.7C1200,149,1320,107,1380,85.3L1440,64L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z"></path></svg>');
  position: absolute;
  width: 100%;
  height: 100%;
  animation: wave-animation 20s linear infinite;
  background-size: 100% 100px;
  background-repeat: repeat-x;
  background-position: bottom;
  bottom: 0;
  opacity: 0.5;
}

.wave1 {
  animation: wave-animation 20s linear infinite;
  z-index: 3;
  opacity: 0.7;
  animation-delay: 0s;
  bottom: 0;
}

.wave2 {
  animation: wave-animation-reverse 12s linear infinite;
  z-index: 2;
  opacity: 0.5;
  animation-delay: -5s;
  bottom: 10px;
}

.wave3 {
  animation: wave-animation 30s linear infinite;
  z-index: 1;
  opacity: 0.3;
  animation-delay: -2s;
  bottom: 15px;
}

@keyframes wave-animation {
  0% {
    background-position-x: 0;
  }
  100% {
    background-position-x: 1000px;
  }
}

@keyframes wave-animation-reverse {
  0% {
    background-position-x: 1000px;
  }
  100% {
    background-position-x: 0;
  }
}

/* 气泡效果 */
.floating-bubbles {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 2;
  overflow: hidden;
}

.bubble {
  position: absolute;
  bottom: -100px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(3px);
  -webkit-backdrop-filter: blur(3px);
  animation: bubble-animation 15s infinite ease-in;
  box-shadow: inset 0 0 10px rgba(255, 255, 255, 0.2),
    0 0 10px rgba(255, 255, 255, 0.1);
}

.bubble::before {
  content: "";
  position: absolute;
  top: 10px;
  left: 10px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
}

.bubble1 {
  left: 10%;
  width: 30px;
  height: 30px;
  animation-duration: 20s;
  animation-delay: 0s;
}

.bubble2 {
  left: 20%;
  width: 25px;
  height: 25px;
  animation-duration: 15s;
  animation-delay: 2s;
}

.bubble3 {
  left: 35%;
  width: 40px;
  height: 40px;
  animation-duration: 18s;
  animation-delay: 5s;
}

.bubble4 {
  left: 50%;
  width: 20px;
  height: 20px;
  animation-duration: 12s;
  animation-delay: 1s;
}

.bubble5 {
  left: 65%;
  width: 35px;
  height: 35px;
  animation-duration: 19s;
  animation-delay: 3s;
}

.bubble6 {
  left: 80%;
  width: 18px;
  height: 18px;
  animation-duration: 14s;
  animation-delay: 4s;
}

.bubble7 {
  left: 90%;
  width: 28px;
  height: 28px;
  animation-duration: 17s;
  animation-delay: 6s;
}

.bubble8 {
  left: 40%;
  width: 22px;
  height: 22px;
  animation-duration: 16s;
  animation-delay: 7s;
}

@keyframes bubble-animation {
  0% {
    transform: translateY(0) scale(1);
    opacity: 0;
  }
  20% {
    transform: translateY(-20%) scale(1.1);
    opacity: 0.8;
  }
  40% {
    transform: translateY(-40%) scale(1);
    opacity: 0.7;
  }
  60% {
    transform: translateY(-60%) scale(1.2);
    opacity: 0.6;
  }
  80% {
    transform: translateY(-80%) scale(0.9);
    opacity: 0.4;
  }
  100% {
    transform: translateY(-100%) scale(1);
    opacity: 0;
  }
}

/* 鱼儿效果 */
.swimming-fish {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 2;
  background: linear-gradient(to bottom, #1d3a4c, #2a5d68, #4ecdc4);
}

.fish {
  position: absolute;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 20"><path fill="white" opacity="0.6" d="M20,10 C20,6 17,0 8,0 C8,0 3,1 3,10 C3,19 8,20 8,20 C17,20 20,14 20,10 Z M25,8 L25,12 L30,15 L25,12 L25,8 Z"></path><circle fill="black" cx="6" cy="10" r="1"/></svg>');
  background-repeat: no-repeat;
  width: 30px;
  height: 20px;
  opacity: 0.6;
  animation: fish-animation 30s linear infinite;
}

.fish1 {
  top: 20%;
  animation-duration: 25s;
  transform: scale(1.2);
}

.fish2 {
  top: 45%;
  animation-duration: 35s;
  animation-delay: 5s;
  transform: scale(0.8);
}

.fish3 {
  top: 70%;
  animation-duration: 30s;
  animation-delay: 12s;
  transform: scale(1);
}

@keyframes fish-animation {
  0% {
    left: -5%;
  }
  100% {
    left: 100%;
  }
}

/* 叠加层效果 */
.header-content-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--bg-color-alpha);
  backdrop-filter: blur(5px);
  z-index: 1;
}

/* 内容区域 */
.header-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* 作者简介 */
.author-brief {
  color: var(--text-color-primary);

  .author-brief-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 10px;
    color: rgba(223, 215, 199, 0.849);
  }
}

/* 顶部简略统计数据 */
.profile-stats-brief {
  display: flex;
  gap: 20px;
}

.stat-brief-item:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.25);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.stat-number {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 5px;
  font-family: "DIN Alternate", "Arial", sans-serif;
}

.stat-label {
  font-size: 15px;
  opacity: 0.95;
  font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", sans-serif;
  font-weight: 300;
}

/* 个人信息卡片 */
.csdn-profile-card {
  background-color: var(--bg-color-secondary);
  border-radius: 12px;
  box-shadow: var(--card-shadow);
  margin-top: -50px;
  position: relative;
  border: 1px solid var(--border-color);
}

.csdn-profile-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: linear-gradient(to right, #0a4d68, #05bfdb);
}

/* 布局 */
.csdn-profile-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 30px;
}

/* 左侧区域 */
.csdn-profile-left {
  padding: 30px;
  border-right: 1px solid var(--border-color);
}

/* 右侧区域 */
.csdn-profile-right {
  padding: 30px;
}

/* 头像 */
.csdn-avatar-wrapper {
  margin-bottom: 25px;
  text-align: center;
}

.csdn-avatar-container {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  margin: 0 auto 20px;
  border: 3px solid var(--border-color);
  position: relative;

  .avatar-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .avatar-hover-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: var(--bg-color-alpha);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s ease;
    color: var(--text-color-primary);

    &:hover {
      opacity: 1;
    }

    .upload-icon {
      font-size: 24px;
      margin-bottom: 5px;
    }
  }
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;

  &:hover {
    transform: scale(1.05);
  }
}

.avatar-hover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(60, 140, 231, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0;
  transition: opacity 0.3s ease;
  cursor: pointer;
  border-radius: 50%;
}

.avatar-uploader:hover .avatar-hover-overlay {
  opacity: 1;
}

.upload-icon {
  font-size: 24px;
  margin-bottom: 6px;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: #d1d5db;
  background-color: #f8fafc;
}

/* 统计数据 */
.csdn-stats-detail {
  margin-top: 30px;
}

.stat-card {
  background-color: var(--bg-color-tertiary);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid var(--border-color);
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;

  .stat-grid-item {
    text-align: center;

    .stat-value {
      font-size: 20px;
      font-weight: bold;
      color: var(--text-color-primary);
      margin-bottom: 5px;
    }

    .stat-label {
      font-size: 12px;
      color: var(--text-color-secondary);
    }
  }
}

/* 联系信息卡片 */
.contact-card {
  background-color: var(--bg-color-tertiary);
  border-radius: 8px;
  padding: 20px;
  border: 1px solid var(--border-color);

  .card-title {
    font-size: 16px;
    font-weight: bold;
    color: var(--text-color-primary);
    margin-bottom: 15px;
  }

  .contact-item {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
    color: var(--text-color-regular);

    i {
      color: var(--primary-color);
    }
  }
}

/* 用户信息 */
.csdn-user-info {
  margin-bottom: 30px;
}

.user-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;

  .user-name {
    font-size: 24px;
    font-weight: bold;
    color: var(--text-color-primary);
  }
}

.user-badges {
  display: flex;
  gap: 10px;
  transform: translateX(-530px);

  .badge-item {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    background-color: var(--bg-color-tertiary);
    color: var(--primary-color);
    border: 1px solid var(--border-color);
  }
}

.user-bio {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-color-regular);
  margin-bottom: 20px;
  padding-left: 15px;
  border-left: 3px solid var(--primary-color);
}

/* 操作按钮 */
.csdn-action-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;

  .primary-actions {
    display: flex;
    gap: 10px;
  }

  .secondary-actions {
    display: flex;
    gap: 10px;
  }
}

/* 标签页 */
.csdn-tabs {
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 20px;
  display: flex;
  flex-wrap: nowrap; /* 不允许换行 */
  overflow-x: auto; /* 允许横向滚动 */
  white-space: nowrap; /* 文本不换行 */
  scrollbar-width: none; /* 隐藏滚动条 - Firefox */
  -ms-overflow-style: none; /* 隐藏滚动条 - IE/Edge */
  
  &::-webkit-scrollbar {
    display: none; /* 隐藏滚动条 - Chrome/Safari/Opera */
  }

  .scroll-container {
    display: flex;
    flex-wrap: nowrap; /* 不允许换行 */
    min-width: 100%;
  }

  .csdn-tab-item {
    padding: 15px 15px;
    font-size: 15px;
    color: var(--text-color-regular);
    cursor: pointer;
    position: relative;
    transition: all 0.2s ease;
    white-space: nowrap; /* 文本不换行 */
    flex-shrink: 0; /* 不缩小 */

    &:hover {
      color: var(--primary-color);
    }

    &.active {
      color: var(--primary-color);
      font-weight: 500;

      &::after {
        content: "";
        position: absolute;
        bottom: -1px;
        left: 0;
        right: 0;
        height: 2px;
        background-color: var(--primary-color);
      }
    }

    /* 添加计数徽章样式 */
    .count-badge {
      font-size: 12px;
      background-color: var(--primary-color-alpha);
      color: var(--primary-color);
      padding: 2px 6px;
      border-radius: 10px;
      margin-left: 5px;
      font-weight: normal;
    }
  }
}

/* 添加响应式调整 */
@media (max-width: 1200px) {
  .csdn-tabs .csdn-tab-item {
    padding: 15px 12px;  /* 减少内边距 */
    font-size: 14px;     /* 减小字体 */
  }
}

@media (max-width: 992px) {
  .csdn-tabs .csdn-tab-item {
    padding: 15px 10px;
    font-size: 13px;
  }
}

@media (max-width: 768px) {
  .csdn-tabs .csdn-tab-item {
    padding: 15px 8px;
    font-size: 12px;
    
    .count-badge {
      padding: 1px 4px;
      font-size: 10px;
    }
  }
}

@media (max-width: 576px) {
  .csdn-tabs .csdn-tab-item {
    padding: 15px 6px;
    font-size: 11px;
  }
}

/* 内容区过滤器 */
.csdn-content-filter {
  margin-bottom: 25px;
  padding: 10px 0;

  /deep/ .el-radio-button__inner {
    border-color: @border-color;
    background: white;
    font-size: 13px;
    color: @text-secondary;
    transition: all 0.25s ease;

    &:hover {
      color: @primary-color;
    }
  }

  /deep/ .el-radio-button__orig-radio:checked + .el-radio-button__inner {
    background-color: @primary-color;
    border-color: @primary-color;
    box-shadow: -1px 0 0 0 @primary-color;
    color: white;
  }
}

/* 徽章 */
.csdn-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  background-color: rgba(60, 140, 231, 0.1);
  color: @primary-color;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  z-index: 2;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(60, 140, 231, 0.15);
  animation: fadeIn 0.5s ease;

  i {
    font-size: 14px;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 弹窗 */
/deep/ .csdn-dialog {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);

  .el-dialog__header {
    padding: 16px 20px;
    border-bottom: 1px solid @border-color;
    background-color: #f8fafc;
  }

  .el-dialog__title {
    font-weight: 600;
    font-size: 16px;
    color: @text-primary;
  }

  .el-dialog__body {
    padding: 25px;
  }

  .el-dialog__footer {
    border-top: 1px solid @border-color;
    padding: 16px 20px;
    background-color: #f8fafc;
  }

  .el-form-item__label {
    color: @text-secondary;
    font-weight: 500;
  }

  .el-input__inner {
    border-color: @border-color;

    &:focus {
      border-color: @primary-color;
    }
  }

  .el-textarea__inner {
    border-color: @border-color;

    &:focus {
      border-color: @primary-color;
    }
  }

  .el-button--primary {
    background-color: @primary-color;
    border-color: @primary-color;

    &:hover {
      background-color: @primary-light;
      border-color: @primary-light;
    }
  }
}

/* 内容区样式 */
.csdn-content-area {
  padding-top: 10px;
  min-height: 400px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .csdn-profile-layout {
    grid-template-columns: 1fr;
  }

  .csdn-profile-left {
    border-right: none;
    border-bottom: 1px solid var(--border-color);
  }

  .user-header {
    flex-direction: column;
    align-items: flex-start;

    .user-name {
      margin-bottom: 10px;
    }
  }

  .csdn-action-bar {
    flex-direction: column;
    gap: 10px;

    .primary-actions,
    .secondary-actions {
      width: 100%;
      justify-content: center;
    }
  }
}

@media (max-width: 576px) {
  .csdn-header-background {
    height: 150px;
  }

  .profile-stats-brief {
    justify-content: center;
    width: 100%;
  }

  .csdn-profile-card {
    margin-top: -30px;
  }

  .user-name {
    font-size: 22px;
    text-align: center;
    width: 100%;
  }

  .user-badges {
    justify-content: center;
    width: 100%;
  }

  .user-bio {
    text-align: center;
    padding-left: 0;
    border-left: none;
    padding-bottom: 10px;
    border-bottom: 1px solid @border-color;
  }
}

/* 关注列表样式 */
.follows-container {
  margin-top: 20px;
}

.empty-follows,
.follows-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px 0;
  color: @text-hint;

  i {
    font-size: 40px;
    margin-bottom: 15px;
  }

  p {
    font-size: 14px;
  }
}

.follows-list {
  .follow-item {
    display: flex;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid @border-color;
    transition: all 0.2s ease;

    &:hover {
      background-color: @hover-bg;
    }

    .follow-user-avatar {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      overflow: hidden;
      margin-right: 15px;
      border: 2px solid white;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
    }

    .follow-user-info {
      flex: 1;

      .follow-user-name {
        font-size: 16px;
        font-weight: 500;
        //color: @text-primary;
        margin-bottom: 5px;
        cursor: pointer;

        &:hover {
          color: @primary-color;
        }
      }

      .follow-user-bio {
        font-size: 13px;
        color: @text-secondary;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 400px;
      }
    }

    .follow-actions {
      margin-left: 20px;
    }
  }
}

.follows-pagination {
  margin-top: 20px;
  text-align: center;
}

.csdn-tab-item {
  padding: 12px 20px;
  font-size: 15px;
  color: #666;
  cursor: pointer;
  position: relative;
  transition: all 0.3s;
  white-space: nowrap;
}

.csdn-tab-item:hover {
  color: #05bfdb;
}

.csdn-tab-item.active {
  color: #05bfdb;
  font-weight: 500;
}

.csdn-tab-item.active::after {
  content: "";
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 2px;
  background: #05bfdb;
}

.role-switcher {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  text-align: center;

  .el-radio-button__inner {
    padding: 12px 20px;
    display: inline-flex;
    align-items: center;
    gap: 5px;

    i {
      font-size: 16px;
    }
  }
}

.already-following {
  background-color: #f5f5f5 !important;
  color: #606266 !important;
  border-color: #dcdfe6 !important;

  &:hover {
    background-color: #f0f0f0 !important;
    color: #409eff !important;
  }
}

.follow-user-name {
  color: #0a4d68;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.3s;

  &:hover {
    color: #05bfdb;
    text-decoration: underline;
  }
}

.self-tag {
  color: #909399;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 4px;
  background: #f4f4f5;
  padding: 4px 8px;
  border-radius: 4px;

  i {
    font-size: 14px;
  }
}

.role-badge {
  position: absolute;
  top: 20px;
  right: 20px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  color: white;

  &.RESEARCHER {
    background: linear-gradient(135deg, #0a4d68, #088395);
  }

  &.HOBBYIST {
    background: linear-gradient(135deg, #28a745, #20c997);
  }

  &:not(.RESEARCHER):not(.HOBBYIST) {
    background: linear-gradient(135deg, #6c757d, #495057);
  }
}
</style>
