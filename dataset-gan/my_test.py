import os
import torch
from options.test_options import TestOptions
from data import create_dataset
from models import create_model
from util.visualizer import save_images
from util import html
import sys
import logging
from datetime import datetime

# 配置日志
def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # 只创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    
    # 创建格式器
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()

def process_images(dataroot, name='darkBA_pix2pix', model_type='pix2pix', direction='BtoA', results_dir='./static1/processed'):
    """
    处理图像的主函数，参考 test.py 的实现
    """
    try:
        # 检查数据集目录结构
        test_dir = os.path.join(dataroot, 'test')
        if not os.path.exists(test_dir):
            logger.error(f"Directory 'test' not found in {dataroot}")
            return False
            
        # 检查是否有图片文件
        test_images = [f for f in os.listdir(test_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                   
        if not test_images:
            logger.error(f"No images found in directory 'test'")
            return False
            
        logger.info(f"Found {len(test_images)} images in test/")

        # 检查CUDA是否可用
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f'Using device: {device}')

        # 保存原始命令行参数
        original_argv = sys.argv

        # 参考 test.py 设置命令行参数
        sys.argv = [
            'test.py',
            '--dataroot', str(dataroot),
            '--name', str(name),
            '--model', str(model_type),
            '--direction', str(direction),
            '--results_dir', str(results_dir),
            '--dataset_mode', 'aligned',  # 使用 aligned 模式，与 test.py 一致
            '--norm', 'batch',
            '--netG', 'unet_256',
            '--input_nc', '3',
            '--output_nc', '3',
            '--preprocess', 'resize_and_crop',  # 使用默认的预处理
            '--load_size', '256',
            '--crop_size', '256',
            '--no_flip',
            '--phase', 'test',
            '--eval',
            '--num_test', str(len(test_images)),  # 使用实际的图片数量
            '--gpu_ids', '-1'
        ]

        try:
            # 设置测试选项
            opt = TestOptions().parse()
            
            # 创建数据集和模型
            dataset = create_dataset(opt)
            model = create_model(opt)
            model.setup(opt)
            
            # 创建结果目录
            web_dir = os.path.join(opt.results_dir, opt.name, f'{opt.phase}_latest')
            os.makedirs(web_dir, exist_ok=True)
            logger.info(f'创建结果目录: {web_dir}')
            
            # 创建网页用于保存结果
            webpage = html.HTML(web_dir, f'Experiment = {opt.name}, Phase = {opt.phase}')
            
            # 设置评估模式
            model.eval()
            
            # 处理图像
            for i, data in enumerate(dataset):
                model.set_input(data)
                model.test()
                visuals = model.get_current_visuals()
                img_path = model.get_image_paths()
                if i % 5 == 0:
                    logger.info(f'处理第 {i} 张图像... {img_path}')
                save_images(webpage, visuals, img_path, aspect_ratio=opt.aspect_ratio, width=opt.display_winsize)
            
            webpage.save()
            logger.info('处理完成')
            return True
            
        finally:
            sys.argv = original_argv
            
    except Exception as e:
        logger.error(f'处理图像时发生错误: {str(e)}', exc_info=True)
        return False

if __name__ == '__main__':
    # 测试代码
    dataroot = './datasets/test'
    process_images(dataroot)
