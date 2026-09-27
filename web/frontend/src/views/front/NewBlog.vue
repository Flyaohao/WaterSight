<template>
  <div class="blog-editor-container">
    <!-- 左侧目录区域，可收起 -->
    <div class="toc-sidebar" :class="{ 'collapsed': tocCollapsed }">
      <div class="toc-toggle" @click="tocCollapsed = !tocCollapsed">
        <i :class="tocCollapsed ? 'el-icon-arrow-right' : 'el-icon-arrow-left'"></i>
      </div>
      <div v-show="!tocCollapsed" class="toc-content">
        <h3 class="toc-title">文章目录</h3>
        <div class="toc-list">
          <div v-if="tocItems.length === 0" class="toc-empty">
            尚未检测到标题
          </div>
          <div 
            v-for="(item, index) in tocItems" 
            :key="index"
            class="toc-item"
            :class="[`toc-level-${item.level}`]"
            @click="scrollToHeading(item.id)"
          >
            <span class="toc-text">{{ item.text }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 主编辑区域 -->
    <div class="blog-editor-content glass-effect" :class="{ 'wide-mode': tocCollapsed }">
      <div class="editor-header">
        <h2 class="editor-title">{{ blogId ? '编辑博客' : '发表新博客' }}</h2>
        <div class="user-role-info">
          <span>当前身份: </span>
          <el-tag size="small" :type="roleTagType" v-if="!canSwitchRole">
            {{ roleDisplayName }}
          </el-tag>
          <el-dropdown v-else @command="handleRoleChange" trigger="click">
            <el-tag size="small" :type="roleTagType" class="role-dropdown-trigger">
              {{ roleDisplayName }} <i class="el-icon-arrow-down el-icon--right"></i>
            </el-tag>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item 
                v-for="role in availableRoles" 
                :key="role.value" 
                :command="role.value"
                :disabled="role.value === userRole"
              >
                <i :class="role.icon"></i> {{ role.label }}
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
        <el-button
          type="primary"
          size="medium"
          @click="save"
          class="publish-btn"
          >{{ blogId ? '保存修改' : '发布文章' }}</el-button
        >
      </div>
      <el-form
        :model="form"
        label-width="80px"
        :rules="rules"
        ref="formRef"
        class="blog-form"
      >
        <div class="form-layout">
          <div class="form-left">
            <el-form-item label="标题" prop="title" class="title-input">
              <el-input
                v-model="form.title"
                placeholder="请输入文章标题（最多100个字）"
                maxlength="100"
              ></el-input>
            </el-form-item>
            <el-form-item label="简介" prop="descr" class="descr-input">
              <el-input
                type="textarea"
                v-model="form.descr"
                placeholder="请输入文章简介，让读者快速了解文章内容（至少5个字）"
                :rows="3"
                show-word-limit
                maxlength="200"
              ></el-input>
            </el-form-item>
            <div class="form-row">
              <el-form-item
                label="分类"
                prop="categoryId"
                class="category-select"
              >
                <el-select
                  v-model="form.categoryId"
                  placeholder="请选择文章分类"
                  filterable
                >
                  <template v-if="userRole === 'ALL'">
                    <el-option-group
                      label="所有用户可选分类"
                    >
                      <el-option
                        v-for="item in categoryList.filter(c => c.role === 'HOBBYIST')"
                        :key="item.id"
                        :value="item.id"
                        :label="item.name"
                      ></el-option>
                    </el-option-group>
                  </template>
                  <template v-else>
                    <el-option
                      v-for="item in categoryList"
                      :key="item.id"
                      :value="item.id"
                      :label="item.name"
                    ></el-option>
                  </template>
                </el-select>
              </el-form-item>
              <el-form-item label="标签" prop="tags" class="tags-select">
                <el-select
                  v-model="tagsArr"
                  multiple
                  placeholder="请选择标签，最多5个"
                  :multiple-limit="5"
                  filterable
                  allow-create
                  default-first-option
                >
                  <el-option value="水下摄影"></el-option>
                  <el-option value="水产养殖"></el-option>
                  <el-option value="水下图像"></el-option>
                  <el-option value="目标识别"></el-option>
                  <el-option value="科学研究"></el-option>
                  <el-option value="教育资源"></el-option>
                  <el-option value="法规政策"></el-option>
                  <el-option value="技术交流"></el-option>
                  <el-option value="行业动态"></el-option>
                </el-select>
              </el-form-item>
            </div>
          </div>
          <div class="form-right">
            <el-form-item v-if="userRole !== 'RESEARCHER'" label="封面" prop="cover" class="cover-upload">
              <el-upload
                :action="$baseUrl + '/files/upload'"
                :headers="{ token: user.token }"
                list-type="picture-card"
                :on-success="handleCoverSuccess"
                :limit="1"
                class="cover-uploader"
              >
                <div class="upload-content">
                  <i class="el-icon-camera-solid"></i>
                  <div class="upload-text">💭 点击或拖拽上传封面图</div>
                </div>
                <div slot="tip" class="el-upload__tip">
                  建议尺寸：900x383px，支持 jpg、png 格式，最大不超过 2MB
                </div>
              </el-upload>
              <div v-if="form.cover" class="upload-success-animation">
                <img
                  src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath d='M50,10 C60,30 80,40 90,50 C80,60 60,70 50,90 C40,70 20,60 10,50 C20,40 40,30 50,10z' fill='%233498db'/%3E%3C/svg%3E"
                  class="dolphin-icon"
                  alt="上传成功"
                />
              </div>
            </el-form-item>
            <div v-if="userRole === 'RESEARCHER'" class="researcher-note">
              <i class="el-icon-info-circle"></i>
              <p>科研人员发布的博客使用系统默认封面，专注于内容本身</p>
            </div>
          </div>
        </div>
        <el-form-item label="内容" prop="content" class="content-editor">
          <div id="editor" class="wang-editor"></div>
        </el-form-item>
      </el-form>
    </div>

    <!-- 右侧悬浮工具栏 -->
    <div class="floating-toolbar" :class="{ 'collapsed': isToolbarCollapsed }">
      <div class="toolbar-toggle" @click="toggleFloatingToolbar">
        <i :class="isToolbarCollapsed ? 'el-icon-d-arrow-right' : 'el-icon-d-arrow-left'"></i>
      </div>
      <div class="floating-toolbar-inner">
        <div class="toolbar-title">编辑工具</div>
        <div class="toolbar-buttons">
          <div class="toolbar-button" @click="applyFormat('bold')" title="加粗 (Ctrl+B)">
            <i class="el-icon-bold">B</i>
          </div>
          <div class="toolbar-button" @click="applyFormat('italic')" title="斜体 (Ctrl+I)">
            <i class="el-icon-italic" style="font-style: italic;">I</i>
          </div>
          <div class="toolbar-button" @click="applyFormat('underline')" title="下划线 (Ctrl+U)">
            <i class="el-icon-underline">U</i>
          </div>
          <div class="toolbar-divider"></div>
          <div class="toolbar-button" @click="toggleHeading('h1')" title="一级标题 (Alt+1)">
            <span class="heading-icon">H1</span>
          </div>
          <div class="toolbar-button" @click="toggleHeading('h2')" title="二级标题 (Alt+2)">
            <span class="heading-icon">H2</span>
          </div>
          <div class="toolbar-button" @click="toggleHeading('h3')" title="三级标题 (Alt+3)">
            <span class="heading-icon">H3</span>
          </div>
          <div class="toolbar-button" @click="toggleHeading('h4')" title="四级标题 (Alt+4)">
            <span class="heading-icon">H4</span>
          </div>
          <div class="toolbar-divider"></div>
          <div class="toolbar-button" @click="applyFormat('fontSize')" title="字号">
            <i class="el-icon-sort"></i>
          </div>
          <div class="toolbar-button" @click="applyFormat('foreColor')" title="文字颜色">
            <i class="el-icon-price-tag"></i>
          </div>
          <div class="toolbar-divider"></div>
          <div class="toolbar-button" @click="applyFormat('link')" title="链接 (Ctrl+L)">
            <i class="el-icon-link"></i>
          </div>
          <div class="toolbar-button" @click="applyFormat('image')" title="插入图片">
            <i class="el-icon-picture"></i>
          </div>
          <div class="toolbar-button" @click="applyFormat('quote')" title="引用 (Ctrl+Q)">
            <i class="el-icon-right"></i>
          </div>
          <div class="toolbar-button" @click="applyFormat('code')" title="代码 (Ctrl+K)">
            <i class="el-icon-tickets"></i>
          </div>
          <div class="toolbar-divider"></div>
          <div class="toolbar-button" @click="insertList('ordered')" title="有序列表">
            <i class="el-icon-s-operation"></i>
          </div>
          <div class="toolbar-button" @click="insertList('unordered')" title="无序列表">
            <i class="el-icon-menu"></i>
          </div>
          <div class="toolbar-button" @click="insertTable()" title="插入表格">
            <i class="el-icon-s-grid"></i>
          </div>
          <div class="toolbar-divider"></div>
          <div class="toolbar-button" @click="applyFormat('undo')" title="撤销 (Ctrl+Z)">
            <i class="el-icon-refresh-left"></i>
          </div>
          <div class="toolbar-button" @click="applyFormat('redo')" title="恢复 (Ctrl+Y)">
            <i class="el-icon-refresh-right"></i>
          </div>
          <div class="toolbar-divider"></div>
          <div class="toolbar-button" @click="scrollToEditor" title="返回编辑区">
            <i class="el-icon-edit"></i>
          </div>
          <div class="toolbar-button" @click="scrollToTop" title="返回顶部">
            <i class="el-icon-top"></i>
          </div>
          <div class="toolbar-button" @click="manualUpdateToc" title="更新目录">
            <i class="el-icon-document"></i>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import E from "wangeditor";
import hljs from "highlight.js";

export default {
  name: "NewBlog",
  data() {
    return {
      form: {},
      user: JSON.parse(localStorage.getItem("xm-user") || "{}"),
      rules: {
        title: [{ required: true, message: "请输入标题", trigger: "blur" }],
        descr: [
          { required: true, message: "请输入简介", trigger: "blur" },
          { min: 5, message: "简介至少需要5个字", trigger: "blur" },
        ],
        categoryId: [
          { required: true, message: "请选择分类", trigger: "change" },
        ],
        cover: [
          { 
            required: true, 
            message: "请上传封面图片", 
            trigger: "change",
            validator: (rule, value, callback) => {
              // 科研人员角色不需要验证封面
              if (this.userRole === 'RESEARCHER') {
                callback();
              } else if (!value) {
                callback(new Error('请上传封面图片'));
              } else {
                callback();
              }
            }
          },
        ],
      },
      tagsArr: [],
      categoryList: [],
      editor: null,
      blogId: this.$route.query.blogId,
      userRole: "",
      tocItems: [], // 存储目录项
      headingUpdateTimer: null, // 用于节流处理目录更新
      tocCollapsed: false, // 目录区域是否收起
      isToolbarCollapsed: false, // 悬浮工具栏是否收起
      availableRoles: [], // 用户可用的角色列表
    };
  },
  created() {
    // 设置页面标题
    document.title = this.blogId ? '编辑博客 - WaterSight' : '发表博客 - WaterSight';
  
    // 加载用户的工具栏偏好设置
    const toolbarState = localStorage.getItem('editor-toolbar-collapsed');
    if (toolbarState !== null) {
      this.isToolbarCollapsed = toolbarState === 'true';
    }

    // 监听登录成功事件
    this.$root.$on("login-success", this.handleLoginSuccess);

    // 初始化表单数据
    this.form = {
      userId: this.user.id,
      userName: this.user.userName,
      userAvatar: this.user.avatar,
    };

    // 加载用户可用角色
    this.loadUserRoles();

    this.loadCategories();

    // 只有在编辑模式下才获取博客详情
    if (this.blogId) {
      this.$request
        .get("/blog/selectById/" + this.blogId)
        .then((res) => {
          if (res.data) {
            this.form = {
              ...res.data,
              userId: this.user.id,
              userName: this.user.userName,
              userAvatar: this.user.avatar,
            };
            this.tagsArr = JSON.parse(this.form.tags || "[]");
            this.$nextTick(() => {
              this.editor.txt.html(this.form.content || "");
            });
            
            // 更新页面标题，包含博客标题
            document.title = `编辑: ${this.form.title} - WaterSight`;
          }
        })
        .catch((err) => {
          console.error("获取博客详情失败:", err);
          this.$message.error("获取博客详情失败");
        });
    }

    this.setRichText();
  },
  beforeDestroy() {
    // 移除事件监听
    this.$root.$off("login-success", this.handleLoginSuccess);
    // 移除全局快捷键监听
    document.removeEventListener('keydown', this.handleGlobalShortcuts);
    // 移除滚动监听
    window.removeEventListener('scroll', this.handleToolbarPosition);
    
    // 清理可能存在的提示元素
    const tooltips = document.querySelectorAll('.editor-tooltip');
    tooltips.forEach(tooltip => {
      if (tooltip.parentNode) {
        tooltip.parentNode.removeChild(tooltip);
      }
    });
  },
  mounted() {
    // 添加全局快捷键监听
    document.addEventListener('keydown', this.handleGlobalShortcuts);
    
    // 添加工具栏置顶监听
    window.addEventListener('scroll', this.handleToolbarPosition);
  },
  methods: {
    handleLoginSuccess() {
      // 登录成功后的处理，如刷新数据等
      this.loadData();
    },
    checkLogin() {
      const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
      if (!user.role) {
        // 通过父组件显示登录弹窗
        this.$parent.$refs.loginDialog.show();
        return false;
      }
      return true;
    },
    save() {
      if (!this.checkLogin()) return;
      if (!this.form.title?.trim()) {
        this.$message.warning("请输入博客标题");
        return;
      }
      if (!this.form.categoryId) {
        this.$message.warning("请选择博客分类");
        return;
      }

      this.$refs.formRef.validate(async (valid) => {
        if (valid) {
          if (!this.editor.txt.html()) {
            this.$message.warning("请输入博客内容");
            return;
          }

          try {
            // 显示加载提示
            const loading = this.$loading({
              lock: true,
              text: "正在保存...",
              spinner: "el-icon-loading",
              background: "rgba(0, 0, 0, 0.7)",
            });

            // 如果是科研人员角色并且没有封面，则使用默认封面
            if (this.userRole === 'RESEARCHER' && !this.form.cover) {
              this.form.cover = 'https://img-blog.csdnimg.cn/20210701164003884.jpg';
            }

            // 确保标签以JSON字符串形式保存
            let tagsString = "";
            if (this.tagsArr && this.tagsArr.length > 0) {
              // 确保tagsArr是数组
              const tagsArray = Array.isArray(this.tagsArr) ? this.tagsArr : [this.tagsArr];
              tagsString = JSON.stringify(tagsArray);
            } else {
              tagsString = "[]";
            }

            // 准备请求数据
            const blogData = {
              ...this.form,
              tags: tagsString, // 使用正确格式化的JSON字符串
              content: this.editor.txt.html(),
              userId: this.user.id,
              userName: this.user.userName,
              userAvatar: this.user.avatar,
            };

            console.log("正在保存博客数据:", blogData);

            // 强制设置更新方法为PUT
            let method = this.form.id ? "PUT" : "POST";
            let url = this.form.id ? "/blog/update" : "/blog/add";
            console.log("使用的保存方法:", method, "URL:", url);

            const res = await this.$request({
              url: url,
              method: method,
              data: blogData,
            });

            loading.close();

            if (res.code === "200") {
              this.$message.success(this.form.id ? "更新成功" : "发布成功");
              
              // 保存成功后延迟返回，确保消息显示
              setTimeout(() => {
                this.$router.go(-1);
              }, 1000);
            } else {
              throw new Error(res.msg || "保存失败");
            }
          } catch (err) {
            console.error("博客保存失败:", err);
            this.$message.error(err.message || "保存失败，请稍后重试");
          }
        }
      });
    },
    handleCoverSuccess(res) {
      if (res.code === "200" && res.data) {
        this.form.cover = res.data;
        // 清除封面验证错误
        this.$refs.formRef.clearValidate("cover");
      } else {
        this.$message.error("封面上传失败");
      }
    },
    
    // 切换标题格式的通用方法（恢复此方法）
    toggleHeading(headingTag) {
      const currentFormat = this.editor.cmd.queryCommandValue('formatBlock');
      if (currentFormat === headingTag) {
        this.editor.cmd.do('formatBlock', '<p>');
      } else {
        this.editor.cmd.do('formatBlock', `<${headingTag}>`);
      }
      
      // 更新目录
      this.$nextTick(() => {
        this.generateToc();
      });
    },
    
    setRichText() {
      this.$nextTick(() => {
        // 初始化编辑器
        this.editor = new E(`#editor`);
        this.editor.highlight = hljs;
        
        // 配置编辑器
        this.editor.config.height = null;
        this.editor.config.uploadImgServer = this.$baseUrl + "/files/editor/upload";
        this.editor.config.uploadFileName = "file";
        this.editor.config.uploadImgHeaders = {
          token: this.user.token,
        };
        this.editor.config.uploadImgParams = {
          type: "img",
        };
        this.editor.config.zIndex = 100;
        
        // 禁用全屏按钮
        this.editor.config.showFullScreen = false;
        
        // 添加Markdown支持
        this.editor.config.markdownConfig = {
          bold: true,
          italic: true,
          header: true,
          underline: true,
          strikethrough: true,
          mark: true,
          superscript: true,
          subscript: true,
          quote: true,
          ol: true,
          ul: true,
          link: true,
          imageLink: true,
          code: true,
          table: true,
          todo: true,
          align: true,
          math: true,
          highlight: true
        };
        
        // 配置快捷键
        this.editor.config.keyup = (e) => {
          // 内容变化时更新目录
          if (this.headingUpdateTimer) {
            clearTimeout(this.headingUpdateTimer);
          }
          this.headingUpdateTimer = setTimeout(() => {
            this.generateToc(false); // 不显示提示消息
          }, 500);
        };
        
        // 设置自定义快捷键
        this.editor.config.customHotKeys = {
          'alt+1': (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggleHeading('h1');
            return false;
          },
          'alt+2': (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggleHeading('h2');
            return false;
          },
          'alt+3': (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggleHeading('h3');
            return false;
          },
          'alt+4': (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggleHeading('h4');
            return false;
          },
          'alt+5': (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggleHeading('h5');
            return false;
          },
          'alt+6': (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggleHeading('h6');
            return false;
          },
          'ctrl+b': (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.editor.cmd.do('bold');
            return false;
          },
          'ctrl+i': (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.editor.cmd.do('italic');
            return false;
          },
          'ctrl+u': (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.editor.cmd.do('underline');
            return false;
          },
          'ctrl+l': (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.editor.cmd.do('link');
            return false;
          },
          'ctrl+q': (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.editor.cmd.do('quote');
            return false;
          },
          'ctrl+k': (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.editor.cmd.do('code');
            return false;
          }
        };
        
        // 创建编辑器
        this.editor.create();
        
        // 设置容器样式
        const textContainer = document.querySelector(".w-e-text-container");
        if (textContainer) {
          textContainer.style.height = "auto";
          textContainer.style.minHeight = "400px";
          textContainer.style.maxHeight = "none";
          textContainer.style.overflowY = "visible";
          textContainer.classList.add('editor-content-container');
        }

        const textArea = document.querySelector(".w-e-text");
        if (textArea) {
          textArea.style.height = "auto";
          textArea.style.minHeight = "400px";
          textArea.style.overflowY = "visible";
        }
        
        // 立即设置工具栏固定在顶部
        this.fixToolbarPosition();
        
        // 添加撤销和重做功能
        this.setupUndoRedoButtons();
        
        // 添加快捷键提示
        this.addShortcutHints();
        
        // 监听编辑器内容变化，更新目录
        this.editor.txt.eventHooks.changeEvents.push(() => {
          if (this.headingUpdateTimer) {
            clearTimeout(this.headingUpdateTimer);
          }
          this.headingUpdateTimer = setTimeout(() => {
            this.generateToc(false); // 不显示提示消息
          }, 500);
        });
        
        // 生成初始目录
        this.$nextTick(() => {
          this.generateToc(false); // 不显示提示消息
        });
      });
    },
    
    // 处理键盘事件 - 特别是撤销和恢复操作
    handleDocumentKeyDown(e) {
      // 检查编辑器是否获得焦点
      const editorFocused = document.activeElement.closest('.w-e-text-container') !== null;
      if (!editorFocused) return;
      
      // 撤销: Ctrl+Z
      if (e.ctrlKey && e.key.toLowerCase() === 'z' && !e.shiftKey) {
        e.preventDefault();
        e.stopPropagation();
        document.execCommand('undo', false, null);
      }
      
      // 恢复: Ctrl+Y 或 Ctrl+Shift+Z
      if ((e.ctrlKey && e.key.toLowerCase() === 'y') || 
          (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 'z')) {
        e.preventDefault();
        e.stopPropagation();
        document.execCommand('redo', false, null);
      }
    },

    // 设置撤销和恢复功能
    setupUndoRedoFunctions() {
      setTimeout(() => {
        // 获取撤销按钮
        const undoBtn = document.querySelector('.w-e-menu[data-title="撤销"]');
        if (undoBtn) {
          undoBtn.onclick = (e) => {
            e.preventDefault();
            e.stopPropagation();
            document.execCommand('undo', false, null);
          };
        }
        
        // 获取恢复按钮
        const redoBtn = document.querySelector('.w-e-menu[data-title="恢复"]');
        if (redoBtn) {
          redoBtn.onclick = (e) => {
            e.preventDefault();
            e.stopPropagation();
            document.execCommand('redo', false, null);
          };
        }
      }, 500);
    },

    // 修复编辑器工具栏并设置固定在顶部
    fixEditorToolbar() {
      setTimeout(() => {
        const toolbar = document.querySelector('.w-e-toolbar');
        if (!toolbar) return;
        
        // 去除编辑器原本的position: sticky
        toolbar.style.position = 'fixed';
        toolbar.style.top = '0';
        toolbar.style.left = '0';
        toolbar.style.right = '0';
        toolbar.style.zIndex = '10000';
        toolbar.style.background = 'var(--bg-color-secondary)'; 
        toolbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        toolbar.style.padding = '5px 10px';
        
        // 给内容区域添加上边距，避免被固定工具栏遮挡
        const textContainer = document.querySelector('.w-e-text-container');
        if (textContainer) {
          const toolbarHeight = toolbar.offsetHeight;
          textContainer.style.marginTop = `${toolbarHeight + 10}px`;
        }
        
        // 监听窗口大小改变，确保工具栏大小正确
        window.addEventListener('resize', () => {
          if (textContainer) {
            const toolbarHeight = toolbar.offsetHeight;
            textContainer.style.marginTop = `${toolbarHeight + 10}px`;
          }
        });
      }, 300);
    },
    
    // 生成目录
    generateToc(showMessage = false) {
      const editorContentEl = document.querySelector('.w-e-text');
      if (!editorContentEl) return;
      
      // 清空现有目录
      this.tocItems = [];
      
      // 查找所有标题元素
      const headings = editorContentEl.querySelectorAll('h1, h2, h3, h4, h5, h6');
      
      // 为每个标题添加ID并收集目录项
      headings.forEach((heading, index) => {
        // 获取标题级别
        const level = parseInt(heading.tagName.substring(1));
        
        // 生成唯一ID
        const id = `heading-${index}`;
        heading.id = id;
        
        // 添加到目录项
        this.tocItems.push({
          id,
          text: heading.textContent.trim() || `[空标题 ${level}]`,
          level,
        });
      });
      
      // 只有在手动触发更新时才显示提示
      if (showMessage) {
        if (this.tocItems.length === 0) {
          this.$message.info('未检测到标题，请添加标题以生成目录');
        } else {
          this.$message.success(`已更新目录，共 ${this.tocItems.length} 个标题`);
        }
      }
    },
    
    // 滚动到指定标题
    scrollToHeading(id) {
      const el = document.getElementById(id);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    },
    
    async loadCategories() {
      try {
        const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
        this.userRole = user.browseRole || "";

        // 首先获取所有分类
        let res = await this.$request.get("/category/selectByRole", {
          params: {
            role: this.userRole === "ALL" ? "HOBBYIST" : this.userRole,
          },
        });

        if (res.code === "200") {
          this.categoryList = res.data || [];
          
          // 如果是ALL角色（全部用户），可能需要获取其他角色的分类
          if (this.userRole === "ALL" && user.role === "ADMIN") {
            // 如果是管理员用户，获取所有分类
            const allCategoriesRes = await this.$request.get("/category/all");
            if (allCategoriesRes.code === "200") {
              this.categoryList = allCategoriesRes.data || [];
            }
          }
          
          if (this.categoryList.length === 0) {
            console.warn(`未找到角色 ${this.userRole} 的分类数据`);
          }
        } else {
          throw new Error(res.msg || "获取分类失败");
        }
      } catch (error) {
        console.error("加载分类失败:", error);
        this.$message.error("获取分类失败，请稍后重试");
      }
    },

    // 添加处理工具栏位置的方法
    handleToolbarPosition() {
      this.fixToolbarPosition();
    },

    // 修复工具栏位置的方法
    fixToolbarPosition() {
      const toolbar = document.querySelector('.w-e-toolbar');
      if (!toolbar) return;
      
      // 添加固定定位样式
      toolbar.classList.add('w-e-toolbar-fixed');
      
      // 获取所有按钮并确保它们可点击
      const buttons = toolbar.querySelectorAll('.w-e-menu');
      buttons.forEach(btn => {
        btn.style.cursor = 'pointer';
      });
      
      // 为编辑区域添加顶部外边距，防止内容被工具栏覆盖
      const textContainer = document.querySelector('.w-e-text-container');
      if (textContainer) {
        const toolbarHeight = toolbar.offsetHeight;
        textContainer.style.marginTop = `${toolbarHeight + 10}px`;
      }
    },

    // 设置撤销和重做按钮的功能
    setupUndoRedoButtons() {
      setTimeout(() => {
        const undoBtn = document.querySelector('.w-e-menu[data-title="撤销"]');
        if (undoBtn) {
          // 移除原有事件
          const newUndoBtn = undoBtn.cloneNode(true);
          undoBtn.parentNode.replaceChild(newUndoBtn, undoBtn);
          
          // 添加新的点击事件
          newUndoBtn.addEventListener('click', () => {
            document.execCommand('undo', false, null);
          });
        }
        
        const redoBtn = document.querySelector('.w-e-menu[data-title="恢复"]');
        if (redoBtn) {
          // 移除原有事件
          const newRedoBtn = redoBtn.cloneNode(true);
          redoBtn.parentNode.replaceChild(newRedoBtn, redoBtn);
          
          // 添加新的点击事件
          newRedoBtn.addEventListener('click', () => {
            document.execCommand('redo', false, null);
          });
        }
      }, 500);
    },

    // 处理全局快捷键
    handleGlobalShortcuts(e) {
      // 仅当编辑器获得焦点时处理快捷键
      const editorFocused = document.activeElement.closest('.w-e-text-container') !== null;
      if (!editorFocused) return;
      
      // 处理撤销恢复
      if (e.ctrlKey && e.key.toLowerCase() === 'z' && !e.shiftKey) {
        e.preventDefault();
        document.execCommand('undo', false, null);
        return;
      }
      
      if ((e.ctrlKey && e.key.toLowerCase() === 'y') || 
          (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 'z')) {
        e.preventDefault();
        document.execCommand('redo', false, null);
        return;
      }
      
      // 处理标题快捷键
      if (e.altKey && e.key >= '1' && e.key <= '6') {
        e.preventDefault();
        
        const headingLevel = parseInt(e.key);
        const headingTag = `h${headingLevel}`;
        this.toggleHeading(headingTag);
      }
    },

    // 添加快捷键提示
    addShortcutHints() {
      setTimeout(() => {
        // 获取所有工具栏按钮
        const toolbar = document.querySelector('.w-e-toolbar');
        if (!toolbar) return;
        
        // 快捷键映射
        const shortcutMap = {
          '标题': '标题快捷键: Alt+1~6',
          '加粗': '加粗: Ctrl+B',
          '斜体': '斜体: Ctrl+I',
          '下划线': '下划线: Ctrl+U',
          '撤销': '撤销: Ctrl+Z',
          '恢复': '恢复: Ctrl+Y/Ctrl+Shift+Z',
          '代码': '代码: Ctrl+K',
          '引用': '引用: Ctrl+Q',
          '链接': '链接: Ctrl+L'
        };
        
        // 为每个按钮添加提示和快捷键显示
        const buttons = toolbar.querySelectorAll('.w-e-menu');
        buttons.forEach(btn => {
          const title = btn.getAttribute('data-title');
          if (title && shortcutMap[title]) {
            // 添加快捷键到按钮标题
            btn.setAttribute('data-title', `${title} (${shortcutMap[title].split(': ')[1]})`);
            
            // 添加悬停显示提示功能
            btn.addEventListener('mouseenter', () => {
              // 删除任何现有提示
              const existingTooltips = document.querySelectorAll('.editor-tooltip');
              existingTooltips.forEach(t => t.parentNode && t.parentNode.removeChild(t));
              
              // 创建新提示
              const tooltip = document.createElement('div');
              tooltip.className = 'editor-tooltip';
              tooltip.textContent = shortcutMap[title];
              document.body.appendChild(tooltip);
              
              // 设置提示位置
              const rect = btn.getBoundingClientRect();
              tooltip.style.left = `${rect.left + rect.width/2}px`;
              tooltip.style.transform = 'translateX(-50%)';
              
              // 先显示在按钮下方
              tooltip.style.top = `${rect.bottom + 10}px`;
              
              // 获取提示尺寸后调整到按钮上方
              setTimeout(() => {
                tooltip.style.top = `${rect.top - tooltip.offsetHeight - 10}px`;
              }, 10);
            });
            
            // 鼠标离开时移除提示
            btn.addEventListener('mouseleave', () => {
              const tooltips = document.querySelectorAll('.editor-tooltip');
              tooltips.forEach(t => t.parentNode && t.parentNode.removeChild(t));
            });
          }
        });
      }, 500);
    },

    // 应用格式化工具的方法
    applyFormat(type) {
      if (!this.editor) return;
      
      switch(type) {
        case 'bold':
          this.editor.cmd.do('bold');
          break;
        case 'italic':
          this.editor.cmd.do('italic');
          break;
        case 'underline':
          this.editor.cmd.do('underline');
          break;
        case 'link':
          this.editor.cmd.do('link');
          break;
        case 'image':
          // 调用wangEditor的图片上传功能
          const imageMenu = document.querySelector('.w-e-menu[data-title^="图片"]');
          if (imageMenu) {
            imageMenu.click();
          }
          break;
        case 'quote':
          this.editor.cmd.do('quote');
          break;
        case 'code':
          this.editor.cmd.do('code');
          break;
        case 'fontSize':
          // 调用wangEditor的字号菜单
          const fontSizeMenu = document.querySelector('.w-e-menu[data-title^="字号"]');
          if (fontSizeMenu) {
            fontSizeMenu.click();
          }
          break;
        case 'foreColor':
          // 调用wangEditor的文字颜色菜单
          const foreColorMenu = document.querySelector('.w-e-menu[data-title^="文字颜色"]');
          if (foreColorMenu) {
            foreColorMenu.click();
          }
          break;
        case 'undo':
          document.execCommand('undo', false, null);
          break;
        case 'redo':
          document.execCommand('redo', false, null);
          break;
        default:
          break;
      }

      // 编辑器获得焦点
      this.editor.txt.selection.restoreSelection();
    },

    // 切换悬浮工具栏显示状态
    toggleFloatingToolbar() {
      this.isToolbarCollapsed = !this.isToolbarCollapsed;
      // 存储状态到localStorage，让用户的偏好可以保持
      localStorage.setItem('editor-toolbar-collapsed', this.isToolbarCollapsed.toString());
    },

    // 滚动到编辑区
    scrollToEditor() {
      const editorArea = document.querySelector('.w-e-text');
      if (editorArea) {
        editorArea.scrollIntoView({ behavior: 'smooth', block: 'center' });
        // 聚焦编辑器
        this.editor.txt.selection.createEmptyRange();
        this.editor.txt.selection.restoreSelection();
      }
    },

    // 滚动到页面顶部
    scrollToTop() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    },

    // 加载用户可用角色
    loadUserRoles() {
      const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
      this.userRole = user.browseRole || "";
      
      // 设置可用角色
      this.availableRoles = [];
      
      // 普通用户角色始终可用
      this.availableRoles.push({
        value: 'ALL',
        label: '普通用户',
        icon: 'el-icon-user'
      });
      
      // 如果用户有特定角色权限
      if (user.role) {
        switch(user.role) {
          case 'HOBBYIST':
            this.availableRoles.push({
              value: 'HOBBYIST',
              label: '水域爱好者',
              icon: 'el-icon-ship'
            });
            break;
          case 'RESEARCHER':
            this.availableRoles.push({
              value: 'RESEARCHER',
              label: '科研人员',
              icon: 'el-icon-data-analysis'
            });
            break;
          case 'POLICY_MAKER':
            this.availableRoles.push({
              value: 'POLICY_MAKER',
              label: '政策制定者',
              icon: 'el-icon-office-building'
            });
            break;
          case 'EDUCATOR':
            this.availableRoles.push({
              value: 'EDUCATOR',
              label: '教育工作者',
              icon: 'el-icon-reading'
            });
            break;
          case 'ADMIN':
            // 管理员可以使用所有角色
            this.availableRoles.push(
              {
                value: 'HOBBYIST',
                label: '水域爱好者',
                icon: 'el-icon-ship'
              },
              {
                value: 'RESEARCHER',
                label: '科研人员',
                icon: 'el-icon-data-analysis'
              },
              {
                value: 'POLICY_MAKER',
                label: '政策制定者',
                icon: 'el-icon-office-building'
              },
              {
                value: 'EDUCATOR',
                label: '教育工作者',
                icon: 'el-icon-reading'
              },
              {
                value: 'ADMIN',
                label: '管理员',
                icon: 'el-icon-s-tools'
              }
            );
            break;
        }
      }
    },
    
    // 处理角色切换
    handleRoleChange(role) {
      if (role === this.userRole) return;
      
      this.userRole = role;
      
      // 更新本地存储中的浏览角色
      const user = JSON.parse(localStorage.getItem("xm-user") || "{}");
      user.browseRole = role;
      localStorage.setItem("xm-user", JSON.stringify(user));
      
      // 重新加载分类
      this.loadCategories();
      
      this.$message.success(`已切换到 ${this.roleDisplayName} 身份`);
    },

    // 在方法部分添加插入列表的方法
    insertList(type) {
      if (!this.editor) return;
      
      if (type === 'ordered') {
        this.editor.cmd.do('insertOrderedList');
      } else if (type === 'unordered') {
        this.editor.cmd.do('insertUnorderedList');
      }
      
      // 编辑器获得焦点
      this.editor.txt.selection.restoreSelection();
    },

    // 插入表格
    insertTable() {
      // 调用wangEditor的表格菜单
      const tableMenu = document.querySelector('.w-e-menu[data-title^="表格"]');
      if (tableMenu) {
        tableMenu.click();
      }
    },

    // 手动更新目录，显示提示
    manualUpdateToc() {
      this.generateToc(true);
    },
  },
  computed: {
    roleDisplayName() {
      const roleMap = {
        'ALL': '普通用户',
        'HOBBYIST': '水域爱好者',
        'RESEARCHER': '科研人员',
        'POLICY_MAKER': '政策制定者',
        'EDUCATOR': '教育工作者',
        'ADMIN': '管理员'
      };
      return roleMap[this.userRole] || '未知角色';
    },
    roleTagType() {
      const typeMap = {
        'ALL': 'info',
        'HOBBYIST': 'success',
        'RESEARCHER': 'warning',
        'POLICY_MAKER': 'danger',
        'EDUCATOR': 'primary',
        'ADMIN': ''
      };
      return typeMap[this.userRole] || 'info';
    },
    canSwitchRole() {
      return this.availableRoles.length > 1;
    }
  },
};
</script>

<style lang="less" scoped>
.blog-editor-container {
  display: flex;
  min-height: calc(100vh - 60px);
  background: var(--bg-gradient);
  padding: 0;
  width: 100%;
  margin: 0;
  position: relative;
}

// 左侧目录区样式
.toc-sidebar {
  width: 250px;
  background-color: var(--bg-color-alpha, rgba(255, 255, 255, 0.9));
  backdrop-filter: blur(10px);
  border-right: 1px solid var(--border-color, #ebeef5);
  position: fixed;
  left: 0;
  top: 60px; // 顶部导航栏高度
  height: calc(100vh - 60px);
  z-index: 90;
  transition: all 0.3s ease;
  
  &.collapsed {
    width: 30px;
    overflow: hidden;
  }
}

.toc-toggle {
  position: absolute;
  right: 0;
  top: 10px;
  width: 20px;
  height: 40px;
  background-color: var(--primary-color, #0a4d68);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 4px 0 0 4px;
  z-index: 2;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
  
  &:hover {
    background-color: var(--primary-color-hover, #05bfdb);
  }
}

.toc-content {
  padding: 20px 15px;
  height: 100%;
  overflow-y: auto;
}

// 主编辑区样式
.blog-editor-content {
  flex: 1;
  max-width: calc(100% - 250px);
  margin-left: 250px;
  padding: 20px 40px;
  transition: all 0.3s ease;
  border-radius: 0;
  position: relative;
  background: var(--bg-color-alpha);
  backdrop-filter: blur(10px);
  border: 0;
  
  &.wide-mode {
    max-width: calc(100% - 30px);
    margin-left: 30px;
  }
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 2px solid var(--border-color);
  padding-bottom: 20px;
  
  .editor-title {
    margin: 0;
    font-size: 24px;
    font-weight: 600;
    position: relative;
    padding-left: 15px;
    color: var(--text-color-primary);
  }
  
  .editor-title::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 5px;
    background: var(--primary-gradient);
    border-radius: 3px;
  }
  
  .user-role-info {
    display: flex;
    align-items: center;
    margin-left: auto;
    margin-right: 15px;
    font-size: 14px;
    
    span {
      margin-right: 5px;
      color: #606266;
    }
    
    .el-tag {
      border-radius: 12px;
      padding: 0 10px;
    }
    
    .role-dropdown-trigger {
      cursor: pointer;
      display: flex;
      align-items: center;
      
      i {
        margin-left: 5px;
      }
    }
  }
}

.editor-btn {
  background: linear-gradient(to right, #3498db, #2980b9);
  border: none;
  padding: 12px 25px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 30px;
  box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
  transition: all 0.3s ease;
}

.editor-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 7px 20px rgba(52, 152, 219, 0.4);
}

.blog-form {
  margin-top: 20px;
}

.form-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
  margin-bottom: 30px;
}

.form-left {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-right {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.blog-form /deep/.el-form-item__label {
  font-size: 16px;
  color: #2c3e50;
  font-weight: 500;
}

.title-input /deep/.el-input__inner {
  background: var(--bg-color-secondary);
  backdrop-filter: blur(5px);
  border: none;
  position: relative;
  height: 40px;
  line-height: 40px;
  font-size: 15px;
  color: var(--text-color-primary);

  &:focus {
    box-shadow: 0 0 15px var(--primary-shadow);
  }
}

.descr-input /deep/.el-textarea__inner {
  padding: 10px 15px;
  border-radius: 12px;
  border: 2px solid var(--border-color);
  transition: all 0.3s ease;
  background: var(--bg-color-secondary);
  min-height: 80px;
  max-height: 120px;
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-color-primary);
}

.descr-input /deep/.el-textarea__inner:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--primary-shadow);
}

.cover-upload {
  margin: 10px 0;
  position: relative;
}

.cover-uploader /deep/.el-upload--picture-card {
  width: 100%;
  height: 200px;
  margin: 0;
  border-radius: 12px;
  border: 2px dashed var(--primary-color);
  background: var(--bg-color-secondary);
  backdrop-filter: blur(5px);
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.upload-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;

  .el-icon-camera-solid {
    font-size: 48px;
    color: var(--primary-color);
    margin-bottom: -35px;
  }

  .upload-text {
    font-size: 16px;
    color: var(--text-color-primary);
  }
}

.upload-success-animation {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2;

  .dolphin-icon {
    width: 60px;
    height: 60px;
    animation: dolphinJump 1s ease-in-out;
  }
}

@keyframes wave {
  0% {
    background-position: 0% 0%;
  }
  100% {
    background-position: 100% 100%;
  }
}

@keyframes dolphinJump {
  0% {
    transform: translateY(50px) rotate(0deg);
    opacity: 0;
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
    opacity: 1;
  }
  100% {
    transform: translateY(0) rotate(360deg);
    opacity: 1;
  }
}

.category-select,
.tags-select {
  /deep/.el-select {
    width: 100%;
    max-width: 400px;
  }

  /deep/.el-select .el-input__inner {
    background: var(--bg-color-secondary);
    backdrop-filter: blur(5px);
    border: none;
    position: relative;
    height: 40px;
    line-height: 40px;
    color: var(--text-color-primary);

    &:focus {
      box-shadow: 0 0 15px var(--primary-shadow);
    }
  }
}

.tags-tip {
  color: #7f8c8d;
  font-size: 14px;
  margin-top: 8px;
  font-style: italic;
}

.content-editor {
  margin-top: 0;

  /deep/ .w-e-text-container {
    min-height: 400px !important;
    height: auto !important;
    max-height: none !important;
    overflow-y: visible !important;
  }
}

.wang-editor {
  background: var(--bg-color-secondary) !important;
  backdrop-filter: blur(5px);
  border: none !important;
  position: relative;
  overflow: visible;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border: 2px solid var(--border-color);
  }
}

.wang-editor:focus-within {
  border-color: var(--primary-color) !important;
  box-shadow: 0 0 0 3px var(--primary-shadow);
}

/deep/.w-e-toolbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: var(--bg-color-secondary) !important;
  border-bottom: 1px solid var(--border-color) !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

/deep/.w-e-text-container {
  min-height: 400px !important;
  height: auto !important;
  max-height: none !important;
  background: var(--bg-color-secondary) !important;
}

/deep/.w-e-text {
  padding: 20px 25px !important;
  min-height: 400px !important;
  height: auto !important;
  overflow: visible !important;
  color: var(--text-color-primary) !important;
}

/deep/.el-select-dropdown {
  border-radius: 12px;
  box-shadow: 0 8px 30px var(--shadow-color);
  background-color: var(--bg-color-secondary);
}

/deep/.el-select-dropdown__item {
  padding: 12px 20px;
  font-size: 15px;
  color: var(--text-color-primary);

  &:hover {
    background-color: var(--bg-color-hover);
  }

  &.selected {
    color: var(--primary-color);
    background-color: var(--primary-color-light);
  }
}

/deep/.el-tag {
  border-radius: 20px;
  padding: 6px 15px;
  margin: 4px;
  background-color: var(--primary-color-light);
  color: var(--primary-color);
  border-color: var(--primary-color-light);
}

.bubble-select /deep/ {
  .el-select__tags {
    padding: 6px;
    display: flex;
    flex-wrap: nowrap;
    gap: 8px;
    overflow-x: auto;
    white-space: nowrap;
    scrollbar-width: thin;

    &::-webkit-scrollbar {
      height: 4px;
    }

    &::-webkit-scrollbar-track {
      background: rgba(52, 152, 219, 0.1);
      border-radius: 2px;
    }

    &::-webkit-scrollbar-thumb {
      background: rgba(52, 152, 219, 0.3);
      border-radius: 2px;

      &:hover {
        background: rgba(52, 152, 219, 0.5);
      }
    }
  }

  .el-tag {
    flex-shrink: 0;
    height: auto;
    padding: 8px 15px;
    border-radius: 20px;
    margin: 0;
    background: #e67e22;
    border: none;
    position: relative;
    overflow: hidden;
    display: inline-flex;
    align-items: center;
  }
}

@media screen and (max-width: 1200px) {
  .blog-editor-content {
    max-width: 95%;
  }
}

@media screen and (max-width: 992px) {
  .toc-sidebar {
    width: 200px;
    
    &.collapsed {
      width: 0;
    }
  }
  
  .blog-editor-content {
    max-width: calc(100% - 200px);
    margin-left: 200px;
    padding: 20px;
    
    &.wide-mode {
      max-width: 100%;
      margin-left: 0;
    }
  }
  
  .form-layout {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
}

@media screen and (max-width: 768px) {
  .toc-sidebar {
    width: 0;
    
    &.collapsed {
      width: 0;
    }
  }
  
  .blog-editor-content {
    max-width: 100%;
    margin-left: 0;
    padding: 15px;
  }
  
  .toc-toggle {
    right: -20px;
    border-radius: 0 4px 4px 0;
  }
}

/deep/ *::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

/deep/ *::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 3px;
}

/deep/ *::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;

  &:hover {
    background: rgba(0, 0, 0, 0.3);
  }
}

.shortcut-icon {
  display: none;
}

.shortcut-tooltip {
  display: none;
}

/* CSDN风格的工具栏固定样式 */
.w-e-toolbar-fixed {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  z-index: 10001 !important;
  background-color: var(--bg-color-secondary) !important;
  border-bottom: 1px solid var(--border-color) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
  padding: 5px 20px !important;
  width: 100% !important;
  display: flex !important;
  justify-content: center !important;
}

.editor-content-container {
  margin-top: 50px !important; /* 为固定的工具栏腾出空间 */
}

.editor-tooltip {
  position: fixed;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 12px;
  z-index: 20000;
  pointer-events: none;
  transition: opacity 0.2s;
}

.editor-tooltip:after {
  content: '';
  position: absolute;
  top: -5px;
  left: 50%;
  transform: translateX(-50%);
  border-width: 0 5px 5px;
  border-style: solid;
  border-color: transparent transparent rgba(0, 0, 0, 0.8);
}

// 目录样式
.toc-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 15px;
  color: var(--text-color-primary, #303133);
  display: flex;
  align-items: center;
  
  &::before {
    content: "";
    width: 4px;
    height: 16px;
    background: var(--primary-color, #0a4d68);
    margin-right: 8px;
    border-radius: 2px;
  }
}

.toc-list {
  max-height: calc(100vh - 150px);
  overflow-y: auto;
  padding: 10px;
  border-radius: 8px;
  background-color: rgba(0, 0, 0, 0.02);
  
  &::-webkit-scrollbar {
    width: 4px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 2px;
  }
  
  &::-webkit-scrollbar-track {
    background: transparent;
  }
}

.toc-empty {
  color: var(--text-color-secondary, #909399);
  font-style: italic;
  font-size: 13px;
  text-align: center;
  padding: 15px 0;
}

.toc-item {
  padding: 8px 12px;
  font-size: 14px;
  color: var(--text-color-regular, #606266);
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: all 0.2s;
  border-radius: 4px;
  position: relative;
  margin-bottom: 2px;
  display: flex;
  align-items: center;
  
  &::before {
    content: "";
    width: 3px;
    height: 0;
    background: var(--primary-color, #0a4d68);
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    transition: height 0.2s;
  }
  
  &:hover {
    color: var(--primary-color, #0a4d68);
    background-color: var(--bg-color-hover, #f5f7fa);
    
    &::before {
      height: 100%;
    }
  }
}

.toc-level-1 {
  padding-left: 12px;
  font-weight: 600;
}

.toc-level-2 {
  padding-left: 24px;
}

.toc-level-3 {
  padding-left: 36px;
}

.toc-level-4 {
  padding-left: 48px;
}

.toc-level-5 {
  padding-left: 60px;
  font-size: 13px;
}

.toc-level-6 {
  padding-left: 72px;
  font-size: 13px;
}

// 右侧悬浮工具栏样式
.floating-toolbar {
  position: fixed;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: auto;
  background-color: var(--bg-color-secondary);
  border-radius: 12px 0 0 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  transition: all 0.3s ease;
  overflow: visible;
  border: 1px solid var(--border-color);
  
  &.collapsed {
    right: -200px;
    
    .toolbar-toggle {
      left: -20px;
    }
  }
}

.toolbar-toggle {
  position: absolute;
  left: -20px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 40px;
  background-color: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 4px 0 0 4px;
  z-index: 2;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
  
  &:hover {
    background-color: var(--primary-color-hover);
  }
}

.floating-toolbar-inner {
  padding: 15px;
  width: 200px;
  transition: all 0.3s ease;
  max-height: 80vh;
  overflow-y: auto;
  
  &::-webkit-scrollbar {
    width: 4px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 2px;
  }
  
  &::-webkit-scrollbar-track {
    background: transparent;
  }
}

.toolbar-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 15px;
  color: var(--text-color-primary);
  text-align: center;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 8px;
}

.toolbar-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.toolbar-button {
  width: 40px;
  height: 40px;
  background-color: var(--bg-color-alpha);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  font-size: 16px;
  color: var(--text-color-regular);
  
  i {
    font-size: 18px;
    line-height: 1;
  }
  
  &:hover {
    background-color: var(--bg-color-hover);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    color: var(--primary-color);
  }
  
  &:active {
    transform: translateY(0);
    box-shadow: none;
  }
}

.toolbar-divider {
  width: 100%;
  height: 1px;
  background-color: var(--border-color);
  margin: 8px 0;
}

.heading-icon {
  font-weight: bold;
  font-size: 14px;
  color: var(--text-color-regular);
}

.toolbar-button:hover .heading-icon {
  color: var(--primary-color);
}

// 添加科研人员角色提示样式
.researcher-note {
  background-color: rgba(52, 152, 219, 0.1);
  border-radius: 10px;
  padding: 15px;
  margin: 20px 0;
  display: flex;
  align-items: center;
  
  i {
    font-size: 24px;
    color: #3498db;
    margin-right: 10px;
  }
  
  p {
    margin: 0;
    font-size: 14px;
    color: var(--text-color-regular);
    line-height: 1.5;
  }
}

// 添加响应式样式
@media screen and (max-width: 768px) {
  .floating-toolbar {
    right: 10px;
  }
  
  .floating-toolbar-inner {
    width: 180px;
  }
  
  .toolbar-button {
    width: 36px;
    height: 36px;
  }
}
</style>
