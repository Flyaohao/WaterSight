import torch
import os
import sys
from pathlib import Path
import cv2
from datetime import datetime
import yaml
import numpy as np
from PIL import Image

def detect_fish(image_path):
    try:
        print("Starting fish detection...")
        # 获取当前文件的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        
        print(f"Current directory: {current_dir}")
        print(f"Parent directory: {parent_dir}")
        
        # 添加父目录到系统路径
        if parent_dir not in sys.path:
            sys.path.append(parent_dir)
            
        # 加载模型配置文件
        data_yaml = os.path.join(current_dir, 'weights', 'fish', 'data.yaml')
        with open(data_yaml, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            class_names = data['names']  # 获取所有鱼类名称
        
        print(f"Loaded class names: {class_names}")
            
        # 加载完整的鱼类检测模型
        weights_path = os.path.join(current_dir, 'weights', 'fish', 'best.pt')
        print(f"Loading model from: {weights_path}")
        model = torch.hub.load(parent_dir, 'custom', path=weights_path, source='local')
        
        # 设置模型参数
        model.conf = 0.25  # 置信度阈值
        model.iou = 0.45   # NMS IOU阈值
        model.classes = None  # 检测所有类别
        
        # 进行检测
        print(f"Running detection on image: {image_path}")
        results = model(image_path)
        
        # 生成带时间戳的结果文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        original_filename = os.path.splitext(os.path.basename(image_path))[0]
        result_filename = f"fish_{original_filename}_{timestamp}.jpg"
        results_dir = os.path.join(current_dir, 'results')
        
        print(f"Result directory: {results_dir}")
        print(f"Result filename: {result_filename}")
        
        # 确保结果目录存在
        os.makedirs(results_dir, exist_ok=True)
        
        # 保存结果
        save_path = os.path.join(results_dir, result_filename)
        print(f"Saving result to: {save_path}")
        
        # 使用 PIL 读取图像
        try:
            pil_image = Image.open(image_path)
            # 转换为 RGB 模式（如果是 RGBA，去掉 alpha 通道）
            if pil_image.mode == 'RGBA':
                pil_image = pil_image.convert('RGB')
            # 转换为 numpy 数组
            im0 = np.array(pil_image)
            # 转换颜色空间从 RGB 到 BGR（OpenCV 使用 BGR）
            im0 = cv2.cvtColor(im0, cv2.COLOR_RGB2BGR)
            print(f"Successfully read image with shape: {im0.shape}")
        except Exception as e:
            print(f"Error reading image with PIL: {str(e)}")
            print(f"Image file exists: {os.path.exists(image_path)}")
            print(f"Image file size: {os.path.getsize(image_path) if os.path.exists(image_path) else 'N/A'}")
            raise Exception(f"Failed to read image from {image_path}")
        
        # 统计检测结果和置信度
        detections = {}
        confidence_scores = {}
        for det in results.pred[0]:
            if det is not None and len(det):
                *xyxy, conf, cls = det
                cls_name = class_names[int(cls)]
                detections[cls_name] = detections.get(cls_name, 0) + 1
                # 更新置信度（如果有多个同类目标，取最高置信度）
                if cls_name not in confidence_scores or conf > confidence_scores[cls_name]:
                    confidence_scores[cls_name] = float(conf)
                
                # 获取边界框坐标、置信度和类别
                *xyxy, conf, cls = det
                # 转换为整数坐标
                x1, y1, x2, y2 = map(int, xyxy)
                # 绘制边界框
                cv2.rectangle(im0, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # 添加标签（类别名称和置信度）
                label = f'{cls_name} {conf:.2f}'
                # 计算标签的位置和大小
                (label_width, label_height), baseline = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                # 绘制标签背景
                cv2.rectangle(im0, (x1, y1 - label_height - 10),
                            (x1 + label_width, y1), (0, 255, 0), -1)
                # 绘制标签文本
                cv2.putText(im0, label, (x1, y1 - 10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        # 保存结果图像
        try:
            print(f"Attempting to save image with shape {im0.shape} to {save_path}")
            # 确保图像数据是有效的
            if im0 is None or im0.size == 0:
                raise ValueError("Image data is empty")
            
            # 确保目标目录存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # 将 BGR 转换为 RGB（PIL 使用 RGB）
            rgb_image = cv2.cvtColor(im0, cv2.COLOR_BGR2RGB)
            
            # 转换为 PIL Image
            pil_image = Image.fromarray(rgb_image)
            
            # 保存图像
            pil_image.save(save_path, format='JPEG', quality=95)
            
            print(f"Successfully saved result image to: {save_path}")
            print(f"File exists: {os.path.exists(save_path)}")
            print(f"File size: {os.path.getsize(save_path) if os.path.exists(save_path) else 'N/A'}")
        except Exception as e:
            print(f"Error saving result image: {str(e)}")
            raise
        
        print("Detection completed successfully")
        return result_filename, detections, confidence_scores
    except Exception as e:
        print(f"Error in detect_fish: {str(e)}")
        import traceback
        traceback.print_exc()
        raise e
