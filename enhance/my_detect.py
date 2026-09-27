import cv2
import numpy as np
import tensorflow as tf
from model import T_CNN
from utils import white_balance, adjust_gamma
import os
import shutil
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
import tempfile
import uuid

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 添加文件处理器
file_handler = logging.FileHandler('my_detect.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# 添加控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

# 全局变量，用于存储任务状态
processing_tasks = {}

def white_balance(img, percent=0.5):
    """自动白平衡"""
    try:
        if img is None:
            return None
        
        out_channels = []
        cumstops = (
            img.shape[0] * img.shape[1] * percent / 200.0,
            img.shape[0] * img.shape[1] * (1 - percent / 200.0)
        )
        
        for channel in cv2.split(img):
            cumhist = np.cumsum(cv2.calcHist([channel], [0], None, [256], (0,256)))
            low_cut, high_cut = np.searchsorted(cumhist, cumstops)
            lut = np.concatenate((
                np.zeros(low_cut),
                np.around(np.linspace(0, 255, high_cut - low_cut + 1)),
                255 * np.ones(255 - high_cut)
            ))
            out_channels.append(cv2.LUT(channel, lut.astype('uint8')))
        
        return cv2.merge(out_channels)
    except Exception as e:
        logger.error(f"白平衡处理出错: {str(e)}")
        return img

def adjust_gamma(image, gamma=1.0):
    """伽马校正"""
    try:
        if image is None:
            return None
            
        # 建立查找表
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255
            for i in np.arange(0, 256)]).astype("uint8")
    
        # 应用伽马校正
        return cv2.LUT(image, table)
    except Exception as e:
        logger.error(f"伽马校正出错: {str(e)}")
        return image

class ImageEnhancer:
    def __init__(self):
        # 禁用GPU
        tf.config.set_visible_devices([], 'GPU')
        
        # 使用相对路径避免中文路径问题
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.checkpoint_dir = os.path.join(current_dir, "checkpoint")
        
        logger.info(f"Checkpoint目录: {self.checkpoint_dir}")

        # 确保目录存在
        os.makedirs(self.checkpoint_dir, exist_ok=True)

        # 检查checkpoint目录中的文件
        if os.path.exists(self.checkpoint_dir):
            files = os.listdir(self.checkpoint_dir)
            logger.info(f"checkpoint目录中的文件: {files}")
            
            # 检查模型子目录
            model_dir = os.path.join(self.checkpoint_dir, "coarse_112")
            if os.path.exists(model_dir):
                model_files = os.listdir(model_dir)
                logger.info(f"模型目录中的文件: {model_files}")

        # 初始化OpenCV设置
        cv2.setNumThreads(0)
        cv2.ocl.setUseOpenCL(False)

        # 设置最大图像尺寸
        self.max_size = 800

        self.executor = ThreadPoolExecutor(max_workers=1)

    def preprocess_image(self, image):
        """预处理图像：调整大小并保持宽高比"""
        height, width = image.shape[:2]
        scale = min(self.max_size / width, self.max_size / height)
        if scale < 1:  # 只有当图像太大时才缩小
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            logger.info(f"图像已调整大小: {new_height}x{new_width}")
        return image

    def enhance_image(self, input_path, output_path):
        try:
            logger.info(f"处理图片: {input_path}")
            # 读取图像文件
            image_test = cv2.imread(input_path, cv2.IMREAD_COLOR)
            if image_test is None:
                raise ValueError(f"无法读取图像文件: {input_path}")

            # 预处理图像
            image_test = self.preprocess_image(image_test)
            shape = image_test.shape
            logger.info(f"最终图像尺寸: {shape}")

            # 创建临时目录，避免中文路径问题
            with tempfile.TemporaryDirectory() as temp_dir:
                # 使用UUID生成唯一文件名
                temp_filename = f"temp_{uuid.uuid4().hex}.png"
                temp_input = os.path.join(temp_dir, temp_filename)

                # 保存临时文件
                success = cv2.imwrite(temp_input, image_test)
                if not success:
                    raise ValueError(f"无法保存临时文件: {temp_input}")
                
                # 检查文件是否成功写入
                if not os.path.exists(temp_input) or os.path.getsize(temp_input) == 0:
                    raise ValueError(f"临时文件创建失败或大小为0: {temp_input}")
                
                logger.info(f"临时文件已保存: {temp_input}")
                
                # 检查文件是否可读
                test_read = cv2.imread(temp_input)
                if test_read is None:
                    raise ValueError(f"无法读取刚刚保存的临时文件: {temp_input}")
                logger.info(f"临时文件读取测试成功")

                # 预处理图像增强
                # 白平衡处理
                wb_image = white_balance(image_test.copy(), 0.5)
                # 对比度增强处理 (CLAHE)
                gray_image = cv2.cvtColor(image_test.copy(), cv2.COLOR_BGR2GRAY)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                ce_image = clahe.apply(gray_image)
                ce_image = cv2.cvtColor(ce_image, cv2.COLOR_GRAY2BGR)
                # 伽马校正处理
                gc_image = adjust_gamma(image_test.copy(), 0.7)
                
                # 重置TensorFlow图
                tf.compat.v1.reset_default_graph()
                
                # 创建会话并处理图像
                with tf.compat.v1.Session() as sess:
                    # 配置参数
                    class Config:
                        def __init__(self):
                            self.epoch = 120
                            self.batch_size = 1
                            # 固定label_height和label_width为112，确保模型加载路径正确
                            self.label_height = 112
                            self.label_width = 112
                            self.learning_rate = 0.001
                            self.beta1 = 0.5
                            self.c_dim = 3
                            self.c_depth_dim = 1
                            self.is_train = False

                    config = Config()
                    
                    # 创建模型实例 - 使用图像真实尺寸作为图像大小
                    # 但使用固定的112作为label_height和label_width以匹配模型目录
                    logger.info(f"创建模型实例，图像尺寸: {shape[0]}x{shape[1]}")
                    model = T_CNN(sess,
                                 image_height=shape[0],
                                 image_width=shape[1],
                                 label_height=112,  # 固定为112
                                 label_width=112,   # 固定为112
                                 batch_size=1,
                                 c_dim=3,
                                 checkpoint_dir=self.checkpoint_dir,
                                 test_image_name=temp_input,
                                 test_wb_name=os.path.join(temp_dir, f"wb_{temp_filename}"),
                                 test_ce_name=os.path.join(temp_dir, f"ce_{temp_filename}"),
                                 test_gc_name=os.path.join(temp_dir, f"gc_{temp_filename}"))
                    
                    # 使用模型处理图像
                    logger.info(f"开始处理图像: {temp_input}")
                    
                    # 运行模型并获取结果图像数据
                    result_image = model.train(config)
                    
                    if result_image is not False:
                        # 获取原始文件名
                        original_filename = os.path.basename(input_path)
                        
                        # 原始文件已被模型直接保存到static/images/enhanced目录
                        enhanced_path = os.path.join("static", "images", "enhanced", original_filename)
                        
                        # 检查文件是否存在
                        if os.path.exists(enhanced_path):
                            logger.info(f"深度学习处理结果已保存到: {enhanced_path}")
                            
                            # 如果需要复制到其他位置
                            if enhanced_path != output_path:
                                logger.info(f"复制结果到指定输出路径: {output_path}")
                                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                                shutil.copy2(enhanced_path, output_path)
                                
                            return True
                        else:
                            raise Exception(f"找不到处理后的图片: {enhanced_path}")
                    else:
                        raise Exception("模型处理失败")
            
        except Exception as e:
            logger.error(f"增强处理出错: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            
            # 尝试使用备选方案
            try:
                logger.info("使用备选方案处理图像")
                image = cv2.imread(input_path, cv2.IMREAD_COLOR)
                if image is not None:
                    # 使用OpenCV基本增强
                    enhanced = self.enhance_image_frame(image)
                    # 保存结果
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    cv2.imwrite(output_path, enhanced)
                    logger.info(f"已使用备选方案处理图像并保存到 {output_path}")
                    return True
            except Exception as backup_error:
                logger.error(f"备选方案处理也失败: {str(backup_error)}")
            
            return False

    def enhance_video(self, input_path, output_path):
        """处理视频文件"""
        try:
            logger.info(f"处理视频: {input_path}")
            
            # 打开视频文件
            cap = cv2.VideoCapture(input_path)
            if not cap.isOpened():
                logger.error(f"无法打开视频文件: {input_path}")
                raise ValueError(f"无法打开视频文件: {input_path}")
            
            # 获取视频信息
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            logger.info(f"视频信息 - 宽度: {width}, 高度: {height}, FPS: {fps}, 总帧数: {total_frames}")
            
            # 创建临时输出文件
            temp_output = output_path + '.temp.mp4'
            
            # 尝试不同的编码器
            encoders = [
                ('avc1', cv2.VideoWriter_fourcc(*'avc1')),  # H.264
                ('H264', cv2.VideoWriter_fourcc(*'H264')),  # H.264 alternate
                ('mp4v', cv2.VideoWriter_fourcc(*'mp4v')),  # MPEG-4
                ('XVID', cv2.VideoWriter_fourcc(*'XVID'))   # XVID
            ]
            
            out = None
            for codec_name, fourcc in encoders:
                try:
                    out = cv2.VideoWriter(temp_output, fourcc, fps, (width, height))
                    if out.isOpened():
                        logger.info(f"使用编码器: {codec_name}")
                        break
                except Exception as e:
                    logger.warning(f"编码器 {codec_name} 失败: {str(e)}")
                    if out:
                        out.release()
            
            if not out or not out.isOpened():
                raise ValueError("无法创建视频写入器")
            
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # 处理帧
                enhanced_frame = self.enhance_image_frame(frame)
                out.write(enhanced_frame)
                
                frame_count += 1
                if frame_count % 10 == 0:  # 每10帧记录一次进度
                    progress = (frame_count / total_frames) * 100
                    logger.info(f"已处理 {frame_count}/{total_frames} 帧 ({progress:.1f}%)")
            
            # 释放资源
            cap.release()
            out.release()
            
            # 检查输出文件
            if os.path.exists(temp_output):
                # 检查文件大小
                file_size = os.path.getsize(temp_output)
                if file_size > 0:
                    shutil.move(temp_output, output_path)
                    logger.info(f"视频处理完成，保存到: {output_path}, 文件大小: {file_size} bytes")
                    return True
                else:
                    logger.error("生成的视频文件大小为0")
                    raise Exception("生成的视频文件无效")
            else:
                logger.error(f"临时文件未生成: {temp_output}")
                raise Exception("处理后的视频文件未生成")
            
        except Exception as e:
            logger.error(f"视频增强处理出错: {str(e)}")
            return False
        
        finally:
            if 'cap' in locals():
                cap.release()
            if 'out' in locals():
                out.release()
            if 'temp_output' in locals() and os.path.exists(temp_output):
                try:
                    os.remove(temp_output)
                except Exception as e:
                    logger.error(f"删除临时文件失败: {str(e)}")

    async def enhance_video_async(self, input_path, output_path):
        """异步处理视频的方法"""
        try:
            # 使用线程池执行同步的视频处理方法
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                self.enhance_video,
                input_path,
                output_path
            )
            return result
        except Exception as e:
            logger.error(f"异步视频处理出错: {str(e)}")
            return False

    def enhance_image_frame(self, frame):
        """处理单个视频帧"""
        try:
            # 调整图像大小
            height, width = frame.shape[:2]
            new_height = 800
            new_width = int((width / height) * new_height)
            resized = cv2.resize(frame, (new_width, new_height))
            logger.info(f"图像已调整大小: {new_height}x{new_width}")
            
            # 应用增强处理
            enhanced = self.enhance_image_data(resized)
            
            # 将图像调整回原始大小
            if enhanced is not None:
                enhanced = cv2.resize(enhanced, (width, height))
                return enhanced
            
            return frame  # 如果处理失败，返回原始帧
            
        except Exception as e:
            logger.error(f"处理视频帧时出错: {str(e)}")
            return frame  # 如果处理失败，返回原始帧

    def enhance_image_data(self, image):
        """处理单个图像数据，参照 enhance_image 的实现逻辑"""
        try:
            # 1. 检查输入图像
            if image is None:
                raise ValueError("输入图像为空")

            # 2. 预处理图像
            image = self.preprocess_image(image)
            shape = image.shape
            logger.info(f"预处理后图像尺寸: {shape}")

            # 3. 创建 TensorFlow 会话并应用模型
            tf.compat.v1.reset_default_graph()
            with tf.compat.v1.Session() as sess:
                # 配置参数
                class Config:
                    def __init__(self):
                        self.epoch = 120
                        self.batch_size = 1
                        # 固定label_height和label_width为112，确保模型加载路径正确
                        self.label_height = 112
                        self.label_width = 112
                        self.learning_rate = 0.001
                        self.beta1 = 0.5
                        self.c_dim = 3
                        self.c_depth_dim = 1
                        self.is_train = False

                config = Config()

                # 创建临时目录保存图像
                with tempfile.TemporaryDirectory() as temp_dir:
                    # 使用UUID生成唯一文件名
                    temp_filename = f"temp_{uuid.uuid4().hex}.png"
                    temp_input = os.path.join(temp_dir, temp_filename)
                    wb_temp = os.path.join(temp_dir, f"wb_{temp_filename}")
                    ce_temp = os.path.join(temp_dir, f"ce_{temp_filename}")
                    gc_temp = os.path.join(temp_dir, f"gc_{temp_filename}")
                    
                    # 保存临时文件
                    cv2.imwrite(temp_input, image)
                    
                    # 准备预处理后的图像
                    # 白平衡处理
                    wb_image = white_balance(image.copy(), 0.5)
                    cv2.imwrite(wb_temp, wb_image)
                    
                    # 对比度增强处理 (CLAHE)
                    gray_image = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                    ce_image = clahe.apply(gray_image)
                    ce_image = cv2.cvtColor(ce_image, cv2.COLOR_GRAY2BGR)
                    cv2.imwrite(ce_temp, ce_image)
                    
                    # 伽马校正处理
                    gc_image = adjust_gamma(image.copy(), 0.7)
                    cv2.imwrite(gc_temp, gc_image)

                    # 创建模型实例 - 使用图像真实尺寸作为图像大小
                    # 但使用固定的112作为label_height和label_width以匹配模型目录
                    model = T_CNN(sess,
                                image_height=shape[0],
                                image_width=shape[1],
                                label_height=112,  # 固定为112
                                label_width=112,   # 固定为112
                                batch_size=1,
                                c_dim=3,
                                checkpoint_dir=self.checkpoint_dir,
                                test_image_name=temp_input,
                                test_wb_name=wb_temp,
                                test_ce_name=ce_temp,
                                test_gc_name=gc_temp)

                    # 运行模型
                    result_image = model.train(config)
                    
                    if result_image is not False:
                        # 将浮点数图像数据转换为uint8格式（0-255范围）
                        enhanced_image = np.clip(result_image * 255, 0, 255).astype(np.uint8)
                        
                        # 如果图像是RGB格式，转换为BGR（OpenCV使用BGR）
                        if enhanced_image.shape[-1] == 3:
                            enhanced_image = cv2.cvtColor(enhanced_image, cv2.COLOR_RGB2BGR)
                            
                        logger.info(f"图像增强处理完成，尺寸: {enhanced_image.shape}")
                        return enhanced_image
                    else:
                        raise ValueError("模型处理失败")

        except Exception as e:
            logger.error(f"图像增强处理出错: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            
            # 应用基本的图像增强作为后备方案
            try:
                # 应用简单的图像增强
                enhanced = cv2.detailEnhance(image, sigma_s=10, sigma_r=0.15)
                enhanced = cv2.edgePreservingFilter(enhanced, flags=1, sigma_s=60, sigma_r=0.4)
                return enhanced
            except:
                return image  # 如果处理失败，返回原始图像