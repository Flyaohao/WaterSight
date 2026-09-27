from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
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
)

# 创建上传和结果目录
UPLOAD_DIR = "uploads"
RESULT_DIR = "results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

@app.post("/detect/fish")
async def detect_fish_image(file: UploadFile = File(...)):
    # 保存上传的图片
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 调用检测函数
    result_path = detect_fish(file_path)
    
    return {
        "original": f"/image/{file.filename}",
        "result": f"/image/{os.path.basename(result_path)}"
    }

@app.post("/detect/shanhu")
async def detect_shanhu_image(file: UploadFile = File(...)):
    # 保存上传的图片
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 调用检测函数
    result_path = detect_shanhu(file_path)
    
    return {
        "original": f"/image/{file.filename}",
        "result": f"/image/{os.path.basename(result_path)}"
    }

@app.get("/image/{image_name}")
async def get_image(image_name: str):
    # 先检查结果目录
    result_path = os.path.join(RESULT_DIR, image_name)
    if os.path.exists(result_path):
        return FileResponse(result_path)
    
    # 再检查上传目录
    upload_path = os.path.join(UPLOAD_DIR, image_name)
    if os.path.exists(upload_path):
        return FileResponse(upload_path)
    
    return {"error": "Image not found"} 