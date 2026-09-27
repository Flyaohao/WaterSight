from fastapi import FastAPI, UploadFile, File, HTTPException, Form, BackgroundTasks
from fastapi.responses import FileResponse, Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from my_detect import ImageEnhancer, processing_tasks
import shutil
import uvicorn
from starlette.responses import FileResponse
from datetime import datetime
import logging
import cv2
import numpy as np
from pathlib import Path
from cleaner import StaticCleaner  # 导入清理工具
import asyncio
from typing import Dict
import mimetypes
import ssl

# 禁用SSL证书验证
ssl._create_default_https_context = ssl._create_unverified_context

# 获取项目根目录的绝对路径
BASE_DIR = Path(__file__).resolve().parent

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 添加文件处理器
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# 添加控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

# 确保必要的目录存在
def ensure_directories():
    directories = [
        "static",  # 添加基础static目录
        "static/images/original",
        "static/images/enhanced",
        "static/videos/original",
        "static/videos/enhanced"
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


# 在创建应用之前确保目录存在
ensure_directories()

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:9090",
        "http://127.0.0.1:9090",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有头部
    expose_headers=["*"],  # 暴露所有响应头部
    max_age=3600,  # 预检请求的缓存时间（秒）
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static", html=False), name="static")

# 创建图像增强器实例
enhancer = ImageEnhancer()

# 创建静态文件清理器实例
cleaner = StaticCleaner(base_dir=BASE_DIR, max_files_per_type=5)

# 添加任务状态存储
processing_tasks: Dict[str, dict] = {}

def init_video_writer(output_path, width, height, fps):
    """初始化视频写入器，尝试多种编码器"""
    codecs = [
        ('mp4v', 'MPEG-4'),  # 最通用兼容
        ('avc1', 'H.264/AVC'),  # 次优
        ('XVID', 'XVID'),  # 备选
        ('MJPG', 'Motion JPEG'),  # 较大文件但兼容性好
        ('WMV1', 'Windows Media Video 7'),
        ('WMV2', 'Windows Media Video 8')
    ]
    
    writer = None
    used_codec = None
    
    for codec, codec_name in codecs:
        try:
            fourcc = cv2.VideoWriter_fourcc(*codec)
            temp_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            if temp_writer.isOpened():
                writer = temp_writer
                used_codec = codec_name
                logger.info(f"成功初始化视频编码器: {codec_name}")
                break
            else:
                temp_writer.release()
                logger.warning(f"编码器 {codec_name} 初始化失败")
        except Exception as e:
            logger.warning(f"尝试编码器 {codec_name} 时出错: {str(e)}")
            continue
    
    if writer is None:
        raise Exception("无法初始化任何视频编码器")
        
    return writer, used_codec

class FastImageEnhancer:
    @staticmethod
    def white_balance(img):
        """自适应白平衡算法"""
        result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        avg_a = np.average(result[:, :, 1])
        avg_b = np.average(result[:, :, 2])
        result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
        return result

    @staticmethod
    def contrast_stretching(img):
        """对比度拉伸"""
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # 计算L通道的直方图
        hist = cv2.calcHist([l], [0], None, [256], [0, 256])
        
        # 找到主要分布区间
        cumsum = np.cumsum(hist)
        total_pixels = img.shape[0] * img.shape[1]
        min_val = np.argmin(np.abs(cumsum - total_pixels * 0.01))
        max_val = np.argmin(np.abs(cumsum - total_pixels * 0.99))
        
        # 拉伸对比度
        l = np.clip((l.astype(float) - min_val) * 255.0 / (max_val - min_val), 0, 255).astype(np.uint8)
        
        enhanced = cv2.merge([l, a, b])
        return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

    @staticmethod
    def color_correction(img):
        """颜色校正"""
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # 计算每个通道的均值和标准差
        l_mean, l_std = np.mean(l), np.std(l)
        a_mean, a_std = np.mean(a), np.std(a)
        b_mean, b_std = np.mean(b), np.std(b)
        
        # 调整a和b通道以增强颜色
        a = np.clip(((a - a_mean) * (1.2 if a_std < 10 else 1.1)) + 128, 0, 255).astype(np.uint8)
        b = np.clip(((b - b_mean) * (1.2 if b_std < 10 else 1.1)) + 128, 0, 255).astype(np.uint8)
        
        enhanced = cv2.merge([l, a, b])
        return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

    @staticmethod
    def enhance_image(image):
        """使用改进的水下图像增强方法"""
        try:
            # 转换为float32类型，范围0-1
            img_float = image.astype(np.float32) / 255.0
            
            # 1. 去雾处理
            # 使用暗通道先验去雾
            dark_channel = np.min(img_float, axis=2)
            A = np.max(dark_channel)  # 大气光估计
            transmission = 1 - 0.95 * dark_channel  # 透射率估计
            transmission = np.maximum(transmission, 0.1)
            
            # 应用去雾
            result = np.empty_like(img_float)
            for i in range(3):
                result[:,:,i] = (img_float[:,:,i] - A) / transmission + A
            
            # 转回uint8
            result = np.clip(result * 255, 0, 255).astype(np.uint8)
            
            # 2. 自适应白平衡
            result = FastImageEnhancer.white_balance(result)
            
            # 3. 对比度拉伸
            result = FastImageEnhancer.contrast_stretching(result)
            
            # 4. CLAHE处理（分别处理每个通道）
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            for i in range(3):
                result[:,:,i] = clahe.apply(result[:,:,i])
            
            # 5. 颜色校正
            result = FastImageEnhancer.color_correction(result)
            
            # 6. 细节增强
            # 使用USM锐化
            gaussian = cv2.GaussianBlur(result, (0, 0), 2.0)
            result = cv2.addWeighted(result, 1.5, gaussian, -0.5, 0)
            
            # 7. 最终调整
            # 使用Gamma校正改善暗部细节
            gamma = 1.2
            look_up_table = np.empty((1,256), np.uint8)
            for i in range(256):
                look_up_table[0,i] = np.clip(pow(i / 255.0, 1.0 / gamma) * 255.0, 0, 255)
            result = cv2.LUT(result, look_up_table)
            
            return result
            
        except Exception as e:
            logger.error(f"快速增强处理出错: {str(e)}")
            raise Exception(f"图像处理失败: {str(e)}")

    @staticmethod
    async def enhance_video_async(input_path, output_path, progress_callback=None):
        """异步处理视频文件"""
        try:
            cap = cv2.VideoCapture(input_path)
            if not cap.isOpened():
                raise Exception("无法打开视频文件")
                
            # 获取视频信息
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            logger.info(f"处理视频 - 尺寸: {width}x{height}, FPS: {fps}, 总帧数: {total_frames}")
            
            # 初始化视频写入器 - 优先使用H.264编码器，最广泛兼容的格式
            codecs = [
                ('mp4v', 'MPEG-4'),  # 最通用兼容
                ('avc1', 'H.264/AVC'),  # 次优
                ('XVID', 'XVID'),  # 备选
                ('MJPG', 'Motion JPEG'),  # 较大文件但兼容性好
                ('WMV1', 'Windows Media Video 7'),
                ('WMV2', 'Windows Media Video 8')
            ]
            
            writer = None
            used_codec = None
            
            for codec, codec_name in codecs:
                try:
                    fourcc = cv2.VideoWriter_fourcc(*codec)
                    temp_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                    if temp_writer.isOpened():
                        writer = temp_writer
                        used_codec = codec_name
                        logger.info(f"成功初始化视频编码器: {codec_name}")
                        break
                    else:
                        temp_writer.release()
                        logger.warning(f"编码器 {codec_name} 初始化失败")
                except Exception as e:
                    logger.warning(f"尝试编码器 {codec_name} 时出错: {str(e)}")
                    continue
            
            if writer is None:
                raise Exception("无法初始化任何视频编码器")
                
            try:
                frame_count = 0
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                        
                    # 使用快速增强方法处理帧
                    enhanced_frame = FastImageEnhancer.enhance_image(frame)
                    writer.write(enhanced_frame)
                    
                    frame_count += 1
                    if progress_callback:
                        try:
                            if asyncio.iscoroutinefunction(progress_callback):
                                await progress_callback(frame_count)
                            else:
                                progress_callback(frame_count)
                        except Exception as e:
                            logger.error(f"进度回调出错: {str(e)}")
                    
                    if frame_count % 10 == 0:  # 每10帧记录一次进度
                        progress = (frame_count / total_frames) * 100
                        logger.info(f"视频处理进度: {progress:.2f}%")
                        await asyncio.sleep(0)  # 让出控制权
                    
                logger.info("视频处理完成")
                
            finally:
                cap.release()
                writer.release()
                
            # 验证输出文件
            if not os.path.exists(output_path):
                raise Exception("输出文件未生成")
                
            output_size = os.path.getsize(output_path)
            if output_size == 0:
                raise Exception("输出文件大小为0")
                
            # 验证可以打开输出文件
            test_cap = cv2.VideoCapture(output_path)
            if not test_cap.isOpened():
                raise Exception("无法打开生成的视频文件")
            test_cap.release()
            
            logger.info(f"视频文件已生成: {output_path}, 大小: {output_size} bytes")
            return True
            
        except Exception as e:
            logger.error(f"视频快速增强处理出错: {str(e)}")
            # 清理失败的输出文件
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                    logger.info(f"已删除失败的输出文件: {output_path}")
                except Exception as cleanup_error:
                    logger.error(f"清理失败的输出文件出错: {str(cleanup_error)}")
            raise Exception(f"视频处理失败: {str(e)}")

# 创建快速增强器实例
fast_enhancer = FastImageEnhancer()

# 添加CORS中间件，确保静态文件也能正确处理跨域请求
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    
    # 为所有响应添加CORS头
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Expose-Headers"] = "Content-Length, Content-Type, Content-Range, Accept-Ranges"
    
    # 处理预检请求
    if request.method == "OPTIONS":
        return Response(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Max-Age": "3600",
            }
        )
    
    return response

# 添加日志中间件
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"收到请求: {request.method} {request.url}")
    logger.info(f"请求头: {request.headers}")
    response = await call_next(request)
    logger.info(f"响应状态码: {response.status_code}")
    return response

# 添加新的统一端点，根据文件类型自动路由
@app.post("/api/enhance")
async def enhance_file(
    file: UploadFile = File(...), 
    mode: str = Form("standard"),
    background_tasks: BackgroundTasks = None
):
    if background_tasks is None:
        background_tasks = BackgroundTasks()
        
    logger.info("="*50)
    logger.info(f"收到通用增强请求，文件名: {file.filename}")
    logger.info(f"Content-Type: {file.content_type}")
    logger.info(f"处理模式: {mode}")
    
    # 根据文件类型调用相应的处理函数
    if file.content_type.startswith('image/'):
        logger.info("检测到图片文件，转发到图像处理")
        return await enhance_image(file, mode)
    elif file.content_type.startswith('video/'):
        logger.info("检测到视频文件，转发到视频处理")
        return await enhance_video(
            file=file,
            mode=mode,
            background_tasks=background_tasks
        )
    else:
        logger.error(f"不支持的文件类型: {file.content_type}")
        return {
            "status": "error",
            "message": f"不支持的文件类型: {file.content_type}，仅支持图片或视频"
        }

@app.post("/api/enhance/image")
async def enhance_image(file: UploadFile = File(...), mode: str = "standard"):
    try:
        # 生成文件名
        original_filename = file.filename
        file_extension = os.path.splitext(original_filename)[1]

        # 保存原始图片
        original_path = f"static/images/original/{original_filename}"
        with open(original_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 设置增强后的图片路径
        enhanced_filename = f"{os.path.splitext(original_filename)[0]}_enhanced{file_extension}"
        enhanced_path = f"static/images/enhanced/{enhanced_filename}"

        # 根据模式选择处理方法
        if mode == "fast":
            # 读取图像
            image = cv2.imread(original_path)
            if image is None:
                raise Exception("无法读取图像文件")
                
            # 使用快速处理方法
            enhanced_image = FastImageEnhancer.enhance_image(image)
            
            # 保存结果
            cv2.imwrite(enhanced_path, enhanced_image)
            success = True
        else:
            # 使用标准处理方法（深度学习模型）
            success = enhancer.enhance_image(original_path, enhanced_path)

        # 清理旧文件
        deleted = cleaner.clean_on_upload("image", original_filename)
        logger.info(f"清理完成，共删除 {deleted} 个旧文件")

        # 构建响应
        if success:
            response_data = {
                "status": "success",
                "message": f"图像{mode}增强成功",
                "original_image": f"/static/images/original/{original_filename}",
                "result_image": f"/static/images/enhanced/{enhanced_filename}",
                "processing_mode": mode
            }
        else:
            response_data = {
                "status": "error",
                "message": "图像增强处理失败"
            }
            
        return response_data

    except Exception as e:
        logger.error(f"图像增强处理出错: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }

async def process_video_background(
    original_path: str,
    enhanced_path: str,
    task_id: str,
    mode: str,
    enhancer_instance,
    fast_enhancer_instance
) -> bool:
    """在后台处理视频"""
    try:
        logger.info(f"开始处理视频任务 {task_id}")
        logger.info(f"处理模式: {mode}")
        
        # 更新任务状态为处理中
        if task_id not in processing_tasks:
            logger.error(f"任务 {task_id} 不存在")
            return False
            
        processing_tasks[task_id]["status"] = "processing"
        
        # 获取视频信息用于进度计算
        cap = cv2.VideoCapture(original_path)
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {original_path}")
            
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        
        # 更新任务状态
        processing_tasks[task_id].update({
            "total_frames": total_frames,
            "processed_frames": 0,
            "progress": 0
        })
        
        # 定义进度回调函数
        async def progress_callback(current_frame: int):
            if task_id in processing_tasks:
                progress = min(100, int((current_frame / total_frames) * 100))
                processing_tasks[task_id].update({
                    "progress": progress,
                    "processed_frames": current_frame,
                    "status": "processing"  # 确保状态保持为processing
                })
                await asyncio.sleep(0)  # 让出控制权
        
        if mode == "fast":
            logger.info("使用快速处理模式")
            success = await fast_enhancer_instance.enhance_video_async(
                original_path, 
                enhanced_path
            )
        else:
            logger.info("使用标准处理模式")
            success = await enhancer_instance.enhance_video_async(
                original_path, 
                enhanced_path
            )
            
        if success:
            logger.info(f"视频处理成功: {task_id}")
            # 验证输出文件
            if not os.path.exists(enhanced_path):
                raise Exception("输出文件未生成")
                
            output_size = os.path.getsize(enhanced_path)
            if output_size == 0:
                raise Exception("输出文件大小为0")
                
            processing_tasks[task_id].update({
                "status": "completed",
                "result_path": enhanced_path,
                "progress": 100,
                "processed_frames": total_frames,
                "completion_time": datetime.now().isoformat()
            })
        else:
            logger.error(f"视频处理失败: {task_id}")
            processing_tasks[task_id].update({
                "status": "failed",
                "error": "处理失败",
                "progress": -1,
                "completion_time": datetime.now().isoformat()
            })
            
        return success
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"视频处理错误: {error_msg}")
        if task_id in processing_tasks:
            processing_tasks[task_id].update({
                "status": "failed",
                "error": error_msg,
                "progress": -1,
                "completion_time": datetime.now().isoformat()
            })
        
        # 清理失败的输出文件
        if os.path.exists(enhanced_path):
            try:
                os.remove(enhanced_path)
                logger.info(f"已删除失败的输出文件: {enhanced_path}")
            except Exception as cleanup_error:
                logger.error(f"清理失败的输出文件出错: {str(cleanup_error)}")
        return False

@app.post("/api/enhance/video")
async def enhance_video(
    file: UploadFile = File(...),
    mode: str = Form("standard"),
    background_tasks: BackgroundTasks = None
):
    if background_tasks is None:
        background_tasks = BackgroundTasks()
        
    logger.info("="*50)
    logger.info("进入视频处理函数")
    logger.info(f"收到视频增强请求，文件名: {file.filename}")
    logger.info(f"Content-Type: {file.content_type}")
    logger.info(f"处理模式: {mode}")

    try:
        # 生成唯一任务ID
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"
        
        # 生成唯一文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_filename = f"{timestamp}_{file.filename}"
        file_extension = os.path.splitext(original_filename)[1].lower()
        
        # 确保扩展名是.mp4
        if file_extension != '.mp4':
            original_filename = f"{os.path.splitext(original_filename)[0]}.mp4"
        
        # 设置路径
        videos_dir = os.path.join(BASE_DIR, "static", "videos")
        original_dir = os.path.join(videos_dir, "original")
        enhanced_dir = os.path.join(videos_dir, "enhanced")
        
        os.makedirs(original_dir, exist_ok=True)
        os.makedirs(enhanced_dir, exist_ok=True)
        
        original_path = os.path.join(original_dir, original_filename)
        enhanced_filename = f"{os.path.splitext(original_filename)[0]}_enhanced.mp4"
        enhanced_path = os.path.join(enhanced_dir, enhanced_filename)
        
        # 保存原始文件
        with open(original_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            
        # 获取视频信息
        cap = cv2.VideoCapture(original_path)
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {original_path}")
            
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        estimated_time = total_frames / fps
        cap.release()
        
        # 初始化任务状态
        processing_tasks[task_id] = {
            "status": "",  # 空字符串表示正在处理
            "progress": 0,
            "total_frames": total_frames,
            "processed_frames": 0,
            "original_path": original_path,
            "enhanced_path": enhanced_path,
            "mode": mode,
            "start_time": datetime.now().isoformat()
        }
        
        # 创建快速增强器实例
        fast_enhancer_instance = FastImageEnhancer()
        
        # 启动后台处理任务
        background_tasks.add_task(
            process_video_background,
            original_path,
            enhanced_path,
            task_id,
            mode,
            enhancer,
            fast_enhancer_instance
        )
        
        # 返回初始响应
        return {
            "status": "",  # 空字符串表示正在处理
            "task_id": task_id,
            "message": "视频处理已开始",
            "original_video": f"/static/videos/original/{original_filename}",
            "result_video": f"/static/videos/enhanced/{enhanced_filename}",
            "total_frames": total_frames,
            "fps": fps,
            "width": width,
            "height": height,
            "estimated_time": round(estimated_time, 2),
            "original_size": os.path.getsize(original_path),
            "content_type": "video/mp4",
            "processing_mode": mode,
            "progress": 0
        }
            
    except Exception as e:
        logger.error(f"视频处理错误: {str(e)}")
        # 清理临时文件
        try:
            if 'original_path' in locals() and os.path.exists(original_path):
                os.remove(original_path)
            if 'enhanced_path' in locals() and os.path.exists(enhanced_path):
                os.remove(enhanced_path)
        except Exception as cleanup_error:
            logger.error(f"清理临时文件失败: {str(cleanup_error)}")
            
        return JSONResponse(
            status_code=500,
            content={
                "status": "exception",  # 使用exception表示错误
                "message": str(e),
                "progress": -1
            }
        )

@app.get("/api/enhance/video/status/{task_id}")
async def get_video_status(task_id: str):
    """获取视频处理状态"""
    logger.info(f"获取任务状态: {task_id}")
    logger.info(f"当前所有任务: {list(processing_tasks.keys())}")
    
    if task_id not in processing_tasks:
        logger.error(f"任务不存在: {task_id}")
        return JSONResponse(
            status_code=404,
            content={
                "status": "error",
                "message": "任务不存在",
                "progress": -1
            }
        )
        
    task_info = processing_tasks[task_id]
    logger.info(f"任务信息: {task_info}")
    
    try:
        if task_info["status"] == "completed":
            # 如果处理完成，返回完整的结果信息
            enhanced_path = task_info["result_path"]
            enhanced_size = os.path.getsize(enhanced_path) if os.path.exists(enhanced_path) else 0
            
            return {
                "status": "success",
                "message": f"视频{task_info['mode']}处理成功",
                "original_video": f"/static/videos/original/{os.path.basename(task_info['original_path'])}",
                "result_video": f"/static/videos/enhanced/{os.path.basename(task_info['enhanced_path'])}",
                "total_frames": task_info["total_frames"],
                "processed_frames": task_info["processed_frames"],
                "progress": 100,
                "enhanced_size": enhanced_size,
                "processing_mode": task_info["mode"]
            }
        elif task_info["status"] == "failed":
            return {
                "status": "exception",
                "message": task_info.get("error", "处理失败"),
                "progress": -1
            }
        else:
            # 处理中，返回进度信息
            progress = task_info.get("progress", 0)
            return {
                "status": "",
                "progress": progress,
                "processed_frames": task_info.get("processed_frames", 0),
                "total_frames": task_info.get("total_frames", 0),
                "message": "视频处理中",
                "processing_mode": task_info["mode"]
            }
    except Exception as e:
        logger.error(f"获取视频状态时出错: {str(e)}")
        return {
            "status": "exception",
            "message": f"获取状态失败: {str(e)}",
            "progress": -1
        }

@app.get("/")
async def check_health():
    return {"status": "healthy"}


# 修改静态文件访问路由
@app.get("/static/{file_path:path}")
async def serve_static(file_path: str):
    logger.info(f"请求静态文件: {file_path}")
    full_path = os.path.join("static", file_path)
    logger.info(f"完整文件路径: {full_path}")

    if not os.path.exists(full_path):
        logger.error(f"文件未找到: {full_path}")
        try:
            dir_path = os.path.dirname(full_path)
            if os.path.exists(dir_path):
                files = os.listdir(dir_path)
                logger.info(f"目录 {dir_path} 中的文件: {files}")
        except Exception as e:
            logger.error(f"无法列出目录内容: {str(e)}")
        raise HTTPException(status_code=404, detail=f"文件不存在: {file_path}")

    try:
        file_size = os.path.getsize(full_path)
        logger.info(f"文件大小: {file_size} bytes")

        # 增强CORS头部设置
        headers = {
            'Accept-Ranges': 'bytes',
            'Cache-Control': 'public, max-age=3600',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Expose-Headers': 'Content-Length, Content-Type, Content-Range, Accept-Ranges',
            'Cross-Origin-Resource-Policy': 'cross-origin',
            'Cross-Origin-Embedder-Policy': 'require-corp'
        }

        if file_path.endswith('.mp4'):
            logger.info("返回MP4视频文件")
            headers.update({
                'Content-Type': 'video/mp4',
                'Content-Length': str(file_size),
                'Content-Disposition': f'inline; filename="{os.path.basename(file_path)}"',
                # 添加额外的安全头部，允许在HTTP连接中加载视频
                'Feature-Policy': 'autoplay *; fullscreen *',
                'Permissions-Policy': 'autoplay=*, fullscreen=*',
                'Referrer-Policy': 'no-referrer-when-downgrade',
                'X-Content-Type-Options': 'nosniff'
            })
            return FileResponse(
                full_path,
                media_type="video/mp4",
                headers=headers,
                filename=os.path.basename(file_path)
            )
        elif file_path.endswith(('.jpg', '.jpeg')):
            headers['Content-Type'] = 'image/jpeg'
            return FileResponse(
                full_path,
                media_type="image/jpeg",
                headers=headers,
                filename=os.path.basename(file_path)
            )
        elif file_path.endswith('.png'):
            headers['Content-Type'] = 'image/png'
            return FileResponse(
                full_path,
                media_type="image/png",
                headers=headers,
                filename=os.path.basename(file_path)
            )
        else:
            # 获取适当的MIME类型
            content_type, _ = mimetypes.guess_type(full_path)
            if content_type:
                headers['Content-Type'] = content_type
            
            return FileResponse(
                full_path,
                headers=headers,
                filename=os.path.basename(file_path)
            )
    except Exception as e:
        logger.error(f"文件访问错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# 添加定期清理功能的路由
@app.get("/api/clean-static")
async def clean_static_files():
    """手动触发清理静态文件的端点"""
    try:
        deleted = cleaner.clean_all()
        return {
            "status": "success", 
            "message": f"清理完成，共删除 {deleted} 个文件"
        }
    except Exception as e:
        logger.error(f"清理失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# 添加一个新的流式视频API端点
@app.get("/api/video-stream/{file_path:path}")
async def video_stream(file_path: str):
    """流式传输视频文件，解决CORS和浏览器限制问题"""
    logger.info(f"请求视频流: {file_path}")
    
    # 构建完整路径，确保只能访问static/videos目录下的文件
    if not file_path.startswith(("original/", "enhanced/")):
        file_path = f"enhanced/{file_path}"
        
    full_path = os.path.join("static", "videos", file_path)
    logger.info(f"视频完整路径: {full_path}")
    
    if not os.path.exists(full_path):
        logger.error(f"视频文件未找到: {full_path}")
        raise HTTPException(status_code=404, detail=f"视频文件不存在: {file_path}")
    
    # 设置强制下载的响应头，确保视频能正确传输
    headers = {
        'Accept-Ranges': 'bytes',
        'Cache-Control': 'public, max-age=3600',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Expose-Headers': 'Content-Length, Content-Range, Accept-Ranges',
        'Content-Type': 'video/mp4',
        'Content-Disposition': f'attachment; filename="{os.path.basename(full_path)}"',
    }
    
    return FileResponse(
        full_path,
        headers=headers,
        filename=os.path.basename(full_path),
        media_type='video/mp4'
    )

# 添加一个更简单的视频API端点，返回base64编码的视频
@app.get("/api/video-data/{file_path:path}")
async def get_video_data(file_path: str):
    """返回base64编码的视频文件，解决浏览器兼容性问题"""
    import base64
    
    # 构建完整路径，确保只能访问static/videos目录下的文件
    if not file_path.startswith(("original/", "enhanced/")):
        file_path = f"enhanced/{file_path}"
        
    full_path = os.path.join("static", "videos", file_path)
    logger.info(f"请求视频数据: {full_path}")
    
    if not os.path.exists(full_path):
        logger.error(f"视频文件未找到: {full_path}")
        raise HTTPException(status_code=404, detail=f"视频文件不存在: {file_path}")
    
    try:
        # 读取文件内容并进行base64编码
        with open(full_path, "rb") as video_file:
            video_content = video_file.read()
            base64_video = base64.b64encode(video_content).decode('utf-8')
            
        # 返回包含base64编码和文件信息的JSON响应
        return {
            "status": "success",
            "filename": os.path.basename(full_path),
            "content_type": "video/mp4",
            "size": len(video_content),
            "data": f"data:video/mp4;base64,{base64_video}"
        }
    except Exception as e:
        logger.error(f"处理视频数据出错: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 添加重启命令，确保所有修改都能生效
if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8002
    
    print(f"启动服务器 http://{host}:{port}")
    
    # 启动时清理一次静态文件
    try:
        deleted = cleaner.clean_all()
        print(f"启动时清理完成，共删除 {deleted} 个文件")
    except Exception as e:
        print(f"启动时清理失败: {str(e)}")
    
    # 配置Uvicorn服务器，增加请求超时时间
    uvicorn.run(
        "app:app", 
        host=host, 
        port=port, 
        reload=True, 
        timeout_keep_alive=300,  # 增加到5分钟
        limit_concurrency=10,    # 限制并发请求数
        backlog=100              # 连接队列大小
    )