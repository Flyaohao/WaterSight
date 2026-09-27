<div align="center">

# 🌊 水下视界 · WaterSight

**面向水下场景的多模态视觉分析平台**

图像增强 · 模拟数据集生成 · 鱼类识别 · 珊瑚礁健康监测

![Vue](https://img.shields.io/badge/Vue-2.6-4FC08D?logo=vuedotjs&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-2.5.9-6DB33F?logo=springboot&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.4.1-EE4C2C?logo=pytorch&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13-FF6F00?logo=tensorflow&logoColor=white)
![YOLOv5](https://img.shields.io/badge/YOLOv5-6.0-00FFFF?logo=yolo&logoColor=black)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?logo=mysql&logoColor=white)

</div>

---

## 📖 项目简介

水下光学成像受水体吸收与散射影响，图像普遍存在**色偏、低对比度、雾化**等问题，同时真实水下标注数据获取成本极高，严重制约水下视觉算法的研究与应用。

**水下视界**是一套面向水下场景的完整视觉分析平台，围绕「**数据 → 增强 → 识别**」构建闭环：

- 🎨 **水下图像增强** —— 融合暗通道先验、自适应白平衡、CLAHE 等传统算子与深度学习模型，还原水下图像真实色彩与细节
- 🧪 **模拟数据集生成** —— 基于 **pix2pix** 学习真实水下成像退化规律，将陆地清晰图像批量转换为深水 / 浅水两种退化风格，突破水下数据瓶颈
- 🐟 **鱼类识别** —— 基于 **YOLOv5** 的细粒度目标检测，覆盖 12 类常见观赏鱼，并给出置信度与饲养知识
- 🪸 **珊瑚礁健康监测** —— 识别海星等珊瑚礁指示生物，输出生态角色与保护状态

平台采用 **Vue 前端 + SpringBoot 网关 + 三个 Python 算法微服务** 的四端分离架构，具备完整的用户体系、内容社区与后台管理能力。

> 本项目为**软件应用与开发类竞赛参赛作品**，[设计与开发文档](docs/设计开发文档.pdf) · [作品信息摘要](docs/作品信息摘要.pdf)

---

## 🖼 界面预览

<!-- 建议替换为真实截图：将图片放入 screenshots/ 目录后修改下方文件名 -->

| 首页 | 鱼类识别 |
|:---:|:---:|
| ![首页](screenshots/home.png) | ![鱼类识别](screenshots/fish-detection.png) |

| 图像增强 | 模拟数据集生成 |
|:---:|:---:|
| ![图像增强](screenshots/enhance.png) | ![数据集生成](screenshots/dataset-generation.png) |

| 珊瑚礁健康监测 | 后台管理 |
|:---:|:---:|
| ![珊瑚监测](screenshots/coral-monitoring.png) | ![后台管理](screenshots/admin.png) |

---

## 🏗 系统架构

```
                        ┌──────────────────────────────┐
                        │   Vue 2 前端 (:8080)          │
                        │  用户端 / 算法工作台 / 后台管理 │
                        └───────────────┬──────────────┘
                                        │ HTTP / REST
                        ┌───────────────▼──────────────┐
                        │  SpringBoot 网关 (:9090)      │
                        │  用户体系 · 内容社区 · 文件服务 │
                        │  算法请求统一转发              │
                        └───┬───────────┬───────────┬──┘
                            │           │           │
              ┌─────────────▼──┐  ┌─────▼────────┐  ┌▼─────────────────┐
              │ 图像增强 :8002  │  │ 数据集 :8001  │  │ 目标识别 :8000    │
              │ FastAPI        │  │ FastAPI      │  │ FastAPI          │
              │ TensorFlow 2.13│  │ PyTorch 2.4  │  │ PyTorch 2.4      │
              │ 暗通道先验+DNN  │  │ pix2pix GAN  │  │ YOLOv5 6.0       │
              └────────────────┘  └──────────────┘  └──────────────────┘
                            │           │           │
                        ┌───▼───────────▼───────────▼──┐
                        │        MySQL (mypuredb)       │
                        └──────────────────────────────┘
```

**为什么这样拆？** 三个算法服务分别依赖 TensorFlow / PyTorch 且模型互不共享，独立进程部署可避免框架版本冲突，也便于单独扩缩容；SpringBoot 作为统一网关承担鉴权、限流与请求转发，前端只需对接一个地址。

---

## 🛠 技术栈

| 层次 | 技术选型 |
|:---|:---|
| 前端 | Vue 2.6 · Vue Router 3 · Vuex 3 · Element UI · Axios · WangEditor · Highlight.js |
| 后端网关 | Spring Boot 2.5.9 · MyBatis · PageHelper · Hutool · java-jwt · MySQL Connector |
| 图像增强 | FastAPI · TensorFlow 2.13 / Keras · OpenCV · NumPy |
| 数据集生成 | FastAPI · PyTorch 2.4 · pix2pix (CycleGAN 官方实现) |
| 目标识别 | FastAPI · PyTorch 2.4 · YOLOv5 6.0 |
| 数据库 | MySQL 8.0+ |
| 运行环境 | JDK 8 · Maven 3.9 · Node 22 / npm 10 · Python 3.11 |

---

## 📂 目录结构

```
WaterSight/
├── web/
│   ├── frontend/          # Vue 2 前端（用户端 + 算法工作台 + 后台管理）
│   └── backend/           # SpringBoot 网关（用户体系 / 内容社区 / 算法转发）
├── enhance/               # 图像增强服务 (FastAPI :8002)
├── dataset-gan/           # 水下模拟数据集生成服务 (FastAPI :8001, pix2pix)
├── yolo/                  # 目标识别服务 (FastAPI :8000, YOLOv5 6.0)
│   └── check/             #   实际启动目录（鱼类 / 珊瑚检测 API）
├── database/
│   └── mypuredb.sql       # 数据库结构与种子数据
├── samples/               # 四个功能的测试素材
├── docs/                  # 设计与开发文档、作品信息摘要
└── screenshots/           # 界面截图
```

---

## ✨ 功能详解

### 1. 水下图像增强（`enhance/`）

针对水下图像「雾化 + 色偏 + 低对比度」三类退化，采用**传统算子与深度模型级联**的处理链路：

| 步骤 | 方法 | 作用 |
|:---:|:---|:---|
| ① | 暗通道先验（Dark Channel Prior） | 估计大气光与透射率，去除水下散射雾化 |
| ② | LAB 空间自适应白平衡 | 依据亮度通道动态校正色偏，保持色彩自然 |
| ③ | 直方图百分位对比度拉伸 | 自适应确定拉伸区间，避免过曝失真 |
| ④ | CLAHE | 限制对比度的局部直方图均衡，增强细节 |
| ⑤ | 深度学习模型 | TensorFlow/Keras 水下增强网络做最终复原 |

支持**单图增强**与**视频逐帧增强**（异步任务 + 进度轮询），并提供静态资源定时清理避免磁盘膨胀。

### 2. 水下模拟数据集生成（`dataset-gan/`）

针对「真实水下数据难获取」这一核心痛点，基于 **pix2pix** 训练两套专用退化模型：

- `darkBA_pix2pix` —— 深水环境（蓝绿偏色强、光照衰减剧烈）
- `shallowBA_pix2pix` —— 浅水环境（色偏较弱、纹理保留更多）

用户上传陆地图像（或整包数据集），服务自动完成 **解压 → 切分 → 批量推理 → 打包下载**，可指定目标环境与参数，输出即可直接用于目标检测训练。批量推理架构支持大体积数据集（实测 2.42GB / 4000 张）。

### 3. 鱼类识别（`yolo/check/`）

基于 **YOLOv5 6.0** 自训练权重，识别 **12 类**观赏鱼：神仙鱼、蓝倒吊、蝴蝶鱼、小丑鱼、金鱼、斗鱼、摩里斯神仙、剑尾鱼、条纹甜唇鱼、三带雀鲷、黄丽鱼、黄燕尾鱼、斑马鱼。

检测结果返回**类别、数量、置信度**，并附带每类鱼的**中文名、形态描述、饲养指南与难度评级**，将检测结果转化为可直接使用的领域知识。

### 4. 珊瑚礁健康监测（`yolo/check/`）

使用独立训练的珊瑚礁检测权重识别**海星**等指示生物，输出生态角色、栖息环境与保护状态，为珊瑚礁生态评估提供量化依据。

### 5. 平台能力

- **用户体系**：注册登录、JWT 鉴权、角色权限（管理员 / 普通用户 / 科研人员）
- **内容社区**：博客发布、分类标签、评论点赞收藏、关注与消息中心
- **活动系统**：活动发布与报名签到
- **后台管理**：用户 / 内容 / 评论 / 公告 / 活动全量管理
- **文件服务**：图片上传、静态资源托管、算法结果统一回传

---

## 🚀 快速开始

### 前置要求

| 依赖 | 版本 |
|:---|:---|
| JDK | 1.8 |
| Maven | 3.9+ |
| Node.js / npm | 22.2.0 / 10.9.0 |
| Python | 3.11（算法服务各自独立虚拟环境） |
| MySQL | 8.0+ |

### 0. 准备模型权重与演示视频

仓库为控制体积**未包含模型权重与演示视频**，请按下表放置后再启动对应服务（详见 [模型权重](#-模型权重说明)）。

### 1. 初始化数据库

```bash
# 创建数据库并导入结构与种子数据
mysql -u root -p -e "CREATE DATABASE mypuredb DEFAULT CHARACTER SET utf8mb4;"
mysql -u root -p mypuredb < database/mypuredb.sql
```

后端通过环境变量读取数据库连接，未设置时使用默认值 `localhost:3306 / root / root`：

```bash
# 按需覆盖（Linux / macOS）
export DB_HOST=localhost DB_PORT=3306 DB_NAME=mypuredb
export DB_USERNAME=root DB_PASSWORD=你的密码
```

### 2. 启动后端网关（`:9090`）

```bash
cd web/backend
mvn spring-boot:run
```

### 3. 启动前端（`:8080`）

```bash
cd web/frontend
npm install
npm run serve
```

前端接口地址通过 `.env.development` 配置，默认指向 `http://localhost:9090`（后端）与 `http://localhost:8000`（算法服务）。

### 4. 启动算法服务

三个算法服务相互独立，**按需启动**；未启动的功能在前端会提示服务不可用，不影响其他模块。

```bash
# 图像增强 :8002
cd enhance
conda create -n enhance python=3.11 && conda activate enhance
pip install -r requirements.txt
python app.py

# 模拟数据集生成 :8001
cd dataset-gan
conda create -n p2p python=3.11 && conda activate p2p
pip install -r requirements.txt
python app.py

# 目标识别 :8000（注意：启动目录为 check/）
cd yolo/check
conda create -n yolov5 python=3.11 && conda activate yolov5
pip install -r requirements.txt
python app.py
```

### 5. 访问

浏览器打开 `http://localhost:8080`。种子数据内置管理员账号：

| 账号 | 密码 |
|:---|:---|
| `flyao` | `admin123` |

> ⚠️ 部署到公网前请务必修改该默认密码。

---

## 📦 模型权重说明

以下文件因体积原因未纳入版本控制，请从 **<网盘链接待补充>** 下载后按路径放置：

| 放置路径 | 文件 | 用途 |
|:---|:---|:---|
| `enhance/checkpoint/coarse_112/` | `checkpoint`、`coarse.model-final.index`、`coarse.model-final.data-00000-of-00001`、`coarse.model-final.meta.*` | 图像增强 TF 权重 |
| `dataset-gan/checkpoints/darkBA_pix2pix/` | `latest_net_G.pth`、`train_opt.txt`、`test_opt.txt` | 深水退化生成模型 |
| `dataset-gan/checkpoints/shallowBA_pix2pix/` | `latest_net_G.pth`、`train_opt.txt`、`test_opt.txt` | 浅水退化生成模型 |
| `yolo/check/weights/fish/` | `best.pt`、`data.yaml` | 鱼类检测权重 |
| `yolo/check/weights/shanhu/` | `best.pt`、`data.yaml` | 珊瑚礁检测权重 |
| `yolo/pretrained/` | `yolov5s.pt` | YOLOv5 通用预训练权重（供 `check_run*.py` 使用） |
| `web/frontend/src/assets/videos/` | `enhance.mp4`、`dataset.mp4`、`yolo2.mp4`、`yolofish.mp4` | 前端「观看示例」按钮播放的演示视频 |

---

## 📊 测试素材

`samples/` 目录提供四个功能的开箱即用测试数据：

| 目录 | 内容 |
|:---|:---|
| `samples/enhance/` | 水下图像增强测试图（含视频样例） |
| `samples/dataset-generation/` | 模拟数据集生成测试数据 |
| `samples/fish-detection/` | 鱼类识别测试图 20 张 |
| `samples/coral-monitoring/` | 珊瑚礁健康监测测试图 24 张 |

---

## 📐 性能记录

| 场景 | 数据规模 | 耗时 |
|:---|:---|:---|
| 数据集生成与打包下载 | 158MB / 150 张 | 1min40s |
| 数据集生成与打包下载 | 2.42GB / 4000 张 | 30min |

---

## 🙏 致谢

本项目算法部分基于以下优秀开源工作，谨致谢意：

- [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix) —— pix2pix / CycleGAN 官方实现（BSD License）
- [YOLOv5](https://github.com/ultralytics/yolov5) —— Ultralytics 目标检测框架（GPL-3.0 License）

对应子目录保留其原始 LICENSE 文件。

---

## 📄 License

本项目为竞赛参赛作品，仅供学习与交流使用。第三方组件遵循其各自许可证。
