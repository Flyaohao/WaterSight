<template>
  <div class="home-container">
    <!-- 深度指示器 -->
    <div class="depth-indicator">
      <div class="depth-bar">
        <div
            class="depth-progress"
            :style="{ height: depthProgress + '%' }"
        ></div>
      </div>
      <div
          class="depth-marker"
          v-for="(marker, index) in depthMarkers"
          :key="index"
          :style="{ top: marker.position + '%' }"
          :class="{
          active:
            scrollPosition >= marker.threshold ||
            activeMarker === marker.target,
        }"
          @click="scrollToSection(marker.target, true)"
      >
        <span class="marker-label">
          {{ marker.label }}
          <span class="depth-marker-hint">{{ marker.depth }}</span>
        </span>
      </div>
    </div>

    <!-- 潜艇动画 -->
    <div
        class="submarine"
        :style="{ top: submarinePosition + '%' }"
        :class="{ 'lights-on': lightsOn }"
    >
      <div class="submarine-window"></div>
      <div class="submarine-light"></div>
      <div class="submarine-bubbles">
        <div class="sub-bubble" v-for="n in 3" :key="n"></div>
      </div>
    </div>

    <!-- 气泡效果 -->
    <div class="bubbles-container">
      <div
          v-for="n in 15"
          :key="n"
          class="bubble"
          :style="{
          left: Math.random() * 100 + '%',
          animationDuration: 7 + Math.random() * 10 + 's',
          animationDelay: Math.random() * 5 + 's',
          opacity: 0.2 + Math.random() * 0.6,
          transform: 'scale(' + (0.4 + Math.random() * 0.6) + ')',
        }"
      ></div>
    </div>

    <!-- 深度变化效果 -->
    <div class="depth-overlay" :style="{ opacity: depthProgress / 200 }"></div>

    <!-- 光线射线效果 -->
    <div class="light-rays" :style="{ opacity: 1 - depthProgress / 100 }"></div>

    <!-- 内容区域 -->
    <div class="content-wrapper">
      <!-- 首屏 -->
      <section class="hero-section" id="intro">
        <div class="hero-content">
          <h1 class="reveal-text">WaterSight水下视界</h1>
          <p class="reveal-text delay-1">
            探索神秘的海洋世界，发现水下生态奥秘
          </p>
          <div class="hero-features">
            <div class="hero-feature">
              <div class="feature-icon enhance-icon">
                <i class="el-icon-picture-outline"></i>
              </div>
              <span>图像增强</span>
            </div>
            <div class="hero-feature">
              <div class="feature-icon detect-icon">
                <i class="el-icon-data-analysis"></i>
              </div>
              <span>数据集生成</span>
            </div>
            <div class="hero-feature">
              <div class="feature-icon fish-icon">
                <i class="el-icon-aim"></i>
              </div>
              <span>鱼类识别</span>
            </div>
            <div class="hero-feature">
              <div class="feature-icon coral-icon">
                <i class="el-icon-set-up"></i>
              </div>
              <span>珊瑚健康监测</span>
            </div>
          </div>
          <div class="hero-cta">
            <a
                class="primary-btn pulse"
                @click="scrollToSection('enhance', true)"
            >
              开始探索
              <i class="el-icon-arrow-right"></i>
            </a>
          </div>
          <div class="scroll-hint">
            <span>向下滚动了解更多</span>
            <div class="scroll-arrow"></div>
          </div>
        </div>
        <div class="parallax-bg layer-1"></div>
        <div class="parallax-bg layer-2"></div>
        <div class="parallax-bg layer-3"></div>
      </section>

      <!-- 图像增强 -->
      <section class="feature-section depth-1" id="enhance">
        <div class="feature-content">
          <h2 class="section-title reveal-on-scroll">图像增强</h2>
          <div class="feature-layout">
            <div class="feature-container">
              <div
                  class="feature-left"
                  data-section="enhance"
                  data-side="left"
                  :class="{ expand: visibleCards.enhance.left }"
              >
                <div class="intro-block">
                  <h3>功能介绍</h3>
                  <p style = "text-indent:2em;">
                    创新性集成深度学习与传统图像处理两大技术体系的水下图像增强系统。</p>
                  <p style = "text-indent:2em;">标准模式采用端到端深度学习模型，通过注意力机制和多尺度特征融合实现最优增强效果；</p>
                  <p style = "text-indent:2em;margin-bottom: 20px"> 快速模式基于改进的多阶段串联优化，结合暗通道去雾、自适应白平衡等算法提供高效处理。</p>
                  <ul class="feature-list" >
                    <li>
                      双模式技术：深度学习模式效果最优，传统算法模式速度更快
                    </li>
                    <li>全面支持：支持图片和视频文件的增强处理</li>
                    <li>预览功能：处理效果可视化对比</li>
                    <li>色彩还原：修复水下色偏，恢复真实色彩</li>
                  </ul>
                </div>
              </div>
              <div
                  class="feature-right"
                  data-section="enhance"
                  data-side="right"
                  :class="{ expand: visibleCards.enhance.right }"
              >
                <div class="advantage-block">
                  <h3>技术优势</h3>
                  <ul class="advantage-list">
                    <li>
                      <span class="advantage-title">深度学习驱动</span>
                      <p>
                        采用端到端深度学习模型，通过注意力机制和多尺度特征融合实现最优增强效果
                      </p>
                    </li>
                    <li>
                      <span class="advantage-title">双模式处理架构</span>
                      <p>标准模式与快速模式可灵活切换，平衡处理效果与速度</p>
                    </li>
                    <li>
                      <span class="advantage-title">水下专业优化</span>
                      <p>针对水下图像模糊问题，采用专门的算法模型优化</p>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="parallax-bg section-bg enhance-bg"></div>
      </section>

      <!-- 水下模拟数据集 -->
      <section class="feature-section depth-2" id="detect">
        <div class="feature-content">
          <h2 class="section-title reveal-on-scroll">水下模拟数据集生成</h2>
          <div class="feature-layout">
            <div class="feature-container">
              <div
                  class="feature-left"
                  data-section="detect"
                  data-side="left"
                  :class="{ expand: visibleCards.detect.left }"
              >
                <div class="intro-block">
                  <h3>功能介绍</h3>
                  <p style="text-indent:2em;">
                    专为水下计算机视觉研究设计的数据集生成工具。基于深度学习的图像转换技术，可将普通图片精确模拟转换为不同水深环境下的图像效果，为水下目标检测、图像增强等研究提供高质量的训练数据集。
                  </p>
                  <ul class="feature-list">
                    <li>双环境模拟：支持深水/浅水环境的精确模拟</li>
                    <li>批量处理：支持大规模数据集的批量转换</li>
                    <li>保真度高：准确还原水下成像物理特性</li>
                    <li>效果预览：可查看单张图片的模拟效果</li>
                  </ul>
                  <div class="guide-section">
                    <h4>特色功能</h4>
                    <ul>
                      <li>陆上图像降质模拟水下图像</li>
                      <li>多环境参数控制</li>
                      <li>支持深水与浅水环境模拟</li>
                      <li>高精度光学物理模型</li>
                    </ul>
                  </div>
                </div>
              </div>
              <div
                  class="feature-right"
                  data-section="detect"
                  data-side="right"
                  :class="{ expand: visibleCards.detect.right }"
              >
                <div class="advantage-block">
                  <h3>技术优势</h3>
                  <ul class="advantage-list">
                    <li style="margin-bottom: 20px">
                      <span class="advantage-title">物理模型驱动</span>
                      <p>基于水下光学传播模型，精确模拟水下成像衰减特性</p>
                    </li>
                    <li style="margin-bottom: 20px">
                      <span class="advantage-title">场景适应性强</span>
                      <p>适用于各类场景图片，支持不同深度的模拟</p>
                    </li>
                    <li style="margin-bottom: 20px">
                      <span class="advantage-title">降质效果真实</span>
                      <p>
                        通过大量真实水下图像训练，生成效果与实际水下拍摄高度相似
                      </p>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="parallax-bg section-bg detect-bg"></div>
      </section>

      <!-- 鱼类识别 -->
      <section class="feature-section depth-3" id="fish">
        <div class="feature-content">
          <h2 class="section-title reveal-on-scroll">鱼类识别</h2>
          <div class="feature-layout">
            <div class="feature-container">
              <div
                  class="feature-left"
                  data-section="fish"
                  data-side="left"
                  :class="{ expand: visibleCards.fish.left }"
              >
                <div class="intro-block">
                  <h3>功能介绍</h3>
                  <p style="text-indent:2em;">
                    基于改进YOLOv5的水下鱼类智能识别系统，专门针对水下环境下的鱼类识别进行优化，支持13种常见观赏鱼类的实时精确识别。</p>
                  <ul class="feature-list">
                    <li>多目标检测：同时识别多个鱼类目标</li>
                    <li>鱼种百科：集成13种常见观赏鱼类的基本信息</li>
                    <li>场景适应：可在不同水下环境和光照条件识别</li>
                    <li>结果导出：支持检测结果图片一键保存与分享</li>
                  </ul>
                </div>
              </div>
              <div
                  class="feature-right"
                  data-section="fish"
                  data-side="right"
                  :class="{ expand: visibleCards.fish.right }"
              >
                <div class="advantage-block">
                  <h3>技术优势</h3>
                  <ul class="advantage-list">
                    <li>
                      <span class="advantage-title">高精度识别</span>
                      <p>
                        针对13种观赏鱼类，识别准确率达95%以上，支持复杂场景的多目标检测
                      </p>
                    </li>
                    <li style="margin-bottom: 20px">
                      <span class="advantage-title">处理速度快</span>
                      <p>
                        采用改进YOLOv5架构,实现快速地的检测响应<!-- ，实现毫秒级的检测响应，支持实时视频分析 -->
                      </p>
                    </li>
                    <li>
                      <span class="advantage-title">水下场景适应</span>
                      <p>通过特殊的预处理和数据增强技术，有效应对水下光照变化和模糊问题</p>
                    </li>
                    <li>
                      <span class="advantage-title">专业知识库</span>
                      <p>整合专业的鱼类生态资料，提供科学的饲养建议</p>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="parallax-bg section-bg fish-bg"></div>
      </section>

      <!-- 珊瑚识别 -->
      <section class="feature-section depth-4" id="coral">
        <div class="feature-content">
          <h2 class="section-title reveal-on-scroll">珊瑚礁健康监测</h2>
          <div class="feature-layout">
            <div class="feature-container">
              <div
                  class="feature-left"
                  data-section="coral"
                  data-side="left"
                  :class="{ expand: visibleCards.coral.left }"
              >
                <div class="intro-block">
                  <h3>功能介绍</h3>
                  <p>
                    基于改进YOLOv5的水下珊瑚礁监测系统，专注于珊瑚礁上的海星识别和生态威胁评估。系统可对棘冠海星等威胁生物进行智能预警，为珊瑚礁保护提供科技支持。
                  </p>
                  <ul class="feature-list">
                    <li>威胁检测：自动识别棘冠海星等危害生物</li>
                    <li>位置识别：精准检测珊瑚礁表面海星的分布位置与密度</li>
                    <li>健康评估：对珊瑚礁受侵害程度进行监测</li>
                    <li>保卫环境：为及时开展海星清除工作提供支持</li>
                  </ul>
                </div>
                <div class="intro-block">
                  <h3>应用场景</h3>
                  <ul class="feature-list">
                    <li>珊瑚礁保护区监测</li>
                    <li>海洋生态研究</li>
                    <li>珊瑚养殖管理</li>
                    <li>海洋保护教育</li>
                  </ul>
                </div>
              </div>
              <div
                  class="feature-right"
                  data-section="coral"
                  data-side="right"
                  :class="{ expand: visibleCards.coral.right }"
              >
                <div class="advantage-block">
                  <h3>技术优势</h3>
                  <ul
                      class="advantage-list"
                      style="display: inline-block !important"
                  >
                    <li style="margin-bottom: 30px">
                      <span class="advantage-title">精确识别</span>
                      <p>基于YOLOv5的目标识别,准确率达90%以上</p>
                    </li>
                    <li style="margin-bottom: 30px">
                      <span class="advantage-title">智能预警</span>
                      <p>自动检测棘冠海星等危害生物，及时预警</p>
                    </li>
                    <li style="margin-bottom: 20px">
                      <span class="advantage-title">优化处理</span>
                      <p>显示海星数量统计，提供分布区域可视化展示</p>
                    </li>
                    <li style="margin-bottom: 20px">
                      <span class="advantage-title">环境适应</span>
                      <p>适应不同水下光照和能见度条件下的海星识别</p>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="parallax-bg section-bg coral-bg"></div>
      </section>

      <!-- 论坛社区 -->
      <section class="feature-section depth-5" id="forum">
        <div class="feature-content">
          <h2 class="section-title reveal-on-scroll">水下视界论坛</h2>
          <div class="feature-layout">
            <div class="feature-container forum-container">
              <div class="feature-left" data-section="forum" data-side="left">
                <div class="intro-block forum-intro">
                  <h3>社区介绍</h3>
                  <p style="text-indent:2em;">
                    水下视界论坛是汇聚海洋爱好者、专业科研人员和水下摄影师的综合社区平台，
                    致力于探索水下世界奥秘、分享专业知识和促进海洋保护意识。论坛以精美的水下风格界面和丰富的互动功能，
                    为用户提供沉浸式的社区体验。
                  </p>
                </div>
                <div class="usage-guide">
                  <h3>社区功能</h3>
                  <ul class="feature-list forum-features">
                    <li><i class="el-icon-chat-dot-square"></i> 多元化话题讨论</li>
                    <li><i class="el-icon-date"></i> 专题活动与线上讲座</li>
                    <li><i class="el-icon-document"></i> 水下资源共享中心</li>
                    <li><i class="el-icon-message"></i> 智能消息通知系统</li>
                    <li><i class="el-icon-star-on"></i> 个性化收藏与点赞</li>
                    <li><i class="el-icon-sunrise"></i> 日夜模式无缝切换</li>
                  </ul>
                </div>
              </div>
              <div class="feature-right" data-section="forum" data-side="right">
                <div class="advantage-block forum-sections">
                  <h3>版块精选</h3>
                  <div class="section-grid">
                    <div class="forum-section">
                      <div class="section-icon"><i class="el-icon-cpu"></i></div>
                      <h4>技术交流</h4>
                      <p>分享水下成像与智能处理技术</p>
                    </div>
                    <div class="forum-section">
                      <div class="section-icon"><i class="el-icon-picture-outline"></i></div>
                      <h4>摄影展示</h4>
                      <p>展示精美水下摄影作品与心得</p>
                    </div>
                    <div class="forum-section">
                      <div class="section-icon"><i class="el-icon-data-analysis"></i></div>
                      <h4>学术研讨</h4>
                      <p>专业研究者的前沿科研交流</p>
                    </div>
                    <div class="forum-section">
                      <div class="section-icon"><i class="el-icon-discover"></i></div>
                      <h4>探索活动</h4>
                      <p>水下探险、潜水体验活动组织</p>
                    </div>
                    <div class="forum-section">
                      <div class="section-icon"><i class="el-icon-collection"></i></div>
                      <h4>珊瑚保护</h4>
                      <p>珊瑚礁生态保护与研究专区</p>
                    </div>
                    <div class="forum-section">
                      <div class="section-icon"><i class="el-icon-ship"></i></div>
                      <h4>初学者指南</h4>
                      <p>水下摄影与海洋知识入门</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="parallax-bg section-bg forum-bg"></div>
      </section>

      <!-- 用户角色 -->
      <section class="feature-section depth-6" id="roles">
        <div class="feature-content">
          <h2 class="section-title reveal-on-scroll">用户角色体系</h2>
          <p class="section-subtitle">为不同需求的用户提供专属海洋探索体验</p>
          <div class="roles-container">
            <div class="role-cards">
              <div class="role-card researcher">
                <div class="role-header">
                  <div class="role-icon professional"></div>
                  <div class="role-title">
                    <h4>科研人员</h4>
                    <p>专业海洋研究与学术应用</p>
                  </div>
                </div>
                <div class="role-badge">研究专用版</div>
                <div class="wave-decoration"></div>
                <div class="role-description">
                  <p>面向海洋科研工作者、学术机构和专业研究人员设计的专业版本，提供全面的研究工具与学术交流环境。</p>
                </div>
                <div class="role-features">
                  <div class="feature-group">
                    <h5><i class="el-icon-data-line"></i>数据处理</h5>
                    <ul>
                      <li>高精度水下图像增强与降噪</li>
                      <li>水下模拟数据集生成系统</li>
                    </ul>
                  </div>
                  <div class="feature-group">
                    <h5><i class="el-icon-aim"></i>监测识别</h5>
                    <ul>
                      <li>珊瑚礁健康评估系统</li>
                      <li>海星清除目标识别技术</li>
                    </ul>
                  </div>
                  <div class="feature-group">
                    <h5><i class="el-icon-s-cooperation"></i>专业交流</h5>
                    <ul>
                      <li>学术专区与研讨论坛</li>
                      <li>海洋学术资源库访问</li>
                    </ul>
                  </div>
                </div>
              </div>
              <div class="role-card hobbyist">
                <div class="role-header">
                  <div class="role-icon hobbyist-icon"></div>
                  <div class="role-title">
                    <h4>业余爱好者</h4>
                    <p>探索水下世界的休闲体验</p>
                  </div>
                </div>
                <div class="role-badge">探索娱乐版</div>
                <div class="wave-decoration"></div>
                <div class="role-description">
                  <p>为水下摄影爱好者、潜水爱好者和海洋生态感兴趣的用户打造的友好版本，注重简易操作与美观展示。</p>
                </div>
                <div class="role-features">
                  <div class="feature-group">
                    <h5><i class="el-icon-picture"></i>影像处理</h5>
                    <ul>
                      <li>一键式水下图像美化工具</li>
                      <li>直观易用的操作界面</li>
                    </ul>
                  </div>
                  <div class="feature-group">
                    <h5><i class="el-icon-view"></i>识别探索</h5>
                    <ul>
                      <li>常见观赏鱼类轻松识别</li>
                      <li>海洋生物科普百科</li>
                    </ul>
                  </div>
                  <div class="feature-group">
                    <h5><i class="el-icon-chat-line-square"></i>社区互动</h5>
                    <ul>
                      <li>水下摄影作品展示与交流</li>
                      <li>多种体验活动参与</li>
                      <li>社区论坛多主题讨论</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="parallax-bg section-bg roles-bg"></div>
      </section>

      <!-- 关于我们 -->
      <section class="about-section depth-7" id="about">
        <div class="dark-overlay"></div>
        <div class="about-content">
          <h2 class="section-title reveal-on-scroll">关于我们</h2>
          <div class="about-card-container">
            <div class="about-card">
              <div class="team-header">
                <div class="team-logo"></div>
                <div class="team-title">
                  <h3>视界潜航团队</h3>
                  <p>致力于海洋生态保护技术创新</p>
                </div>
              </div>
              <div class="team-description">
                我们致力于研究水下视觉智能技术，并致力于为水下探索提供技术支持。
              </div>
              <div class="achievements-grid">
                <div class="achievement-item">
                  <div class="achievement-icon patent"></div>
                  <span style="font-size: 1rem !important">水下图像增强</span>
                </div>
                <div class="achievement-item">
                  <div class="achievement-icon algorithm"></div>
                  <span style="font-size: 1rem !important">水下目标检测</span>
                </div>
                <div class="achievement-item">
                  <div class="achievement-icon system"></div>
                  <span style="font-size: 1rem !important">海洋生物识别</span>
                </div>
                <div class="achievement-item">
                  <div class="achievement-icon solution"></div>
                  <span style="font-size: 1rem !important">珊瑚健康监测</span>
                </div>
              </div>
            </div>

            <div class="contact-card">
              <div class="join-us">
                <h4>前往探索</h4>
                <p>
                  从郑和下西洋的浩浩荡荡，到现代潜水器挺进万米深海<br />
                  人类探索海洋的脚步从未停歇<br />
                  在这里，让我们一同踏入虚拟水域<br />
                  触碰历史与科技交织的海洋脉搏<br />
                </p>
                <el-button
                    type="primary"
                    @click="handleLogin"
                    class="login-button"
                >立即登录探索</el-button
                >
              </div>
            </div>
          </div>
        </div>
        <div class="parallax-bg section-bg about-bg"></div>
      </section>
    </div>

    <!-- 添加滚动到底部按钮 -->
    <transition name="fade">
      <div
          v-show="showScrollBottom"
          class="scroll-to-bottom"
          @click="scrollToBottom"
      >
        <i class="el-icon-arrow-down"></i>
      </div>
    </transition>

    <!-- 添加返回顶部按钮 -->
    <!--    <transition name="fade">-->
    <!--      <div v-show="showBackTop" class="back-to-top" @click="scrollToTop">-->
    <!--        <i class="el-icon-arrow-up"></i>-->
    <!--      </div>-->
    <!--    </transition>-->
  </div>
</template>

<script>
export default {
  name: "ProfessionHome",
  data() {
    return {
      visibleCards: {
        enhance: { left: false, right: false },
        detect: { left: false, right: false },
        fish: { left: false, right: false },
        coral: { left: false, right: false },
      },
      showBackTop: false,
      showScrollBottom: false,
      scrollPosition: 0,
      depthProgress: 0,
      submarinePosition: 10, // 初始位置，顶部10%
      activeMarker: null, // 当前活动的标记点
      lightsOn: true, // 潜艇灯光状态
      depthMarkers: [
        {
          label: "首页",
          position: 0,
          threshold: 0,
          target: "intro",
          depth: "0米",
        },
        {
          label: "图像增强",
          position: 14,
          threshold: 14,
          target: "enhance",
          depth: "50米",
        },
        {
          label: "数据集生成",
          position: 28,
          threshold: 28,
          target: "detect",
          depth: "100米",
        },
        {
          label: "鱼类识别",
          position: 42,
          threshold: 42,
          target: "fish",
          depth: "200米",
        },
        {
          label: "珊瑚健康监测",
          position: 56,
          threshold: 56,
          target: "coral",
          depth: "300米",
        },
        {
          label: "论坛社区",
          position: 70,
          threshold: 70,
          target: "forum",
          depth: "400米",
        },
        {
          label: "用户角色",
          position: 85,
          threshold: 85,
          target: "roles",
          depth: "500米",
        },
        {
          label: "关于我们",
          position: 100,
          threshold: 100,
          target: "about",
          depth: "600米",
        },
      ],
      animationFrameId: null,
      revealElements: [],
    };
  },
  mounted() {
    window.addEventListener("scroll", this.handleScroll);
    window.addEventListener("scroll", this.handleParallax);

    // 初始化视差效果
    this.initParallax();

    // 初始化滚动显示元素
    this.initRevealElements();

    // 启动深度指示器和潜艇动画
    this.animateSubmarine();

    // 添加滚动事件监听，用于触发元素动画
    this.addScrollObserver();
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.handleScroll);
    window.removeEventListener("scroll", this.handleParallax);

    // 清除动画请求
    if (this.animationFrameId) {
      window.cancelAnimationFrame(this.animationFrameId);
    }
  },
  methods: {
    // 导航到对应的功能页面
    navigateToFeature(feature) {
      const routes = {
        enhance: "/profession/enhance",
        detect: "/profession/datasetPreprocessing",
        fish: "/profession/fishyolo",
        coral: "/profession/coralyolo",
        forum: "/forum",
      };

      if (routes[feature]) {
        this.$router.push(routes[feature]);
      }
    },
    // 处理登录按钮
    handleLogin() {
      this.$router.push("/login");
    },
    // 处理滚动事件
    handleScroll() {
      const scrollTop =
          window.pageYOffset || document.documentElement.scrollTop;
      const scrollHeight = document.documentElement.scrollHeight;
      const clientHeight = document.documentElement.clientHeight;

      // 计算滚动百分比
      this.scrollPosition = (scrollTop / (scrollHeight - clientHeight)) * 100;

      // 更新深度进度条
      this.depthProgress = Math.min(100, Math.max(0, this.scrollPosition));

      // 显示返回顶部按钮
      this.showBackTop = scrollTop > 300;

      // 显示滚动到底部按钮
      this.showScrollBottom =
          scrollTop < scrollHeight - clientHeight - 200 &&
          scrollHeight > clientHeight * 1.5;

      // 控制潜艇灯光
      this.lightsOn = this.scrollPosition < 50;

      // 更新当前活动的标记点
      this.updateActiveMarker();
    },
    // 更新活动标记点
    updateActiveMarker() {
      const sections = [
        "intro",
        "enhance",
        "detect",
        "fish",
        "coral",
        "forum",
        "roles",
        "about",
      ];
      let currentSection = null;

      for (const section of sections) {
        const element = document.getElementById(section);
        if (element) {
          const rect = element.getBoundingClientRect();
          if (
              rect.top <= window.innerHeight / 2 &&
              rect.bottom >= window.innerHeight / 2
          ) {
            currentSection = section;
            break;
          }
        }
      }

      this.activeMarker = currentSection;
    },
    // 滚动到顶部
    scrollToTop() {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    },
    // 滚动到底部
    scrollToBottom() {
      window.scrollTo({
        top: document.documentElement.scrollHeight,
        behavior: "smooth",
      });
    },
    // 初始化视差效果
    initParallax() {
      this.handleParallax();
    },
    // 处理视差滚动效果
    handleParallax() {
      const scrollTop =
          window.pageYOffset || document.documentElement.scrollTop;

      // 为每个视差背景层应用不同速度的位移
      document.querySelectorAll(".parallax-bg").forEach((bg, index) => {
        const speed = 0.5 - index * 0.1; // 每层不同速度
        const yPos = -(scrollTop * speed);
        bg.style.transform = "translate3d(0, " + yPos + "px, 0)";
      });

      // 为每个功能部分添加视差效果
      document
          .querySelectorAll(".feature-section")
          .forEach((section, index) => {
            const rect = section.getBoundingClientRect();
            const windowHeight = window.innerHeight;

            if (rect.top < windowHeight && rect.bottom > 0) {
              const progress = 1 - rect.top / windowHeight;
              const section_bg = section.querySelector(".section-bg");
              if (section_bg) {
                section_bg.style.transform = `translate3d(0, ${
                    progress * 20
                }px, 0)`;
                section_bg.style.opacity = 0.2 + progress * 0.2;
              }
            }
          });
    },
    // 潜艇动画
    animateSubmarine() {
      const scrolled = window.pageYOffset;
      const windowHeight = window.innerHeight;
      const docHeight = document.documentElement.scrollHeight;

      // 计算滚动百分比
      const scrollPercent = (scrolled / (docHeight - windowHeight)) * 100;

      // 计算潜艇位置（从10%到90%）
      const submarinePosition = Math.min(90, Math.max(10, scrollPercent));

      // 平滑更新潜艇位置
      this.submarinePosition = submarinePosition;

      // 根据深度控制灯光
      this.lightsOn = submarinePosition < 50;

      // 继续动画循环
      this.animationFrameId = requestAnimationFrame(this.animateSubmarine);
    },
    // 初始化滚动显示元素
    initRevealElements() {
      this.revealElements = document.querySelectorAll(".reveal-on-scroll");
      this.checkRevealElements();
    },
    // 检查并触发元素显示动画
    checkRevealElements() {
      const windowHeight = window.innerHeight;

      this.revealElements.forEach((el) => {
        const elTop = el.getBoundingClientRect().top;
        const elVisible = 150; // 显示触发点

        if (elTop < windowHeight - elVisible) {
          el.classList.add("active");
        }
      });
    },
    // 添加滚动观察器
    addScrollObserver() {
      if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            (entries) => {
              entries.forEach((entry) => {
                if (entry.isIntersecting) {
                  entry.target.classList.add("in-view");
                } else {
                  entry.target.classList.remove("in-view");
                }
              });
            },
            {
              threshold: 0.1,
            }
        );

        // 为功能卡片添加观察
        document
            .querySelectorAll(
                ".feature-left, .feature-right, .role-card, .about-card, .contact-card"
            )
            .forEach((el) => {
              observer.observe(el);
              // 添加初始化类
              el.classList.add("scroll-animate");
            });
      }
    },
    // 滚动到指定部分
    scrollToSection(target, isClicked = false) {
      const element = document.getElementById(target);
      if (element) {
        const offset = element.offsetTop;

        window.scrollTo({
          top: offset,
          behavior: "smooth",
        });

        if (isClicked) {
          this.activeMarker = target;
          setTimeout(() => {
            this.activeMarker = null;
          }, 1000);
        }
      }
    },
  },
};
</script>

<style lang="less" scoped>
.home-container {
  min-height: 100vh;
  background: url("@/assets/imgs/leader1.png") no-repeat center center fixed;
  background-size: cover;
  position: relative;
  scroll-behavior: smooth;
  overflow: hidden; /* 防止水平滚动 */
}

/* 修改内容包装器样式 */
.content-wrapper {
  width: 100%;
  min-height: 100vh;
  position: relative;
  z-index: 2;
  overflow: visible; /* 移除内部滚动条 */
}

/* 修改深度指示器样式 */
.depth-indicator {
  position: fixed; /* 改回fixed，但调整其容器结构 */
  left: 30px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1000;
  width: 4px;
  height: 70vh;
  padding: 15px 40px 15px 10px;
  pointer-events: none; /* 防止干扰点击 */
}

.depth-bar {
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.15);
  position: relative;
  border-radius: 4px;
  box-shadow: 0 0 15px rgba(0, 198, 255, 0.2);
  pointer-events: auto; /* 恢复点击 */
}

.depth-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background: linear-gradient(to top, #00c6ff, #0072ff);
  border-radius: 4px;
  box-shadow: 0 0 20px rgba(0, 198, 255, 0.5);
  transition: height 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.depth-marker {
  position: absolute;
  left: 2px;
  width: 24px;
  height: 24px;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  transform: translateX(-50%);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1001;
  pointer-events: auto; /* 恢复点击 */
}

.depth-marker::after {
  content: "";
  width: 8px;
  height: 8px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  transition: all 0.3s ease;
}

.depth-marker:hover {
  background: rgba(0, 198, 255, 0.2);
  transform: translateX(-50%) scale(1.2);
  border-color: rgba(0, 198, 255, 0.8);
  box-shadow: 0 0 20px rgba(0, 198, 255, 0.6);
}

.depth-marker.active {
  background: rgba(0, 198, 255, 0.3);
  border-color: #00c6ff;
  box-shadow: 0 0 25px rgba(0, 198, 255, 0.8);
}

.depth-marker.active::after {
  background: #00c6ff;
  box-shadow: 0 0 10px rgba(0, 198, 255, 0.8);
}

/* 修改标记点和标签样式 */
.marker-label {
  position: absolute;
  left: 30px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0;
  transform: translateX(-10px);
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
  white-space: nowrap;
  pointer-events: none;
  display: flex;
  flex-direction: column;
}

.depth-marker-hint {
  color: #ffffff; /* 改为白色 */
  font-size: 10px; /* 调小字体 */
  font-weight: 400;
  margin-top: 2px; /* 添加间距 */
  opacity: 0.8;
}

.depth-marker:hover .marker-label,
.depth-marker.active .marker-label {
  opacity: 1;
  transform: translateX(0);
  color: #ffffff;
  text-shadow: 0 0 8px rgba(0, 198, 255, 0.5);
}

/* 首屏样式优化 */
.hero-section {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  position: relative;
  overflow: hidden;
  background: radial-gradient(
      ellipse at center,
      rgba(0, 60, 120, 0.2) 0%,
      rgba(0, 30, 60, 0.5) 100%
  );
}

.hero-content {
  color: white;
  z-index: 10;
  padding: 0 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-content h1 {
  font-size: 5rem;
  margin-bottom: 20px;
  text-shadow: 0 2px 15px rgba(0, 198, 255, 0.8);
  background: linear-gradient(45deg, #ffffff, #00c6ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 2px;
  animation: fadeInUp 1s ease-out forwards;
}

.hero-content p {
  font-size: 1.8rem;
  margin-bottom: 40px;
  color: rgba(255, 255, 255, 0.9);
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
  animation: fadeInUp 1s ease-out 0.3s forwards;
  opacity: 0;
}

.hero-features {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-bottom: 50px;
  opacity: 0;
  animation: fadeInUp 1s ease-out 0.6s forwards;
}

.hero-feature {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  transition: all 0.3s ease;
}

.hero-feature:hover {
  transform: translateY(-8px);
}

.feature-icon {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(0, 198, 255, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 20px rgba(0, 198, 255, 0.3);
  transition: all 0.3s ease;
}

.feature-icon i {
  font-size: 30px;
  color: #00c6ff;
}

.hero-feature:hover .feature-icon {
  background: rgba(0, 198, 255, 0.2);
  border-color: rgba(0, 198, 255, 0.8);
  box-shadow: 0 0 30px rgba(0, 198, 255, 0.5);
}

.enhance-icon {
  background: linear-gradient(
      135deg,
      rgba(0, 198, 255, 0.3),
      rgba(0, 114, 255, 0.3)
  );
}

.detect-icon {
  background: linear-gradient(
      135deg,
      rgba(0, 150, 255, 0.3),
      rgba(0, 80, 200, 0.3)
  );
}

.fish-icon {
  background: linear-gradient(
      135deg,
      rgba(0, 120, 255, 0.3),
      rgba(0, 60, 180, 0.3)
  );
}

.coral-icon {
  background: linear-gradient(
      135deg,
      rgba(0, 90, 230, 0.3),
      rgba(0, 40, 150, 0.3)
  );
}

.hero-feature span {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.1rem;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.hero-cta {
  margin-top: 20px;
  opacity: 0;
  animation: fadeInUp 1s ease-out 0.9s forwards;
}

.primary-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 30px;
  background: linear-gradient(45deg, #0072ff, #00c6ff);
  color: white;
  border: none;
  border-radius: 30px;
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 10px 20px rgba(0, 114, 255, 0.3);
  transition: all 0.3s ease;
  text-decoration: none;
}

.primary-btn:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 114, 255, 0.4);
}

.pulse {
  animation: pulse 2s infinite;
}

/* 深度变化覆盖层优化 - 更强的渐变效果模拟水下光照 */
.depth-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
      to bottom,
      rgba(0, 50, 100, 0.2) 0%,
      rgba(0, 40, 90, 0.3) 20%,
      rgba(0, 30, 80, 0.4) 40%,
      rgba(0, 20, 70, 0.5) 60%,
      rgba(0, 10, 60, 0.6) 80%,
      rgba(0, 5, 50, 0.7) 100%
  );
  pointer-events: none;
  z-index: 2;
  transition: opacity 0.8s ease;
}

/* 光线射线效果增强 */
.light-rays {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(
      ellipse at 50% 0%,
      rgba(255, 255, 255, 0.3) 0%,
      transparent 70%
  ),
  radial-gradient(
      ellipse at 30% 10%,
      rgba(173, 216, 230, 0.3) 0%,
      transparent 70%
  ),
  radial-gradient(
      ellipse at 70% 5%,
      rgba(173, 216, 230, 0.25) 0%,
      transparent 70%
  );
  pointer-events: none;
  z-index: 4;
  transition: opacity 1s ease;
  animation: lightPulsate 8s infinite alternate;
}

@keyframes lightPulsate {
  0% {
    opacity: 0.8;
  }
  100% {
    opacity: 1;
  }
}

/* 功能部分样式改进 - 适应不同深度的背景 */
.feature-section {
  position: relative;
  min-height: 100vh;
  width: 100%;
  //display: flex;
  align-items: center;
  justify-content: center;
  //padding: 20px;
  box-sizing: border-box;
  overflow: visible;
  // margin-top: -80px; /* 整体向上移动 */
}

.feature-section::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
}

/* 为每个深度级别设置不同的背景透明度，模拟下潜效果 */
.depth-1::before {
  background-color: rgba(0, 60, 120, 0.6);
}

.depth-2::before {
  background-color: rgba(0, 55, 110, 0.65);
}

.depth-3::before {
  background-color: rgba(0, 50, 100, 0.7);
}

.depth-4::before {
  background-color: rgba(0, 45, 90, 0.75);
}

.depth-5::before {
  background-color: rgba(0, 40, 80, 0.8);
}

.depth-6::before {
  background-color: rgba(0, 35, 70, 0.85);
}

.depth-7::before {
  background-color: rgba(0, 30, 60, 0.9);
}

/* 调整功能内容容器 */
.feature-content {
  width: 75vw;
  height: 70vh;
  margin: 0 auto;
  position: relative;
}

/* 修复功能容器布局 */
.feature-container {
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  padding: 15px;
}

.feature-layout {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* 调整功能卡片大小和样式 */
.feature-left,
.feature-right {
  background: rgba(0, 30, 60, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(0, 198, 255, 0.2);
  padding: 15px;
  height: 100%;
  overflow: auto;

  /* 自定义滚动条样式 */
  &::-webkit-scrollbar {
    width: 4px;
  }

  &::-webkit-scrollbar-track {
    background: rgba(0, 40, 80, 0.3);
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(0, 198, 255, 0.3);
    border-radius: 2px;
  }
}

.feature-left:hover,
.feature-right:hover {
  transform: translateY(-5px);
  border-color: rgba(0, 198, 255, 0.4);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), 0 0 25px rgba(0, 198, 255, 0.15);
}

/* 移除所有滚动条相关样式 */
.feature-left::-webkit-scrollbar,
.feature-right::-webkit-scrollbar,
.feature-left::-webkit-scrollbar-track,
.feature-right::-webkit-scrollbar-track,
.feature-left::-webkit-scrollbar-thumb,
.feature-right::-webkit-scrollbar-thumb {
  display: none;
}

/* 移除页面朦胧白光效果 */
.light-rays {
  display: none;
}

/* 确保内容区域的文字可见 */
.intro-block,
.advantage-block,
.usage-guide {
  background: rgba(0, 40, 80, 0.3);
  border-radius: 16px;
  padding: 25px;
  height: 100%;
  margin-bottom: 30px;
  border: 1px solid rgba(0, 198, 255, 0.15);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  text-align: left;
  color: #ffffff;
}

/* 改进标题样式 */
.intro-block h3,
.advantage-block h3,
.usage-guide h3 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: #00c6ff;
  text-shadow: 0 0 10px rgba(0, 198, 255, 0.4);
  position: relative;
  padding-bottom: 10px;
}

.intro-block h3::after,
.advantage-block h3::after,
.usage-guide h3::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #00c6ff, transparent);
  border-radius: 1.5px;
}

/* 增强特性列表的可见性 */
.feature-list,
.advantage-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
  padding-left: 20px;
}

.feature-list li,
.advantage-list li {
  position: relative;
  padding-left: 20px;
  font-size: 1rem;
  list-style: none;
}

.feature-list li::before,
.advantage-list li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #00c6ff;
  font-size: 1.3em;
}

/* 调整section-title以确保可见 */
.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 30px;
  color: #fff;
  text-shadow: 0 0 10px rgba(0, 198, 255, 0.5);
  letter-spacing: 1px;
  text-align: center;
  width: 100%;
}

/* 调整guide-section内容的样式 */
.guide-section h4 {
  color: #00c6ff;
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.guide-section ul,
.guide-section ol {
  padding-left: 20px;
  margin-bottom: 15px;
}

.guide-section li {
  margin-bottom: 8px;
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.85rem;
}

/* 移除潜艇轨道元素 - 通过移除相关的轨道样式代码 */
/* 注意：保留潜艇本身的样式，只移除轨道部分 */

/* 关于我们页面样式优化 */
.about-section {
  position: relative;
  min-height: 100vh;
  height: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  overflow: hidden;
  background: linear-gradient(
      to bottom,
      rgba(0, 10, 30, 0.9),
      rgba(0, 5, 20, 0.95)
  );
}

.about-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: -100px;
  background: radial-gradient(
      ellipse at center,
      rgba(0, 15, 40, 0.8),
      rgba(0, 5, 20, 0.98)
  );
  z-index: 1;
}

.about-content {
  position: relative;
  z-index: 2;
  color: white;
  max-width: 1200px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 30px;
}

.about-card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 40px;
  justify-content: center;
  margin-top: 40px;
  width: 100%;
}

.about-card,
.contact-card {
  background: rgba(0, 25, 50, 0.8);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  border: 1px solid rgba(0, 198, 255, 0.3);
  padding: 35px;
  flex: 1;
  min-width: 300px;
  max-width: 600px;
  transform: translateY(30px);
  opacity: 0;
  animation: cardReveal 0.8s forwards;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(0, 198, 255, 0.2);
  transition: all 0.4s ease;
}

.about-card:hover,
.contact-card:hover {
  border-color: rgba(0, 198, 255, 0.5);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5), 0 0 30px rgba(0, 198, 255, 0.25);
  transform: translateY(-10px);
}

.team-header {
  display: flex;
  align-items: center;
  gap: 25px;
  margin-bottom: 30px;
  border-bottom: 2px solid rgba(0, 198, 255, 0.3);
  padding-bottom: 20px;
}

.team-logo {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: radial-gradient(
      circle,
      rgba(0, 198, 255, 0.4),
      rgba(0, 114, 255, 0.4)
  );
  border: 3px solid rgba(0, 198, 255, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 30px rgba(0, 198, 255, 0.5),
  inset 0 0 15px rgba(255, 255, 255, 0.5);
  position: relative;
  overflow: hidden;
}

.team-logo::after {
  content: "";
  position: absolute;
  width: 150%;
  height: 150%;
  background: linear-gradient(
      45deg,
      transparent,
      rgba(255, 255, 255, 0.3),
      transparent
  );
  transform: rotate(45deg) translateX(-150%);
  animation: shine 3s infinite;
}

@keyframes shine {
  0% {
    transform: rotate(45deg) translateX(-150%);
  }
  50% {
    transform: rotate(45deg) translateX(150%);
  }
  100% {
    transform: rotate(45deg) translateX(150%);
  }
}

.team-title h3 {
  font-size: 1.5rem;
  color: #ffffff;
  margin-bottom: 8px;
  text-shadow: 0 2px 5px rgba(0, 0, 0, 0.5), 0 0 10px rgba(0, 198, 255, 0.3);
  letter-spacing: 1px;
}

.team-title p {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.85);
  font-style: italic;
}

.team-description {
  font-size: 0.8rem;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 20px;
  padding-bottom: 25px;
  border-bottom: 1px solid rgba(0, 198, 255, 0.25);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 25px;
}

.achievement-item {
  display: flex;
  align-items: center;
  gap: 18px;

  background: rgba(0, 40, 80, 0.4);
  padding: 5px;
  border-radius: 12px;
  border: 1px solid rgba(0, 198, 255, 0.2);
  transition: all 0.3s ease;
}

.achievement-item:hover {
  background: rgba(0, 45, 90, 0.5);
  transform: translateY(-5px);
  border-color: rgba(0, 198, 255, 0.4);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3), 0 0 15px rgba(0, 198, 255, 0.15);
}

.achievement-icon {
  width: 55px;
  height: 55px;
  border-radius: 50%;
  background: rgba(0, 114, 255, 0.25);
  border: 2px solid rgba(0, 198, 255, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #00c6ff;
  box-shadow: 0 0 20px rgba(0, 198, 255, 0.3);
}

.contact-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.contact-card h3 {
  font-size: 2.2rem;
  margin-bottom: 35px;
  color: #ffffff;
  text-align: center;
  position: relative;
  padding-bottom: 15px;
  text-shadow: 0 2px 10px rgba(0, 198, 255, 0.4);
}

.contact-card h3::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 3px;
  background: linear-gradient(90deg, transparent, #00c6ff, transparent);
  border-radius: 2px;
}

.contact-list {
  margin-bottom: 35px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-bottom: 20px;
  padding: 18px;
  background: rgba(0, 40, 80, 0.4);
  border-radius: 12px;
  border: 1px solid rgba(0, 198, 255, 0.25);
  transition: all 0.3s ease;
}

.contact-item:hover {
  background: rgba(0, 45, 90, 0.5);
  transform: translateX(8px);
  border-color: rgba(0, 198, 255, 0.4);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2), 0 0 10px rgba(0, 198, 255, 0.15);
}

.contact-item i {
  font-size: 1.8rem;
  color: #00c6ff;
  text-shadow: 0 0 10px rgba(0, 198, 255, 0.5);
}

.contact-item span {
  font-size: 1.1rem;
}

.join-us {
  background: linear-gradient(
      135deg,
      rgba(0, 114, 255, 0.3),
      rgba(0, 198, 255, 0.3)
  );
  padding: 30px;
  width: 100%;
  height: 100%;
  border-radius: 16px;
  text-align: center;
  border: 1px solid rgba(0, 198, 255, 0.4);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3), 0 0 20px rgba(0, 198, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.join-us::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(
      circle at center,
      rgba(0, 198, 255, 0.1),
      transparent 70%
  );
  z-index: -1;
}

.join-us h4 {
  font-size: 1.8rem;
  margin-bottom: 20px;
  color: #ffffff;
  text-shadow: 0 2px 5px rgba(0, 0, 0, 0.4), 0 0 10px rgba(0, 198, 255, 0.3);
}

.join-us p {
  margin-top: 30px;
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.95);
  line-height: 3rem;
}

.login-button {
  background: linear-gradient(45deg, #0072ff, #00c6ff) !important;
  border: none !important;
  padding: 15px 40px !important;
  font-size: 1.25rem !important;
  margin-top: 10%;
  font-weight: 600 !important;
  border-radius: 30px !important;
  box-shadow: 0 10px 25px rgba(0, 114, 255, 0.4),
  0 0 15px rgba(0, 198, 255, 0.3) !important;
  transition: all 0.3s ease !important;
  letter-spacing: 1px !important;
  position: relative !important;
  overflow: hidden !important;
  animation: pulse-button 2s infinite !important;
}

.login-button:hover {
  transform: translateY(-8px) scale(1.05) !important;
  box-shadow: 0 20px 40px rgba(0, 114, 255, 0.5),
  0 0 30px rgba(0, 198, 255, 0.4) !important;
}

.login-button::after {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
      rgba(255, 255, 255, 0),
      rgba(255, 255, 255, 0.2),
      rgba(255, 255, 255, 0)
  );
  transform: rotate(30deg);
  animation: shine-button 3s infinite;
}

@keyframes pulse-button {
  0% {
    box-shadow: 0 0 0 0 rgba(0, 198, 255, 0.4);
  }
  70% {
    box-shadow: 0 0 0 15px rgba(0, 198, 255, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(0, 198, 255, 0);
  }
}

@keyframes shine-button {
  0% {
    left: -100%;
  }
  20%,
  100% {
    left: 100%;
  }
}

/* 视差滚动增强 */
.parallax-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
  pointer-events: none;
}

.layer-1 {
  background: linear-gradient(
      to bottom,
      rgba(0, 80, 160, 0.2),
      rgba(0, 40, 80, 0.3)
  );
  opacity: 0.7;
}

.layer-2 {
  background: radial-gradient(
      circle at 50% 30%,
      rgba(255, 255, 255, 0.4),
      transparent 70%
  );
  opacity: 0.5;
}

.layer-3 {
  background-image: radial-gradient(
      circle at 25% 25%,
      rgba(255, 255, 255, 0.2) 1px,
      transparent 1px
  ),
  radial-gradient(
      circle at 75% 75%,
      rgba(255, 255, 255, 0.2) 1px,
      transparent 1px
  );
  background-size: 100px 100px;
  opacity: 0.3;
}

.section-bg {
  opacity: 0.2;
  background-size: cover;
  background-position: center;
  transition: all 0.8s ease-out;
}

/* 全局美化和增强 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes floating {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(0, 198, 255, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(0, 198, 255, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(0, 198, 255, 0);
  }
}

/* 响应式设计优化 */
@media (max-width: 1200px) {
  .feature-container {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .feature-left,
  .feature-right {
    max-height: calc((100vh - 250px) / 2);
  }

  .feature-content h2 {
    font-size: 2.2rem;
    margin-bottom: 20px;
  }

  .about-card-container {
    flex-direction: column;
    align-items: center;
  }

  .about-card,
  .contact-card {
    min-width: 100%;
  }
}

@media (max-width: 768px) {
  .depth-indicator {
    left: 15px;
  }

  .feature-left,
  .feature-right {
    width: 100%;
    margin-bottom: 20px;
  }

  .submarine {
    right: 20px;
    transform: scale(0.8);
  }
}

/* 恢复功能布局及内容区样式 */
.feature-layout {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  max-height: calc(100vh - 150px);
  width: 100%;
}

.feature-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  height: auto;
  max-height: calc(100vh - 200px);
}

/* 
.intro-block p,
.advantage-block p,
.usage-guide p {
  font-size: 0.85rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 15px;
} */

.feature-list,
.advantage-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-top: 10px;
}

.feature-list li,
.advantage-list li {
  position: relative;
  padding-left: 18px;
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.85);
  line-height: 1.5;
}

.feature-list li::before,
.advantage-list li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #00c6ff;
  font-size: 1.2em;
}

.advantage-title {
  display: block;
  font-size: 1.1rem;
  color: #00c6ff;
  margin-bottom: 8px;
}

/* 恢复功能介绍页结构和段落样式 */
.guide-section {
  margin-bottom: 20px;
}

.guide-section h4 {
  color: #00c6ff;
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.guide-section ul,
.guide-section ol {
  padding-left: 20px;
  margin-bottom: 15px;
}

.guide-section li {
  margin-bottom: 8px;
  color: rgba(255, 255, 255, 0.85);
}

/* 恢复社区部分样式 */
.forum-container,
.roles-container {
  width: 100%;
}

.forum-left,
.forum-right {
  background: rgba(0, 30, 60, 0.7);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  border: 1px solid rgba(0, 198, 255, 0.2);
  padding: 30px;
  max-height: calc(100vh - 300px);
  overflow-y: auto;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  width: 48%;
  opacity: 1;
  transform: translateY(0);
}

.forum-sections h3 {
  font-size: 1.8rem;
  margin-bottom: 20px;
  color: #00c6ff;
}

.section-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.forum-section {
  background: rgba(0, 40, 80, 0.3);
  border-radius: 16px;
  padding: 20px;
  border: 1px solid rgba(0, 198, 255, 0.15);
  transition: all 0.3s ease;
}

.forum-section:hover {
  background: rgba(0, 40, 80, 0.4);
  border-color: rgba(0, 198, 255, 0.3);
  transform: translateY(-5px);
}

.forum-section h4 {
  color: #ffffff;
  font-size: 1.3rem;
  margin-bottom: 10px;
}

.forum-section p {
  color: rgba(255, 255, 255, 0.8);
}

.community-features h3 {
  font-size: 1.8rem;
  margin-bottom: 20px;
  color: #00c6ff;
}

.forum-stats {
  display: flex;
  justify-content: space-around;
  margin-top: 30px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 1.8rem;
  font-weight: bold;
  color: #00c6ff;
  margin-bottom: 5px;
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
}

/* 恢复用户角色部分样式 */
.roles-container {
  padding: 20px 0;
}

.role-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  width: 100%;
}

.role-card {
  background: rgba(0, 30, 60, 0.7);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  border: 1px solid rgba(0, 198, 255, 0.2);
  padding: 30px;

  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
  transition: all 0.4s ease;
}

.role-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 30px rgba(0, 198, 255, 0.15);
}

.role-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.role-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(0, 198, 255, 0.3);
}

.professional {
  background: linear-gradient(
      135deg,
      rgba(0, 120, 255, 0.3),
      rgba(0, 60, 180, 0.3)
  );
}

.hobbyist-icon {
  background: linear-gradient(
      135deg,
      rgba(0, 198, 255, 0.3),
      rgba(0, 114, 255, 0.3)
  );
}

.role-header h4 {
  font-size: 1.6rem;
  color: #ffffff;
  margin-bottom: 5px;
}

.role-header p {
  color: rgba(255, 255, 255, 0.8);
}

.features-list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.feature-item {
  background: rgba(0, 40, 80, 0.3);
  border-radius: 10px;
  padding: 12px 15px;
  border: 1px solid rgba(0, 198, 255, 0.1);
  transition: all 0.3s ease;
}

.feature-item:hover {
  background: rgba(0, 40, 80, 0.4);
  border-color: rgba(0, 198, 255, 0.2);
  transform: translateY(-3px);
}

.feature-item span {
  color: rgba(255, 255, 255, 0.9);
}

/* 潜艇动画样式优化 */
.submarine {
  position: fixed;
  right: 50px;
  width: 80px;
  height: 30px;
  background: linear-gradient(135deg, #05bfdb, #088395);
  border-radius: 10px 15px 5px 10px;
  z-index: 1000;
  transition: top 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
  filter: drop-shadow(0 0 8px rgba(0, 198, 255, 0.6));
  pointer-events: none;
}

.submarine::before {
  content: "";
  position: absolute;
  left: -15px;
  top: 5px;
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, #05bfdb, #088395);
  border-radius: 50% 50% 50% 50% / 100% 100% 0% 0%;
  transform: rotate(-15deg);
}

.submarine::after {
  content: "";
  position: absolute;
  right: -8px;
  top: 12px;
  width: 15px;
  height: 6px;
  background: #0a4d68;
  border-radius: 5px;
}

.submarine-window {
  position: absolute;
  left: 50%;
  top: 8px;
  width: 12px;
  height: 12px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  transform: translateX(-50%);
  border: 2px solid #088395;
  box-shadow: inset 0 0 5px rgba(0, 198, 255, 0.5);
}

.submarine-light {
  position: absolute;
  left: 15px;
  top: 10px;
  width: 100px;
  height: 150px;
  background: radial-gradient(
      ellipse at left center,
      rgba(255, 255, 255, 0.3),
      transparent 70%
  );
  transform: translateY(-50%) rotate(-30deg);
  transform-origin: left top;
  opacity: 0.6;
  z-index: -1;
  transition: opacity 0.8s ease;
}

.submarine-bubbles {
  position: absolute;
  right: -20px;
  top: 10px;
}

.sub-bubble {
  position: absolute;
  width: 8px;
  height: 8px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  animation: sub-bubble-rise 4s linear infinite;
  opacity: 0.8;
}

@keyframes sub-bubble-rise {
  0% {
    transform: translateY(0) translateX(0);
    opacity: 0.8;
  }
  100% {
    transform: translateY(-50px) translateX(-30px);
    opacity: 0;
  }
}

.lights-on .submarine-light {
  opacity: 0.9;
}

.lights-on .submarine-window {
  background: rgba(255, 255, 200, 0.9);
  box-shadow: 0 0 10px rgba(255, 255, 150, 0.5);
}

@keyframes submarine-float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

@keyframes lightPulse {
  0% {
    opacity: 0.5;
    width: 80px;
  }
  100% {
    opacity: 0.8;
    width: 120px;
  }
}

@keyframes sub-bubble-rise {
  0% {
    transform: translateY(0) translateX(0);
    opacity: 0.8;
  }
  100% {
    transform: translateY(-50px) translateX(-30px);
    opacity: 0;
  }
}

@keyframes bubble-emit {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-2px);
  }
}

/* 气泡效果 */
.bubble {
  position: absolute;
  bottom: -20px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: radial-gradient(
      circle at 30% 30%,
      rgba(255, 255, 255, 0.6),
      rgba(255, 255, 255, 0.1)
  );
  animation: bubble-rise linear infinite;
  box-shadow: 0 0 5px rgba(255, 255, 255, 0.2),
  inset 0 0 5px rgba(255, 255, 255, 0.2);
  pointer-events: none;
}

@keyframes bubble-rise {
  0% {
    transform: translateY(0) scale(1) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.8;
  }
  95% {
    opacity: 0.3;
  }
  100% {
    transform: translateY(-100vh) scale(1.3) rotate(20deg);
    opacity: 0;
  }
}

/* 确保标题动画效果 */
@keyframes titleReveal {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes cardReveal {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 自定义滚动条样式 */
.feature-left::-webkit-scrollbar,
.feature-right::-webkit-scrollbar {
  width: 6px;
}

.feature-left::-webkit-scrollbar-track,
.feature-right::-webkit-scrollbar-track {
  background: rgba(0, 30, 60, 0.3);
  border-radius: 3px;
}

.feature-left::-webkit-scrollbar-thumb,
.feature-right::-webkit-scrollbar-thumb {
  background: rgba(0, 198, 255, 0.5);
  border-radius: 3px;
}

.feature-left::-webkit-scrollbar-thumb:hover,
.feature-right::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 198, 255, 0.7);
}

.intro-block,
.advantage-block,
.usage-guide {
  background: rgba(0, 40, 80, 0.3);
  border-radius: 16px;
  padding: 25px;
  margin-bottom: 30px;
  border: 1px solid rgba(0, 198, 255, 0.15);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  text-align: left;
  color: #ffffff;
}

.intro-block:hover,
.advantage-block:hover,
.usage-guide:hover {
  background: rgba(0, 40, 80, 0.4);
  border-color: rgba(0, 198, 255, 0.2);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.2), 0 0 15px rgba(0, 198, 255, 0.1);
}

.intro-block h3,
.advantage-block h3,
.usage-guide h3 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: #00c6ff;
  text-shadow: 0 0 10px rgba(0, 198, 255, 0.4);
  position: relative;
  padding-bottom: 10px;
}

.intro-block h3::after,
.advantage-block h3::after,
.usage-guide h3::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #00c6ff, transparent);
  border-radius: 1.5px;
}

/* 修改feature-left和feature-right的样式，使内容可见 */
.feature-left,
.feature-right {
  background: rgba(0, 30, 60, 0.7);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  border: 1px solid rgba(0, 198, 255, 0.2);
  padding: 25px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  opacity: 1;
  transform: translateY(0);
}

/* 
.intro-block p,
.advantage-block p,
.usage-guide p,
.guide-section p,
.feature-list li,
.advantage-list li {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.85rem;
  line-height: 1.6;
  margin-bottom: 10px;
} */

/* 增强特性列表的可见性 */
.feature-list,
.advantage-list {
  //display: flex;
  //flex-direction: column;
  gap: 10px;
  margin-top: 10px;
  padding-left: 20px;
}

.feature-list li,
.advantage-list li {
  position: relative;
  padding-left: 20px;
  font-size: 1rem;
  list-style: none;
}

.feature-list li::before,
.advantage-list li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #00c6ff;
  font-size: 1.3em;
}

/* 调整section-title以确保可见 */
.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 30px;
  color: #fff;
  text-shadow: 0 0 10px rgba(0, 198, 255, 0.5);
  letter-spacing: 1px;
  text-align: center;
  width: 100%;
}

/* 调整guide-section内容的样式 */
.guide-section h4 {
  color: #00c6ff;
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.guide-section ul,
.guide-section ol {
  padding-left: 20px;
  margin-bottom: 15px;
}

.guide-section li {
  margin-bottom: 8px;
  color: rgba(255, 255, 255, 0.85);
}

/* 清理重复的样式代码并统一卡片样式 */

/* 调整功能容器布局 - 确保内容完整显示 */
.feature-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin: 0 auto;
  color: #fff;
  gap: 20px;
}

/* 设置卡片高度，确保内容完整显示不需要滚动 */
.feature-left,
.feature-right {
  background: rgba(0, 30, 60, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(0, 198, 255, 0.2);
  padding: 15px;
  width: 48%;
  height: auto;
  /* 移除高度限制和滚动条 */
  max-height: none;
  overflow: visible;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3), 0 0 20px rgba(0, 198, 255, 0.1);
}

.feature-left:hover,
.feature-right:hover {
  transform: translateY(-5px);
  border-color: rgba(0, 198, 255, 0.4);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), 0 0 25px rgba(0, 198, 255, 0.15);
}

/* 移除所有滚动条相关样式 */
.feature-left::-webkit-scrollbar,
.feature-right::-webkit-scrollbar,
.feature-left::-webkit-scrollbar-track,
.feature-right::-webkit-scrollbar-track,
.feature-left::-webkit-scrollbar-thumb,
.feature-right::-webkit-scrollbar-thumb {
  display: none;
}

/* 内容块统一样式 */
.intro-block,
.advantage-block,
.usage-guide {
  background: rgba(0, 40, 80, 0.3);
  border-radius: 16px;
  padding: 25px;
  margin-bottom: 25px;
  border: 1px solid rgba(0, 198, 255, 0.15);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  text-align: left;
  color: #ffffff;
}

.intro-block:hover,
.advantage-block:hover,
.usage-guide:hover {
  background: rgba(0, 40, 80, 0.4);
  border-color: rgba(0, 198, 255, 0.3);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.2), 0 0 15px rgba(0, 198, 255, 0.1);
}

/* 统一标题样式 */
.intro-block h3,
.advantage-block h3,
.usage-guide h3 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: #00c6ff;
  text-shadow: 0 0 10px rgba(0, 198, 255, 0.4);
  position: relative;
  padding-bottom: 10px;
}

.intro-block h3::after,
.advantage-block h3::after,
.usage-guide h3::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #00c6ff, transparent);
  border-radius: 1.5px;
}

/* .intro-block p,
.advantage-block p,
.usage-guide p,
.guide-section p,
.feature-list li,
.advantage-list li {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.85rem;
  line-height: 1.6;
  margin-bottom: 10px;
} */

/* 统一列表样式 */
.feature-list,
.advantage-list {
  //display: flex;
  //flex-direction: column;
  gap: 10px;
  margin-top: 10px;
  padding-left: 20px;
}

.feature-list li,
.advantage-list li {
  position: relative;
  padding-left: 20px;
  font-size: 1rem;
  list-style: none;
}

.feature-list li::before,
.advantage-list li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #00c6ff;
  font-size: 1.3em;
}

/* 论坛特殊样式 */
.forum-section {
  background: rgba(0, 40, 80, 0.3);
  border-radius: 12px;
  padding: 15px;
  margin-bottom: 0;
  border: 1px solid rgba(0, 198, 255, 0.15);
  transition: all 0.3s ease;
}

.forum-section:hover {
  background: rgba(0, 40, 80, 0.4);
  border-color: rgba(0, 198, 255, 0.3);
  transform: translateY(-3px);
}

.section-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.forum-stats {
  display: flex;
  justify-content: space-around;
  margin-top: 25px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 1.8rem;
  font-weight: bold;
  color: #00c6ff;
  margin-bottom: 5px;
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
}

/* 设置卡片高度适应内容 */
.feature-layout {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: auto;
  min-height: 70vh;
}

/* 调整section高度，确保内容完全显示 */
.feature-section {
  height: auto;
  min-height: 100vh;
  padding: 40px 0;
}

/* 修复功能容器布局，确保卡片不会溢出 */
.feature-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin: 0 auto;
  color: #fff;
  gap: 30px;
  flex-wrap: wrap; /* 在小屏幕上允许换行 */
}

/* 调整功能卡片大小和样式，防止内容溢出 */
.feature-left,
.feature-right {
  background: rgba(0, 30, 60, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(0, 198, 255, 0.2);
  padding: 15px;
  width: 48%;
  min-height: 400px;
  height: auto;
  overflow: visible;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3), 0 0 20px rgba(0, 198, 255, 0.1);
  display: flex;
  flex-direction: column;
}

/* 确保内容区域的文字可见且不溢出 */
.intro-block,
.advantage-block,
.usage-guide {
  background: rgba(0, 40, 80, 0.3);
  border-radius: 16px;
  padding: 25px;
  margin-bottom: 25px;
  border: 1px solid rgba(0, 198, 255, 0.15);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  text-align: left;
  color: #ffffff;
  width: 100%;
  box-sizing: border-box;
}

/* 防止文本内容溢出 */
.intro-block p,
.advantage-block p,
.usage-guide p,
.guide-section p,
.feature-list li,
.advantage-list li {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 10px;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

/* 用户角色部分样式优化 */
.section-subtitle {
  text-align: center;
  color: rgba(255, 255, 255, 0.85);
  font-size: 18px;
  margin-top: -5px;
  margin-bottom: 20px;
  font-weight: 300;
  letter-spacing: 0.5px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.role-cards {
  display: flex;
  gap: 40px;
  justify-content: center;
  perspective: 1000px;

  .role-card {
    position: relative;
    overflow: hidden;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(15px);
    max-width: 460px;
    width: 100%;
    max-height: 500px;
    transform-style: preserve-3d;
    transition: transform 0.5s ease, box-shadow 0.5s ease;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);

    &:hover {
      transform: translateY(-10px) rotateX(2deg) rotateY(-2deg);
      box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3), 0 10px 20px rgba(5, 191, 219, 0.2);

      .wave-decoration {
        animation-play-state: running;
      }

      .role-badge {
        background: rgba(5, 191, 219, 0.3);
        box-shadow: 0 0 15px rgba(5, 191, 219, 0.5);
      }
    }

    &.researcher {
      border: 1px solid rgba(10, 77, 104, 0.6);
      background: linear-gradient(135deg,
      rgba(10, 77, 104, 0.25) 0%,
      rgba(8, 131, 149, 0.25) 100%
      );

      .role-icon {
        background-color: rgba(10, 77, 104, 0.8);
        background-image: radial-gradient(
            circle at center,
            rgba(8, 131, 149, 0.9),
            rgba(10, 77, 104, 0.9)
        );
      }

      .feature-group h5 i {
        color: #05bfdb;
        text-shadow: 0 0 8px rgba(5, 191, 219, 0.6);
      }
    }

    &.hobbyist {
      border: 1px solid rgba(5, 191, 219, 0.6);
      background: linear-gradient(135deg,
      rgba(8, 131, 149, 0.25) 0%,
      rgba(5, 191, 219, 0.25) 100%
      );

      .role-icon {
        background-color: rgba(8, 131, 149, 0.8);
        background-image: radial-gradient(
            circle at center,
            rgba(5, 191, 219, 0.9),
            rgba(8, 131, 149, 0.9)
        );
      }

      .feature-group h5 i {
        color: #05bfdb;
        text-shadow: 0 0 8px rgba(5, 191, 219, 0.6);
      }
    }
  }

  .role-header {
    padding: 2px 25px 15px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.15);

    .role-icon {
      width: 65px;
      height: 65px;
      border-radius: 50%;
      margin-right: 20px;
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;

      &::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 50%;
        border: 2px solid rgba(255, 255, 255, 0.2);
        box-shadow: inset 0 0 10px rgba(255, 255, 255, 0.3);
      }

      &::after {
        content: "";
        position: absolute;
        top: -5px;
        left: -5px;
        right: -5px;
        bottom: -5px;
        border-radius: 50%;
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: pulse 2s infinite;
      }

      &.professional::before {
        content: "\e911";
        font-family: element-icons !important;
        font-size: 28px;
        color: white;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.6);
      }

      &.hobbyist-icon::before {
        content: "\e90e";
        font-family: element-icons !important;
        font-size: 28px;
        color: white;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.6);
      }
    }

    .role-title {
      h4 {
        margin: 0 0 8px;
        font-size: 22px;
        color: white;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
      }

      p {
        margin: 0;
        color: rgba(255, 255, 255, 0.7);
        font-size: 15px;
      }
    }
  }

  .role-badge {
    position: absolute;
    top: 25px;
    right: 25px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 13px;
    color: white;
    font-weight: 600;
    backdrop-filter: blur(5px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.1);
    letter-spacing: 0.5px;
  }

  .wave-decoration {
    position: absolute;
    top: 75px;
    right: 0;
    width: 100px;
    height: 200px;
    background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 80" preserveAspectRatio="none"><path d="M0,0 Q5,40 10,80 Q15,40 20,0 Z" fill="rgba(255,255,255,0.03)"/></svg>') repeat-x;
    background-size: 20px 80px;
    transform: rotate(90deg);
    z-index: 0;
    opacity: 0.5;
    animation: wave 8s linear infinite;
    animation-play-state: paused;
  }

  .role-description {
    padding: 0px 25px 5px;
    position: relative;
    z-index: 1;

    p {
      color: rgba(255, 255, 255, 0.85);
      font-size: 15px;
      line-height: 1.6;
      margin: 0;
      text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }
  }

  .role-features {
    padding: 3px 25px 25px;
    position: relative;
    z-index: 1;

    .feature-group {
      margin-bottom: 8px;

      h5 {
        display: flex;
        align-items: center;
        font-size: 17px;
        color: white;
        margin: 0 0 12px;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        font-weight: 600;
        letter-spacing: 0.5px;

        i {
          margin-right: 8px;
          font-size: 20px;
        }
      }

      ul {
        margin: 0;
        padding: 0 0 0 20px;
        list-style-type: none;

        li {
          position: relative;
          margin-bottom: 0px;
          color: rgba(255, 255, 255, 0.85);
          font-size: 14.5px;
          line-height: 1.5;
          padding-left: 5px;

          &::before {
            content: "•";
            position: absolute;
            left: -14px;
            color: rgba(5, 191, 219, 0.9);
            font-size: 18px;
            line-height: 1;
          }
        }
      }
    }
  }
}

@keyframes wave {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: -40px 0;
  }
}

@keyframes pulse {
  0% {
    opacity: 0.6;
    transform: scale(0.98);
  }
  50% {
    opacity: 0.3;
    transform: scale(1.05);
  }
  100% {
    opacity: 0.6;
    transform: scale(0.98);
  }
}

/* 媒体查询优化 */
@media (max-width: 1200px) {
  .role-cards {
    padding: 0 20px;

    .role-card {
      max-width: 440px;
    }
  }
}

@media (max-width: 992px) {
  .role-cards {
    flex-direction: column;
    align-items: center;
    gap: 30px;

    .role-card {
      max-width: 90%;
    }
  }
}

@media (max-width: 768px) {
  .section-subtitle {
    font-size: 16px;
    padding: 0 20px;
  }

  .role-cards .role-card {
    max-width: 100%;
  }
}
</style>
