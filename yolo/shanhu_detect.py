import torch
import os

def detect_shanhu(image_path):
    # 加载模型
    model = torch.hub.load('.', 'custom', path='check/weights/shanhu/best.pt', source='local')
    
    # 进行检测
    results = model(image_path)
    
    # 保存结果
    result_path = os.path.join('results', 'shanhu_' + os.path.basename(image_path))
    results.save(result_path)
    
    return result_path 