from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import shutil
from my_combine import process_dataset as preprocess_dataset
from my_process import process_dataset as process_dataset
import uvicorn
import logging
import sys
from datetime import datetime
import glob
import zipfile
import tempfile
from PIL import Image
from cleaner import StaticCleaner  # 导入StaticCleaner类
import time
import json
import hashlib

# 首先定义基础目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # 只保留控制台处理器
    ],
    force=True
)
logger = logging.getLogger(__name__)

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
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# 配置目录（预处理的目录）
STATIC_DIR = os.path.join(BASE_DIR, "static")  # 预处理的静态文件根目录
DATASET_DIR = os.path.join(STATIC_DIR, "datasets")  # 预处理的数据集目录
PROCESSED_DIR = os.path.join(STATIC_DIR, "processed")  # 预处理的结果目录

# 配置目录（处理的目录）
STATIC1_DIR = os.path.join(BASE_DIR, "static1")  # 处理的静态文件根目录
DATASET1_DIR = os.path.join(STATIC1_DIR, "datasets")  # 处理的数据集目录
PROCESSED1_DIR = os.path.join(STATIC1_DIR, "processed")  # 处理的结果目录
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")  # 新增：上传文件目录

# 在日志中输出路径信息，便于调试
logger.info(f"BASE_DIR: {BASE_DIR}")

# 确保所有必要的目录存在
os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(DATASET1_DIR, exist_ok=True)
os.makedirs(PROCESSED1_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)  # 确保上传目录存在

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/static1", StaticFiles(directory=STATIC1_DIR), name="static1")
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")  # 挂载上传目录

# 初始化静态文件清理器
cleaner = StaticCleaner(BASE_DIR, max_files=1)  # 每个目录保留最新的1个文件
logger.info("初始化静态文件清理器完成")

# 定义一个清理函数，用于首次启动时清理
def initial_clean():
    """初始启动时清理所有目录中过多的文件，但保留每个目录中的最新文件"""
    logger.info("首次启动，执行初始目录清理...")
    deleted = cleaner.clean_all()
    logger.info(f"初始清理完成，共删除 {deleted} 个文件或目录")

# 启动时执行一次初始清理
initial_clean()

# 定义请求模型
class DatasetPreprocessRequest(BaseModel):
    datasetPath: str = None  # 可选，允许空以支持直接上传
    environment: str = 'deep'  # 默认使用深水环境
    fileName: str = None  # 可选的文件名
    fileSize: int = None  # 可选的文件大小

class DatasetProcessRequest(BaseModel):
    datasetPath: str = None  # 可选，允许空以支持直接上传
    environment: str = 'deep'  # 默认使用深水环境
    fileName: str = None  # 可选的文件名
    fileSize: int = None  # 可选的文件大小

# 添加请求日志中间件
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    return response

# 修改 force_print 函数
def force_print(*args, **kwargs):
    message = " ".join(map(str, args))
    print(message, **kwargs)
    sys.stdout.flush()
    # 同时写入日志
    logger.info(message)

def get_model_name(environment: str) -> str:
    """根据环境选择合适的模型"""
    environment = environment.lower() if environment else "deep"
    if environment == 'shallow':
        logger.info(f"根据环境[{environment}]选择浅水模型: shallowBA_pix2pix")
        return 'shallowBA_pix2pix'
    logger.info(f"根据环境[{environment}]选择深水模型: darkBA_pix2pix")
    return 'darkBA_pix2pix'  # 默认使用深水模型

def find_any_available_model():
    """
    扫描checkpoints目录查找任何可用的模型文件
    
    返回:
        tuple: (模型文件路径, 模型名称)，如果未找到则返回(None, None)
    """
    logger.info("尝试查找任何可用的模型文件...")
    
    # 优先尝试默认模型
    model_names = ['darkBA_pix2pix', 'shallowBA_pix2pix']
    for model_name in model_names:
        model_path = os.path.join(BASE_DIR, 'checkpoints', model_name, 'latest_net_G.pth')
        if os.path.exists(model_path):
            logger.info(f"找到默认模型: {model_name}")
            return model_path, model_name
    
    # 搜索checkpoints目录中的所有子目录
    checkpoints_dir = os.path.join(BASE_DIR, 'checkpoints')
    if os.path.exists(checkpoints_dir):
        for dir_name in os.listdir(checkpoints_dir):
            model_dir = os.path.join(checkpoints_dir, dir_name)
            if os.path.isdir(model_dir):
                model_file = os.path.join(model_dir, 'latest_net_G.pth')
                if os.path.exists(model_file):
                    logger.info(f"找到模型: {dir_name}")
                    return model_file, dir_name
    
    logger.warning("未找到任何可用的模型文件")
    return None, None

# ================== 数据集预处理功能 ==================
@app.post("/api/dataset/process")
async def process_dataset_endpoint(
    file: UploadFile = File(None),
    environment: str = Form(None)):
    """处理数据集的接口，支持两种模式：上传文件或提供已上传文件的文件名"""
    try:
        request = DatasetPreprocessRequest(environment=environment)
        
        logger.info("\n=== Starting Dataset Processing ===")
        logger.info(f"Request data: {request}")
        logger.info(f"Form环境参数: {environment}")
        logger.info(f"File info: {file.filename if file else 'No file uploaded'}")
        
        # 获取上传的文件路径
        file_path = None
        
        # 判断上传模式
        if file and file.filename:
            logger.info(f"使用文件上传模式: {file.filename}")
            
            # 保存上传的文件
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = f"{timestamp}_{file.filename}"
            file_path = os.path.join(UPLOADS_DIR, file_name)
            
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
                logger.info(f"文件已保存到: {file_path}，大小: {len(content)} bytes")
            
            # 文件保存后只清理uploads目录，不清理其他目录
            deleted = cleaner.clean_uploads_only()
            logger.info(f"清理uploads目录完成，删除了 {deleted} 个文件")
        
        elif request.datasetPath:
            logger.info(f"使用路径模式: {request.datasetPath}")
            
            # 从文件名获取路径
            file_name = os.path.basename(request.datasetPath)
            file_path = os.path.join(UPLOADS_DIR, file_name)
            
            if not os.path.exists(file_path):
                logger.error(f"无法找到上传文件: {file_path}")
                raise HTTPException(
                    status_code=404,
                    detail=f"无法找到上传文件: {file_name}。请重新上传文件。"
                )
        else:
            logger.error("未提供文件或文件路径")
            raise HTTPException(
                status_code=400,
                detail="必须提供文件上传或文件路径"
            )
        
        # 根据环境选择模型
        model_name = get_model_name(request.environment)
        logger.info(f"Using model: {model_name}")
        
        # 检查模型文件是否存在
        model_path = os.path.join(BASE_DIR, 'checkpoints', model_name, 'latest_net_G.pth')
        logger.info(f"Looking for model at: {model_path}")
        
        if not os.path.exists(model_path):
            # 修改逻辑：不再自动回退到深水模型，而是报错
            logger.error(f"找不到指定的模型: {model_path}")
            raise HTTPException(
                status_code=400,
                detail=f"找不到{request.environment}环境的模型文件，请确认模型文件是否存在于checkpoints/{model_name}目录"
            )

        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            logger.info(f"Created temporary directory: {temp_dir}")

            # 解压文件
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                logger.info("Extracted ZIP file successfully")
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to extract ZIP file: {str(e)}"
                )

            # 查找数据集文件夹
            subfolders = [f for f in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, f))]
            logger.info(f"Found subfolders: {subfolders}")

            if not subfolders:
                raise HTTPException(
                    status_code=400,
                    detail="No dataset folder found in ZIP file"
                )

            dataset_folder = subfolders[0]
            logger.info(f"Using dataset folder: {dataset_folder}")

            # 获取时间戳
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            dataset_id = timestamp

            # 复制数据集到目标目录
            target_dataset_dir = os.path.join(DATASET_DIR, dataset_id)
            logger.info(f"Copying dataset to: {target_dataset_dir}")
            
            if os.path.exists(target_dataset_dir):
                shutil.rmtree(target_dataset_dir)
            shutil.copytree(os.path.join(temp_dir, dataset_folder), target_dataset_dir)
            logger.info("Copy completed")

            # 设置输出目录
            logger.info("\n=== Setting up Output Directory ===")
            output_dir = os.path.join(PROCESSED_DIR, f"{dataset_id}_processed")
            logger.info(f"Created output directory: {output_dir}")
            
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            os.makedirs(output_dir)

            # 处理数据集
            logger.info("\n=== Processing Dataset ===")
            logger.info(f"Input path: {target_dataset_dir}")
            logger.info(f"Output path: {output_dir}")

            # 调用预处理函数
            success = preprocess_dataset(
                input_path=target_dataset_dir,
                output_path=output_dir,
                model_name=model_name
            )
            
            if not success:
                raise Exception("数据集处理失败")

            # 创建结果压缩包
            logger.info("\n=== Creating ZIP Archive ===")
            zip_filename = f"preprocessed_dataset_{timestamp}.zip"
            zip_path = os.path.join(PROCESSED_DIR, zip_filename)
            logger.info(f"Creating ZIP file at: {zip_path}")

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(output_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        logger.info(f"Adding to ZIP: {os.path.relpath(file_path, output_dir)}")
                        zipf.write(file_path, os.path.relpath(file_path, output_dir))

            logger.info("ZIP file created successfully")

            return {
                "status": "success",
                "message": "数据集预处理完成",
                "path": f"/static/processed/{zip_filename}"
            }

    except HTTPException as e:
        # 重新抛出HTTPException异常
        raise e
    except Exception as e:
        logger.error(f"Error processing dataset: {str(e)}")
        logger.error("Stack trace:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ================== 数据集处理功能 ==================
@app.post("/process-dataset")
async def process_dataset_handler(dataset_req: DatasetProcessRequest):
    # 记录请求信息
    logger.info(f"接收到数据集处理请求: {dataset_req}")
    logger.info(f"环境参数: {dataset_req.environment}")
    
    # 检查是否提供了 datasetPath
    if not dataset_req.datasetPath:
        error_message = "未提供数据集路径 (datasetPath)"
        logger.error(error_message)
        raise HTTPException(status_code=400, detail=error_message)
    
    java_path = dataset_req.datasetPath
    
    # 获取当前时间戳作为唯一标识
    timestamp = int(time.time())
    logger.info(f"生成时间戳: {timestamp}")
    
    # 清理static目录，但保留当前处理的文件
    cleaner.clean_static_directories(timestamp=timestamp)
    
    # 根据环境选择模型
    environment = dataset_req.environment or "deep"  # 获取环境参数，默认为deep
    logger.info(f"原始环境参数: {environment}")
    model_name = get_model_name(environment)  # 使用get_model_name函数获取对应的模型名称
    logger.info(f"转换后的模型名称: {model_name}")
    logger.info(f"根据环境[{environment}]选择模型: {model_name}")
    
    # 检查指定的模型是否存在
    model_path = os.path.join(BASE_DIR, 'checkpoints', model_name, 'latest_net_G.pth')
    
    # 检查模型文件大小
    if os.path.exists(model_path):
        file_size = os.path.getsize(model_path)
        logger.info(f"模型文件存在: {model_path}, 大小: {file_size} 字节")
        
        # 检查另一个模型是否也存在
        other_model = 'shallowBA_pix2pix' if model_name == 'darkBA_pix2pix' else 'darkBA_pix2pix'
        other_model_path = os.path.join(BASE_DIR, 'checkpoints', other_model, 'latest_net_G.pth')
        if os.path.exists(other_model_path):
            other_file_size = os.path.getsize(other_model_path)
            logger.info(f"另一个模型文件也存在: {other_model_path}, 大小: {other_file_size} 字节")
            if file_size == other_file_size:
                logger.warning("警告: 两个模型文件大小相同，可能是同一个模型的复制！")
    else:
        logger.error(f"指定的模型文件不存在: {model_path}")
        
        error_detail = {
            "error": "模型文件不存在",
            "message": f"找不到{environment}环境的模型文件(checkpoints/{model_name}/latest_net_G.pth)",
            "solution": "请确认模型文件存在或联系管理员"
        }
        raise HTTPException(status_code=500, detail=json.dumps(error_detail))
        
    logger.info(f"使用指定模型: {model_path}")
    
    # 获取上传文件的绝对路径
    try:
        absolute_path = get_upload_file_path(java_path)
        logger.info(f"上传文件的绝对路径: {absolute_path}")
    except Exception as e:
        error_message = f"获取上传文件路径失败: {str(e)}"
        logger.error(error_message)
        raise HTTPException(status_code=400, detail=error_message)
    
    # 如果文件不存在，返回错误
    if not os.path.exists(absolute_path):
        error_message = f"指定的文件不存在: {absolute_path}"
        logger.error(error_message)
        raise HTTPException(status_code=400, detail=error_message)
    
    # 解析文件名和扩展名
    _, file_name = os.path.split(absolute_path)
    dataset_name = os.path.splitext(file_name)[0]
    logger.info(f"数据集名称: {dataset_name}")
    
    # 创建输出目录 (使用时间戳避免冲突)
    output_dir = os.path.join(STATIC_DIR, "processed", f"{dataset_name}_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"创建输出目录: {output_dir}")
    
    # 设置数据集目录
    dataset_dir = os.path.join(STATIC_DIR, "datasets", f"{dataset_name}_{timestamp}")
    
    # 如果数据集目录已存在，则删除它 (可能是之前处理失败的残留)
    if os.path.exists(dataset_dir):
        logger.warning(f"数据集目录已存在，将被删除: {dataset_dir}")
        shutil.rmtree(dataset_dir)
    
    os.makedirs(dataset_dir, exist_ok=True)
    logger.info(f"创建数据集目录: {dataset_dir}")
    
    # 如果是ZIP文件，解压到数据集目录
    if absolute_path.lower().endswith('.zip'):
        logger.info(f"正在解压ZIP文件: {absolute_path}")
        try:
            with zipfile.ZipFile(absolute_path, 'r') as zip_ref:
                zip_ref.extractall(dataset_dir)
            logger.info("ZIP文件解压完成")
        except Exception as e:
            error_message = f"解压ZIP文件失败: {str(e)}"
            logger.error(error_message)
            raise HTTPException(status_code=500, detail=error_message)
    else:
        # 如果不是ZIP文件，直接复制到数据集目录
        logger.info(f"复制文件到数据集目录: {absolute_path} -> {dataset_dir}")
        shutil.copy(absolute_path, dataset_dir)
    
    # 执行处理逻辑
    try:
        logger.info(f"开始处理数据集: {dataset_dir}, 环境: {environment}, 模型: {model_name}, 输出目录: {output_dir}")
        logger.info(f"===== 处理前环境检查 =====")
        logger.info(f"- 请求的环境: {environment}")
        logger.info(f"- 选择的模型: {model_name}")
        logger.info(f"- 模型文件路径: {model_path}")
        
        # 确认模型文件的唯一性
        if os.path.exists(model_path):
            dark_model_path = os.path.join(BASE_DIR, 'checkpoints', 'darkBA_pix2pix', 'latest_net_G.pth')
            shallow_model_path = os.path.join(BASE_DIR, 'checkpoints', 'shallowBA_pix2pix', 'latest_net_G.pth')
            
            if os.path.exists(dark_model_path) and os.path.exists(shallow_model_path):
                # 计算深水模型哈希值
                with open(dark_model_path, 'rb') as f:
                    dark_hash = hashlib.md5(f.read()).hexdigest()
                
                # 计算浅水模型哈希值
                with open(shallow_model_path, 'rb') as f:
                    shallow_hash = hashlib.md5(f.read()).hexdigest()
                
                logger.info(f"- 深水模型哈希值: {dark_hash}")
                logger.info(f"- 浅水模型哈希值: {shallow_hash}")
                
                if dark_hash == shallow_hash:
                    logger.error("警告: 深水模型和浅水模型哈希值相同，它们是同一个文件！这会导致两种环境效果相同！")
        
        # 调用处理函数，明确传递模型名称
        is_success = process_dataset(dataset_dir, output_dir, model_name=model_name)
        
        if is_success:
            logger.info("数据集处理成功")
            
            # 创建ZIP文件
            zip_filename = f"{dataset_name}_processed_{timestamp}.zip"
            zip_path = os.path.join(output_dir, zip_filename)
            
            logger.info(f"开始创建ZIP文件: {zip_path}")
            shutil.make_archive(
                os.path.join(output_dir, f"{dataset_name}_processed"), 
                'zip', 
                output_dir
            )
            
            # 重命名ZIP文件以匹配预期的名称
            final_zip_path = os.path.join(output_dir, zip_filename)
            os.rename(os.path.join(output_dir, f"{dataset_name}_processed.zip"), final_zip_path)
            
            logger.info(f"ZIP文件创建完成: {final_zip_path}")
            
            # 返回相对路径 (相对于static目录)
            relative_path = os.path.join("processed", f"{dataset_name}_{timestamp}", zip_filename)
            logger.info(f"返回相对路径: {relative_path}")
            
            return {"outputPath": relative_path}
        else:
            error_message = "数据集处理失败，未知错误"
            logger.error(error_message)
            raise HTTPException(status_code=500, detail=error_message)
    except Exception as e:
        error_message = f"处理数据集时发生错误: {str(e)}"
        logger.error(error_message)
        logger.exception(e)
        raise HTTPException(status_code=500, detail=error_message)

@app.get("/api/dataset/download/{filename:path}")
async def download_preprocess(filename: str):
    """下载预处理后的数据集"""
    try:
        # 移除路径中的 'static/processed/' 前缀
        filename = filename.replace('static/processed/', '')
        
        # 构建完整的文件路径
        file_path = os.path.join(PROCESSED_DIR, filename)
        force_print(f"Downloading file from: {file_path}")
        
        if not os.path.exists(file_path):
            force_print(f"File not found: {file_path}")
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
            
        return FileResponse(
            file_path,
            media_type='application/zip',
            filename=filename
            )
    except Exception as e:
        force_print(f"Error downloading file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/api/datasetprocess/download/{filename:path}")
async def download_process(filename: str):
    """下载处理后的数据集"""
    try:
        # 移除路径中的 'static1/processed/' 前缀
        filename = filename.replace('static1/processed/', '')
        
        # 构建完整的文件路径
        file_path = os.path.join(PROCESSED1_DIR, filename)
        force_print(f"Downloading file from: {file_path}")
        
        if not os.path.exists(file_path):
            force_print(f"File not found: {file_path}")
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
            
        return FileResponse(
            file_path,
            media_type='application/zip',
            filename=filename
        )
    except Exception as e:
        force_print(f"Error downloading file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/api/datasetprocess/preview/{dataset_id}")
async def get_preview_images(dataset_id: str):
    """获取数据集预览图片"""
    try:
        logger.info(f"Getting preview images for dataset: {dataset_id}")
        
        # 构建目录路径
        dataset_dir = os.path.join(DATASET_DIR, dataset_id)
        processed_dir = os.path.join(PROCESSED_DIR, f"{dataset_id}_processed")
        
        logger.info(f"Looking for original images in: {dataset_dir}")
        logger.info(f"Looking for processed images in: {processed_dir}")
        
        if not os.path.exists(dataset_dir) or not os.path.exists(processed_dir):
            logger.error(f"Dataset directory exists: {os.path.exists(dataset_dir)}")
            logger.error(f"Processed directory exists: {os.path.exists(processed_dir)}")
            raise HTTPException(
                status_code=404,
                detail="Dataset or processed directory not found"
            )
            
        # 获取所有图片
        preview_pairs = []
        error_images = []
        
        # 遍历原始图片目录
        for root, _, files in os.walk(dataset_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    # 获取相对路径
                    rel_path = os.path.relpath(os.path.join(root, file), dataset_dir)
                    
                    # 构建对应的处理后图片路径
                    processed_path = os.path.join(processed_dir, rel_path)
                    
                    if os.path.exists(processed_path):
                        preview_pairs.append({
                            "original": f"/static/datasets/{dataset_id}/{rel_path}",
                            "processed": f"/static/processed/{dataset_id}_processed/{rel_path}"
                        })
                    else:
                        error_images.append({
                            "file": rel_path,
                            "message": "处理失败"
                        })
                        
        logger.info(f"Found {len(preview_pairs)} preview pairs")
        logger.info(f"Found {len(error_images)} error images")
        
        if not preview_pairs and not error_images:
            raise HTTPException(
                status_code=404,
                detail="No images found"
            )
            
        return {
            "status": "success",
            "previewPairs": preview_pairs[:10],  # 限制最多10张预览图
            "errorImages": error_images
        }
        
    except Exception as e:
        logger.error(f"Error getting preview images: {str(e)}")
        logger.error("Stack trace:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/api/dataset/test")
async def test():
    """测试接口 - 用于检查服务是否正常运行"""
    return {
        'status': 'success',
        'message': 'Python service is running'
    }

def get_upload_file_path(java_path):
    """
    根据传入的文件路径获取实际的文件路径
    现在只查找本地uploads目录，不再依赖Java项目路径
    """
    logger.info(f"Resolving file path for: {java_path}")
    
    if not java_path:
        return None
    
    # 提取基本文件名
    file_name = os.path.basename(java_path)
    
    # 直接在uploads目录中查找
    file_path = os.path.join(UPLOADS_DIR, file_name)
    if os.path.exists(file_path):
        logger.info(f"Found file at: {file_path}")
        return file_path
    
    # 尝试查找在子目录中
    for root, dirs, files in os.walk(UPLOADS_DIR):
        for file in files:
            if file == file_name:
                full_path = os.path.join(root, file)
                logger.info(f"Found file in subdirectory: {full_path}")
                return full_path
    
    logger.warning(f"File not found: {file_name}")
    return None

@app.post("/api/dataset/datasetprocess")
async def dataset_process_endpoint(
    file: UploadFile = File(None),
    environment: str = Form(None)
):
    """新增端点，处理来自Vue前端的数据集处理请求"""
    try:
        logger.info(f"接收到/api/dataset/datasetprocess请求，环境参数: {environment}")
        
        # 保存上传的文件
        if not file:
            logger.error("未提供文件")
            raise HTTPException(status_code=400, detail="必须提供文件上传")
        
        # 获取时间戳
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # 保存文件到uploads目录
        file_name = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOADS_DIR, file_name)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            logger.info(f"文件已保存到: {file_path}，大小: {len(content)} bytes")
        
        # 创建处理请求对象
        process_request = DatasetProcessRequest(
            datasetPath=f"./uploads/{file_name}",
            environment=environment or "deep"
        )
        
        # 调用现有的处理函数
        result = await process_dataset_handler(process_request)
        logger.info(f"处理结果: {result}")
        
        # 返回结果
        return {
            "status": "success",
            "message": "数据集处理完成",
            "path": f"/static/{result.get('outputPath')}" if isinstance(result, dict) and "outputPath" in result else None
        }
    except HTTPException as e:
        # 重新抛出HTTPException
        raise e
    except Exception as e:
        logger.error(f"处理数据集失败: {str(e)}")
        logger.error("Stack trace:", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

def main():
    """主函数 - 启动服务器"""
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info",
        access_log=True,
        use_colors=True
    )

if __name__ == "__main__":
    main()
