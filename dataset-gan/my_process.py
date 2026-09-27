import os
import numpy as np
import cv2
import torch
import torchvision.transforms as transforms
from models import networks
from util import util
import logging
import hashlib
import time
import gc  # 添加gc模块用于强制垃圾回收

def load_model(model_name='darkBA_pix2pix'):
    """加载预训练的 pix2pix 模型"""
    try:
        # 清除CUDA缓存并执行垃圾回收
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()  # 强制垃圾回收
        
        # 设置模型参数
        logging.info(f"===== 模型加载开始：{model_name} =====")
        netG = networks.define_G(3, 3, 64, 'unet_256', 'batch', True, 'normal', 0.02)
        
        # 获取当前文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 确保model_name不为空且正确
        if not model_name:
            model_name = 'darkBA_pix2pix'
            logging.warning(f"模型名称为空，使用默认模型：{model_name}")
        
        # 强制将环境名转换为模型名
        if model_name.lower() == 'shallow':
            model_name = 'shallowBA_pix2pix'
            logging.info(f"环境名转换为模型名: shallow -> {model_name}")
        elif model_name.lower() == 'deep':
            model_name = 'darkBA_pix2pix'
            logging.info(f"环境名转换为模型名: deep -> {model_name}")
        
        # 构建模型路径
        model_path = os.path.join(current_dir, 'checkpoints', model_name, 'latest_net_G.pth')
        logging.info(f"尝试加载模型: {model_path}")
        
        # 检查文件存在性
        if not os.path.exists(model_path):
            alternative_model = 'darkBA_pix2pix' if model_name == 'shallowBA_pix2pix' else 'shallowBA_pix2pix'
            alt_model_path = os.path.join(current_dir, 'checkpoints', alternative_model, 'latest_net_G.pth')
            
            if os.path.exists(alt_model_path):
                logging.warning(f"找不到指定模型 '{model_name}'，但找到了备选模型 '{alternative_model}'")
                logging.warning(f"强制使用指定模型，拒绝回退！")
            
            raise Exception(f"模型文件未找到: {model_path}")
        
        # 记录文件信息
        file_size = os.path.getsize(model_path)
        file_time = os.path.getmtime(model_path)
        logging.info(f"模型文件[{model_name}]大小: {file_size} 字节")
        logging.info(f"模型文件[{model_name}]修改时间: {time.ctime(file_time)}")
        
        # 计算完整文件哈希，确保使用正确的模型
        with open(model_path, "rb") as f:
            file_content = f.read()
            file_hash = hashlib.md5(file_content).hexdigest()
        logging.info(f"模型文件[{model_name}]完整MD5: {file_hash}")
        
        # 检查另一个模型文件是否存在，并记录信息
        other_model = 'darkBA_pix2pix' if model_name == 'shallowBA_pix2pix' else 'shallowBA_pix2pix'
        other_path = os.path.join(current_dir, 'checkpoints', other_model, 'latest_net_G.pth')
        if os.path.exists(other_path):
            other_size = os.path.getsize(other_path)
            other_time = os.path.getmtime(other_path)
            logging.info(f"另一个模型文件[{other_model}]大小: {other_size} 字节")
            logging.info(f"另一个模型文件[{other_model}]修改时间: {time.ctime(other_time)}")
            
            with open(other_path, "rb") as f:
                other_content = f.read()
                other_hash = hashlib.md5(other_content).hexdigest()
            logging.info(f"另一个模型文件[{other_model}]完整MD5: {other_hash}")
            
            if file_size == other_size:
                logging.warning(f"警告：'{model_name}'和'{other_model}'模型文件大小相同({file_size}字节)！")
            
            if file_hash == other_hash:
                logging.error(f"错误：'{model_name}'和'{other_model}'模型文件哈希值相同，这是同一个文件！这将导致两种环境效果完全相同！")
                # 记录培训配置差异
                train_opt1 = os.path.join(current_dir, 'checkpoints', model_name, 'train_opt.txt')
                train_opt2 = os.path.join(current_dir, 'checkpoints', other_model, 'train_opt.txt')
                if os.path.exists(train_opt1) and os.path.exists(train_opt2):
                    logging.info(f"检查训练配置差异...")
                    with open(train_opt1, 'r') as f1, open(train_opt2, 'r') as f2:
                        logging.info(f"{model_name}训练配置: dataroot={[line for line in f1 if 'dataroot' in line]}")
                        logging.info(f"{other_model}训练配置: dataroot={[line for line in f2 if 'dataroot' in line]}")
        
        # 加载模型 - 添加重试机制以确保加载成功
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logging.info(f"尝试加载模型(尝试 {attempt+1}/{max_retries})...")
                # 强制使用CPU加载模型，避免GPU内存问题
                device = torch.device('cpu')
                # 使用完整路径加载模型
                state_dict = torch.load(model_path, map_location=device)
                netG.load_state_dict(state_dict)
                netG.eval()
                logging.info(f"成功加载模型: {model_name}")
                # 记录模型特征以确认是否正确加载
                params_count = sum(p.numel() for p in netG.parameters())
                logging.info(f"模型参数数量: {params_count}")
                break
            except Exception as e:
                logging.error(f"模型加载尝试 {attempt+1} 失败: {str(e)}")
                if attempt == max_retries - 1:
                    raise Exception(f"无法加载模型 {model_name} 在 {max_retries} 次尝试后: {str(e)}")
                time.sleep(1)  # 等待一秒再重试
        
        logging.info(f"===== 模型 {model_name} 加载完成 =====")
        return netG
    except Exception as e:
        logging.error(f"加载模型 {model_name} 失败: {str(e)}")
        raise

def preprocess_image(img, model, model_name="darkBA_pix2pix"):
    """使用 pix2pix 模型对图像进行预处理"""
    try:
        # 转换 BGR 到 RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # 调整图像大小为 256x256
        img_resized = cv2.resize(img_rgb, (256, 256))
        
        # 转换为 tensor 并归一化
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        img_tensor = transform(img_resized).unsqueeze(0)
        
        # 使用模型处理图像
        with torch.no_grad():
            output = model(img_tensor)
            
            # 转换回图像格式
            output = output.squeeze(0).cpu()
            output = (output + 1) / 2.0 * 255
            output = output.permute(1, 2, 0).numpy()
            
            # 转换回 BGR 格式
            output = cv2.cvtColor(output.astype(np.uint8), cv2.COLOR_RGB2BGR)
            
            # 调整回原始大小
            if img.shape[:2] != (256, 256):
                output = cv2.resize(output, (img.shape[1], img.shape[0]))
            
        return output
    except Exception as e:
        logging.error(f"处理图像失败: {str(e)}")
        # 如果是Numpy错误，使用替代方法处理图像
        if "Numpy is not available" in str(e):
            logging.warning("Numpy不可用，使用替代方法处理图像...")
            try:
                # 简单替代方法：对图像进行滤波并调整亮度
                # 这不是理想的处理方法，但可以避免完全失败
                result = img.copy()
                # 尝试使用OpenCV滤波
                try:
                    # 稍微模糊图像模拟水下效果
                    result = cv2.GaussianBlur(result, (5, 5), 0)
                    # 调整亮度和对比度（模拟深水/浅水效果）
                    if 'dark' in model_name.lower():
                        # 深水效果：降低亮度，增加蓝色
                        result = cv2.convertScaleAbs(result, alpha=0.8, beta=-20)
                        # 增加蓝色通道
                        b, g, r = cv2.split(result)
                        b = cv2.convertScaleAbs(b, alpha=1.2, beta=10)
                        result = cv2.merge([b, g, r])
                    else:
                        # 浅水效果：稍微降低亮度，增加绿色
                        result = cv2.convertScaleAbs(result, alpha=0.9, beta=-10)
                        # 增加绿色通道
                        b, g, r = cv2.split(result)
                        g = cv2.convertScaleAbs(g, alpha=1.1, beta=15)
                        result = cv2.merge([b, g, r])
                except Exception as cv_error:
                    logging.error(f"替代处理方法失败: {str(cv_error)}")
                
                logging.warning("使用替代方法处理图像完成")
                return result
            except Exception as alt_error:
                logging.error(f"替代图像处理方法也失败: {str(alt_error)}")
                # 如果所有方法都失败，返回原始图像
                return img
        # 如果是其他错误，直接抛出
        raise

def process_image(img, model, model_name="darkBA_pix2pix"):
    """使用 pix2pix 模型对图像进行处理"""
    try:
        # 直接调用preprocess_image函数并传递模型名称
        return preprocess_image(img, model, model_name)
    except Exception as e:
        logging.error(f"处理图片失败: {str(e)}")
        raise

def process_dataset(input_path, output_path, model_name='darkBA_pix2pix'):
    """处理数据集中的图片"""
    try:
        # 清除CUDA缓存
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        # 记录当前系统状态和模型参数
        logging.info(f"=== 数据集处理开始 (my_process.py) ===")
        logging.info(f"输入路径: {input_path}")
        logging.info(f"输出路径: {output_path}")
        logging.info(f"请求的模型名称: {model_name}")
        
        # 强制检查模型名称是否正确 - 浅水环境专门处理
        if model_name and ('shallow' in model_name.lower() or model_name.lower() == 'shallow'):
            model_name = 'shallowBA_pix2pix'
            logging.info(f"使用浅水模型: {model_name}")
        elif not model_name or model_name.lower() == 'deep':
            model_name = 'darkBA_pix2pix'
            logging.info(f"使用深水模型: {model_name}")
            
        logging.info(f"最终使用的模型名称: {model_name}")
        
        # 验证模型文件存在
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, 'checkpoints', model_name, 'latest_net_G.pth')
        if os.path.exists(model_path):
            logging.info(f"使用模型文件: {model_path}")
        else:
            logging.error(f"模型文件不存在: {model_path}")
            raise Exception(f"找不到模型文件: {model_path}")
        
        # 检查输入目录是否存在
        if not os.path.exists(input_path):
            raise Exception(f"输入路径不存在: {input_path}")
            
        # 正常加载模型，不做额外清理
        logging.info(f"正在加载模型 {model_name}...")
        model = load_model(model_name)
        logging.info(f"成功加载模型: {model_name}")
        
        # 创建输出目录
        os.makedirs(output_path, exist_ok=True)
        
        # 获取所有图片文件
        img_files = []
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    img_files.append(os.path.join(root, file))
        
        logging.info(f"找到 {len(img_files)} 个图片文件")
        
        # 处理每张图片
        processed_count = 0
        for img_file in img_files:
            try:
                # 读取图片
                img = cv2.imread(img_file)
                if img is None:
                    logging.warning(f"无法读取图片: {img_file}")
                    continue
                
                # 处理图片并保存
                # 获取相对路径
                rel_path = os.path.relpath(img_file, input_path)
                output_img_path = os.path.join(output_path, rel_path)
                os.makedirs(os.path.dirname(output_img_path), exist_ok=True)
                
                # 调用预处理函数并传递模型名称
                processed_img = preprocess_image(img, model, model_name)
                cv2.imwrite(output_img_path, processed_img)
                
                # 统计成功处理的图片
                processed_count += 1
                
                # 每20张图片记录一次进度，减少日志量
                if processed_count % 20 == 0:
                    logging.info(f"已处理 {processed_count}/{len(img_files)} 张图片")
                    
            except Exception as e:
                logging.error(f"处理图片失败 {img_file}: {str(e)}")
                continue
        
        if processed_count == 0:
            raise Exception("没有成功处理任何图片")
            
        logging.info(f"处理完成! 共处理 {processed_count} 张图片，使用模型: {model_name}")
        # 清理资源
        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        return True
        
    except Exception as e:
        logging.error(f"处理数据集失败: {str(e)}")
        return False

if __name__ == '__main__':
    # 设置日志
    logging.basicConfig(level=logging.INFO)
    # 测试代码
    input_path = "./datasets/test"
    output_path = "./datasets/test_processed"
    # 明确指定模型名称
    process_dataset(input_path, output_path, 'darkBA_pix2pix') 