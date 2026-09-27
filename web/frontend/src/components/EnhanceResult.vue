export default {
  props: {
    result: {
      type: Object,
      required: false,
      default: null,
    },
    enhanceServiceUrl: {
      type: String,
      required: false,
      default: "",
    }
  },
  data() {
    return {
      originalSrc: "",
      resultSrc: "",
      error: null,
      debugInfo: null,
      pythonServiceUrl: "", // 将在created中初始化
    };
  },
  created() {
    // 初始化pythonServiceUrl，优先使用props传入的值，其次使用环境变量
    this.pythonServiceUrl = this.enhanceServiceUrl || process.env.VUE_APP_ENHANCE_URL || "http://localhost:8002";
    
    // 确保pythonServiceUrl末尾没有斜杠
    if (this.pythonServiceUrl) {
      this.pythonServiceUrl = this.pythonServiceUrl.replace(/\/$/, "");
    }
    
    console.log("EnhanceResult组件 - Python服务URL:", this.pythonServiceUrl);
    console.log("EnhanceResult组件 - 环境变量:", process.env.VUE_APP_ENHANCE_URL);
    
    // 初始化处理result
    if (this.result) {
      this.handleResultChange(this.result);
    }
  },
  watch: {
    result: {
      handler(newVal) {
        console.log("EnhanceResult收到新的结果:", newVal);
        if (newVal) {
          this.error = null;
          this.debugInfo = null;
          this.originalSrc = "";
          this.resultSrc = "";
          
          try {
            // 记录完整的结果对象，用于调试
            this.debugInfo = JSON.stringify(newVal, null, 2);
            console.log("结果对象详情:", this.debugInfo);
            
            // 检查是否有原始图像URL
            if (newVal.original_image) {
              this.originalSrc = this.formatImageUrl(newVal.original_image);
              console.log("设置原始图像URL:", this.originalSrc);
            } else {
              console.warn("结果中没有原始图像URL");
              // 尝试查找其他可能的字段名
              const possibleFields = ['originalImage', 'original', 'source_image'];
              for (const field of possibleFields) {
                if (newVal[field]) {
                  this.originalSrc = this.formatImageUrl(newVal[field]);
                  console.log(`使用替代字段 '${field}' 设置原始图像URL:`, this.originalSrc);
                  break;
                }
              }
            }
            
            // 检查是否有结果图像URL
            if (newVal.result_image) {
              this.resultSrc = this.formatImageUrl(newVal.result_image);
              console.log("设置结果图像URL:", this.resultSrc);
            } else {
              console.warn("结果中没有结果图像URL");
              // 尝试查找其他可能的字段名
              const possibleFields = ['resultImage', 'enhanced_image', 'target_image', 'output'];
              for (const field of possibleFields) {
                if (newVal[field]) {
                  this.resultSrc = this.formatImageUrl(newVal[field]);
                  console.log(`使用替代字段 '${field}' 设置结果图像URL:`, this.resultSrc);
                  break;
                }
              }
            }
            
            // 如果仍然没有找到图像URL，尝试构造默认URL
            if (!this.originalSrc && newVal.filename) {
              const filename = newVal.filename;
              this.originalSrc = this.formatImageUrl(`/static/images/original/${filename}`);
              console.log("使用文件名构造原始图像URL:", this.originalSrc);
            }
            
            if (!this.resultSrc && newVal.filename) {
              const filename = newVal.filename;
              const baseFilename = filename.split('.')[0];
              const extension = filename.split('.').pop();
              this.resultSrc = this.formatImageUrl(`/static/images/enhanced/${baseFilename}_enhanced.${extension}`);
              console.log("使用文件名构造结果图像URL:", this.resultSrc);
            }
            
            // 验证图像URL是否有效
            this.validateImageUrls();
            
          } catch (error) {
            console.error("处理结果对象时出错:", error);
            this.error = `处理结果时出错: ${error.message}`;
          }
        } else {
          console.log("EnhanceResult: 结果为空");
          this.originalSrc = "";
          this.resultSrc = "";
          this.error = null;
          this.debugInfo = null;
        }
      },
      immediate: true,
    },
  },
  methods: {
    formatImageUrl(url) {
      if (!url) {
        console.warn("formatImageUrl: URL为空");
        return "";
      }
      
      console.log("格式化图像URL:", url);
      
      // 判断url是否已经是完整URL
      if (url.startsWith('http://') || url.startsWith('https://')) {
        console.log("URL已是完整URL，直接返回:", url);
        return url;
      }
      
      // 判断是否以/开头
      if (!url.startsWith('/')) {
        url = '/' + url;
        console.log("添加前导斜杠后的URL:", url);
      }
      
      // 如果url以/api/开头，使用backend服务地址
      if (url.startsWith('/api/')) {
        const baseApi = process.env.VUE_APP_BASE_API || "";
        const formattedUrl = baseApi + url.substring(4);
        console.log("API URL格式化结果:", formattedUrl);
        return formattedUrl;
      }
      
      // 如果url以/static/开头，使用Python服务地址
      if (url.startsWith('/static/')) {
        const formattedUrl = this.pythonServiceUrl + url;
        console.log("静态资源URL格式化结果:", formattedUrl);
        return formattedUrl;
      }
      
      // 默认添加Python服务地址
      const formattedUrl = this.pythonServiceUrl + url;
      console.log("默认URL格式化结果:", formattedUrl);
      return formattedUrl;
    },
    
    validateImageUrls() {
      // 检查原始图像URL是否有效
      if (this.originalSrc) {
        console.log("验证原始图像URL:", this.originalSrc);
        const img = new Image();
        img.onload = () => {
          console.log("原始图像URL有效");
        };
        img.onerror = () => {
          console.warn("原始图像URL无效:", this.originalSrc);
          this.error = "原始图像加载失败，请检查URL";
        };
        img.src = this.originalSrc;
      }
      
      // 检查结果图像URL是否有效
      if (this.resultSrc) {
        console.log("验证结果图像URL:", this.resultSrc);
        const img = new Image();
        img.onload = () => {
          console.log("结果图像URL有效");
        };
        img.onerror = () => {
          console.warn("结果图像URL无效:", this.resultSrc);
          this.error = "结果图像加载失败，请检查URL";
          
          // 尝试添加时间戳避免缓存问题
          const timestamp = new Date().getTime();
          this.resultSrc = `${this.resultSrc}?t=${timestamp}`;
          console.log("添加时间戳后重新尝试:", this.resultSrc);
        };
        img.src = this.resultSrc;
      }
    },
    
    // 提供一个方法供父组件调用，用于手动刷新图像
    refreshImages() {
      console.log("手动刷新图像");
      if (this.result) {
        // 重新处理图像URL
        if (this.result.original_image) {
          this.originalSrc = this.formatImageUrl(this.result.original_image);
        }
        if (this.result.result_image) {
          const timestamp = new Date().getTime();
          this.resultSrc = `${this.formatImageUrl(this.result.result_image)}?t=${timestamp}`;
        }
        this.validateImageUrls();
      }
    }
  },
  computed: {
    hasResult() {
      return this.originalSrc && this.resultSrc;
    },
    
    hasError() {
      return !!this.error;
    },
    
    // 判断是否应该显示调试信息
    showDebugInfo() {
      return process.env.NODE_ENV === 'development' && this.debugInfo;
    }
  },
}; 