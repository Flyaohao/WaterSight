import warnings
warnings.filterwarnings('ignore', message='loaded more than 1 DLL from .libs:')

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
import sys
from typing import Dict, List
from pydantic import BaseModel
import glob
import time

# 获取当前目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# 添加必要的路径
if current_dir not in sys.path:
    sys.path.append(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# 从当前目录导入检测模块
from fish_detect import detect_fish
from shanhu_detect import detect_shanhu

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

# 创建上传和结果目录（使用相对路径）
UPLOAD_DIR = os.path.join("uploads")
RESULT_DIR = os.path.join("results")

# 确保目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

def clean_directory(directory: str, keep_latest: int = 10):
    """
    清理指定目录，只保留最近的N个文件
    :param directory: 要清理的目录路径
    :param keep_latest: 保留最近的文件数量
    """
    try:
        # 获取目录中的所有文件
        files = []
        for file_path in glob.glob(os.path.join(directory, '*')):
            # 获取文件的修改时间和创建时间，使用较早的那个时间
            mtime = os.path.getmtime(file_path)
            ctime = os.path.getctime(file_path)
            timestamp = min(mtime, ctime)
            files.append((file_path, timestamp))
        
        # 按时间排序
        files.sort(key=lambda x: x[1], reverse=True)
        
        # 删除旧文件
        for file_path, _ in files[keep_latest:]:
            try:
                os.remove(file_path)
                print(f"Cleaned up old file: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"Error deleting file {os.path.basename(file_path)}: {e}")
                
    except Exception as e:
        print(f"Error cleaning directory {os.path.basename(directory)}: {e}")

def clean_all_directories():
    """
    清理所有需要维护的目录
    """
    clean_directory(UPLOAD_DIR)
    clean_directory(RESULT_DIR)

# 确保目录有写入权限
def ensure_dir_permissions(directory):
    try:
        # 检查目录是否存在
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # 设置目录权限
        os.chmod(directory, 0o777)
        
        # 设置所有子文件和子目录的权限
        for root, dirs, files in os.walk(directory):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0o777)
            for f in files:
                os.chmod(os.path.join(root, f), 0o777)
                
        print(f"Successfully set permissions for {os.path.basename(directory)}")
    except Exception as e:
        print(f"Warning: Could not set permissions for {os.path.basename(directory)}: {e}")

# 设置目录权限
ensure_dir_permissions(UPLOAD_DIR)
ensure_dir_permissions(RESULT_DIR)

# 挂载静态文件目录
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR, html=True), name="uploads")
app.mount("/results", StaticFiles(directory=RESULT_DIR, html=True), name="results")

# 添加一个辅助路由来获取图像
@app.get("/image/{image_type}/{image_name}")
async def get_image(image_type: str, image_name: str):
    if image_type == "uploads":
        image_path = os.path.join(UPLOAD_DIR, image_name)
    elif image_type == "results":
        image_path = os.path.join(RESULT_DIR, image_name)
    else:
        raise HTTPException(status_code=400, detail="Invalid image type")
    
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(image_path)

# 定义响应数据模型
class DetectionResult(BaseModel):
    original: str
    result: str
    detections: Dict[str, dict]  # 修改为包含更多信息的字典
    details: Dict[str, dict]

@app.post("/detect/fish")
async def detect_fish_image(file: UploadFile = File(...)):
    try:
        # 先清理目录
        clean_all_directories()
        
        # 保存上传的图片
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"Saved uploaded file to: {file_path}")
        
        # 调用检测函数
        result_filename, detections, confidence_scores = detect_fish(file_path)
        
        # 获取鱼类详细信息
        fish_details = {
            "AngelFish": {
                "name": "神仙鱼",
                "name_en": "Angel Fish",
                "description": "神仙鱼体型优美，色彩艳丽，是最受欢迎的热带鱼之一。体侧扁，背鳍和臀鳍延长。",
                "care_guide": """
                    温度：24-28℃
                    pH值：8.0-8.4
                    盐度：1.020-1.025
                    饲养建议：
                    - 需要较大的水族箱
                    - 注意水质管理
                    - 食性：杂食性
                    - 部分品种较具攻击性
                """,
                "difficulty": "中等",

            },
            "BlueTang": {
                "name": "蓝倒吊",
                "name_en": "Blue Tang",
                "description": "蓝倒吊鱼体色鲜艳，以其明亮的蓝色体色和黄色尾鳍而闻名，是《海底总动员》中多莉的原型。",
                "care_guide": """
                    温度：24-26℃
                    pH值：8.1-8.4
                    盐度：1.020-1.025
                    饲养建议：
                    - 需要大型水族箱（至少75加仑）
                    - 充足的游泳空间
                    - 食性：主要食藻类
                    - 性格温和但较敏感
                """,
                "difficulty": "较难",
            },
            "ButterflyFish": {
                "name": "蝴蝶鱼",
                "name_en": "Butterfly Fish",
                "description": "蝴蝶鱼体型扁平，体色鲜艳，游姿优美，是珊瑚礁中最漂亮的鱼类之一。",
                "care_guide": """
                    温度：24-28℃
                    pH值：8.1-8.4
                    盐度：1.020-1.025
                    饲养建议：
                    - 需要充足的游泳空间
                    - 适合珊瑚礁缸饲养
                    - 食性：浮游生物、藻类
                    - 性格温和，适合群居
                """,
                "difficulty": "中等",
            },
            "ClownFish": {
                "name": "小丑鱼",
                "name_en": "Clown Fish",
                "description": "小丑鱼以其鲜艳的橙色体色和白色条纹而闻名，常与海葵共生，是最受欢迎的海水观赏鱼之一。",
                "care_guide": """
                    温度：23-28℃
                    pH值：8.0-8.4
                    盐度：1.020-1.025
                    饲养建议：
                    - 适合初学者饲养
                    - 需要配备海葵
                    - 性格活泼好动
                    - 建议两两饲养
                """,
                "difficulty": "简单",
            },
            "GoldFish": {
                "name": "金鱼",
                "name_en": "Gold Fish",
                "description": "金鱼是最古老的观赏鱼之一，品种繁多，体型和颜色变化丰富。",
                "care_guide": """
                    温度：18-22℃
                    pH值：6.5-7.5
                    水质：软水至中性水
                    饲养建议：
                    - 需要良好的过滤系统
                    - 避免过度喂食
                    - 定期换水
                    - 适合群养
                """,
                "difficulty": "简单",
            },
            "Gourami": {
                "name": "斗鱼",
                "name_en": "Gourami",
                "description": "斗鱼有特殊的迷宫器官可以呼吸空气，体色艳丽，种类众多。",
                "care_guide": """
                    温度：24-28℃
                    pH值：6.0-7.5
                    水质：软水至中性水
                    饲养建议：
                    - 需要水面空间
                    - 提供漂浮植物
                    - 性格较温和
                    - 注意同类相斗
                """,
                "difficulty": "简单",
            },
            "MorishIdol": {
                "name": "摩里斯神仙",
                "name_en": "Moorish Idol",
                "description": "摩里斯神仙因其独特的长背鳍和黑白相间的体色而闻名，是珊瑚礁中最优雅的鱼类之一。",
                "care_guide": """
                    温度：24-28℃
                    pH值：8.1-8.4
                    盐度：1.020-1.025
                    饲养建议：
                    - 需要大型水族箱
                    - 专业饲养技巧
                    - 食性较挑剔
                    - 对环境要求高
                """,
                "difficulty": "专业",
            },
            "PlatyFish": {
                "name": "剑尾鱼",
                "name_en": "Platy Fish",
                "description": "剑尾鱼体型小巧，色彩丰富，繁殖能力强，是受欢迎的淡水观赏鱼。",
                "care_guide": """
                    温度：20-26℃
                    pH值：7.0-8.0
                    水质：中性偏硬水
                    饲养建议：
                    - 适合小型鱼缸
                    - 易于繁殖
                    - 性格活泼
                    - 群居性强
                """,
                "difficulty": "简单",
            },
            "RibbonedSweetlips": {
                "name": "条纹甜唇鱼",
                "name_en": "Ribboned Sweetlips",
                "description": "条纹甜唇鱼体型优美，有独特的条纹图案，是珊瑚礁中引人注目的鱼类。",
                "care_guide": """
                    温度：24-26℃
                    pH值：8.1-8.4
                    盐度：1.020-1.025
                    饲养建议：
                    - 需要大型水族箱
                    - 提供躲藏场所
                    - 食性：小型甲壳类
                    - 性格较胆小
                """,
                "difficulty": "较难",
            },
            "ThreeStripedDamselfish": {
                "name": "三带雀鲷",
                "name_en": "Three Striped Damselfish",
                "description": "三带雀鲷体型小巧，有三条明显的垂直条纹，是典型的珊瑚礁鱼类。",
                "care_guide": """
                    温度：24-28℃
                    pH值：8.1-8.4
                    盐度：1.020-1.025
                    饲养建议：
                    - 适合各种规格鱼缸
                    - 较具攻击性
                    - 食性：杂食性
                    - 耐受力强
                """,
                "difficulty": "简单",
            },
            "YellowCichlid": {
                "name": "黄丽鱼",
                "name_en": "Yellow Cichlid",
                "description": "黄丽鱼体色鲜艳，性格活泼，是受欢迎的热带鱼之一。",
                "care_guide": """
                    温度：24-28℃
                    pH值：7.5-8.5
                    水质：偏硬水
                    饲养建议：
                    - 需要领地空间
                    - 注意种群配置
                    - 食性：杂食性
                    - 具有攻击性
                """,
                "difficulty": "中等",
            },
            "YellowTang": {
                "name": "黄燕尾鱼",
                "name_en": "Yellow Tang",
                "description": "黄燕尾鱼全身鲜艳的黄色，是最受欢迎的海水观赏鱼之一。",
                "care_guide": """
                    温度：24-26℃
                    pH值：8.1-8.4
                    盐度：1.020-1.025
                    饲养建议：
                    - 需要大型水族箱
                    - 充足的游泳空间
                    - 食性：藻类为主
                    - 适合珊瑚礁缸
                """,
                "difficulty": "中等",
            },
            "ZebraFish": {
                "name": "斑马鱼",
                "name_en": "Zebra Fish",
                "description": "斑马鱼体型小巧，有明显的水平条纹，是常见的观赏鱼和实验鱼类。",
                "care_guide": """
                    温度：20-26℃
                    pH值：6.8-7.8
                    水质：中性水
                    饲养建议：
                    - 适合小型鱼缸
                    - 群居性强
                    - 性格活泼
                    - 易于饲养
                """,
                "difficulty": "简单",
            }
        }
        
        # 处理检测结果，添加更多信息
        enhanced_detections = {}
        for fish_type, count in detections.items():
            if fish_type in fish_details:
                enhanced_detections[fish_type] = {
                    "count": count,
                    "name_zh": fish_details[fish_type]["name"],
                    "confidence": confidence_scores.get(fish_type, 0.0),
                    "iou": None  # 如果需要IOU分数，可以从检测结果中获取
                }
        
        return DetectionResult(
            original=f"/uploads/{file.filename}",
            result=f"/results/{result_filename}",
            detections=enhanced_detections,
            details=fish_details
        )
    except Exception as e:
        print(f"Error in detect_fish_image: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/detect/shanhu")
async def detect_shanhu_image(file: UploadFile = File(...)):
    try:
        # 先清理目录
        clean_all_directories()
        
        # 保存上传的图片
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"Saved uploaded file to: {file_path}")
        
        # 调用检测函数
        result_filename, detections, confidence_scores = detect_shanhu(file_path)
        
        # 获取珊瑚详细信息
        coral_details = {
            "starfish": {
                "name": "海星",
                "name_en": "Starfish",
                "description": "海星是一种常见的棘皮动物，形状像星星，通常有五个辐射对称的臂。它们在珊瑚礁生态系统中扮演着重要角色。",
                "care_guide": """
                    温度：22-26℃
                    pH值：8.1-8.4
                    盐度：1.020-1.025
                    饲养建议：
                    - 需要充足的底砂面积
                    - 水质要求较高
                    - 避免与其他底栖生物竞争
                    - 注意投喂量
                """,
                "difficulty": "中等",
                "ecological_role": """
                    生态作用：
                    - 控制珊瑚礁生态平衡
                    - 清理底部有机物
                    - 分解者角色
                    - 食物链中的重要一环
                """,
                "conservation_status": "需要保护",
                "habitat": "珊瑚礁区域、岩石海底"
            }
            # 如果有更多珊瑚或海洋生物类型，可以在这里添加
        }
        
        # 处理检测结果，添加更多信息
        enhanced_detections = {}
        for coral_type, count in detections.items():
            if coral_type in coral_details:
                enhanced_detections[coral_type] = {
                    "count": count,
                    "name_zh": coral_details[coral_type]["name"],
                    "confidence": confidence_scores.get(coral_type, 0.0),
                    "iou": None  # 如果需要IOU分数，可以从检测结果中获取
                }
        
        return DetectionResult(
            original=f"/uploads/{file.filename}",
            result=f"/results/{result_filename}",
            detections=enhanced_detections,
            details=coral_details
        )
    except Exception as e:
        print(f"Error in detect_shanhu_image: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)