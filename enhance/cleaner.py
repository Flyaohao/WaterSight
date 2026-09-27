#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import logging
from datetime import datetime
import shutil
from pathlib import Path
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='cleaner.log'
)
logger = logging.getLogger(__name__)

# 添加控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

class StaticCleaner:
    """静态文件清理工具，用于保持static目录的整洁"""
    
    def __init__(self, base_dir=None, max_files_per_type=1):
        """
        初始化清理工具
        
        参数:
            base_dir: 项目根目录，默认为当前文件所在目录
            max_files_per_type: 每种类型文件保留的最大数量，默认为1（只保留最新的文件）
        """
        if base_dir is None:
            self.base_dir = Path(__file__).resolve().parent
        else:
            self.base_dir = Path(base_dir)
        
        self.static_dir = self.base_dir / "static"
        self.max_files_per_type = max_files_per_type
        
        self.directories = {
            "images": {
                "original": self.static_dir / "images" / "original",
                "enhanced": self.static_dir / "images" / "enhanced"
            },
            "videos": {
                "original": self.static_dir / "videos" / "original",
                "enhanced": self.static_dir / "videos" / "enhanced"
            }
        }
        
        # 确保所有目录存在
        for category in self.directories.values():
            for dir_path in category.values():
                dir_path.mkdir(parents=True, exist_ok=True)
    
    def clean_directory(self, directory, file_pattern="*.*", keep_latest=True):
        """
        清理指定目录下的文件，只保留最近的几个
        
        参数:
            directory: 要清理的目录路径
            file_pattern: 文件模式匹配
            keep_latest: 是否保留最新的文件
        
        返回:
            删除的文件数
        """
        if not directory.exists():
            logger.warning(f"目录不存在: {directory}")
            return 0
        
        # 获取目录中所有匹配的文件
        files = list(directory.glob(file_pattern))
        
        # 如果文件数量少于或等于保留数量，则不需要清理
        if len(files) <= self.max_files_per_type:
            logger.info(f"目录 {directory} 中的文件数量({len(files)})未超过保留数量({self.max_files_per_type})，不需要清理")
            return 0
        
        # 按修改时间排序
        files.sort(key=lambda x: x.stat().st_mtime, reverse=keep_latest)
        
        # 保留最近的几个文件，删除其余的
        files_to_delete = files[self.max_files_per_type:]
        deleted_count = 0
        
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                logger.info(f"已删除文件: {file_path}")
                deleted_count += 1
            except Exception as e:
                logger.error(f"删除文件 {file_path} 失败: {str(e)}")
        
        return deleted_count
    
    def clean_all(self):
        """清理所有静态目录"""
        total_deleted = 0
        
        logger.info("="*50)
        logger.info("开始清理静态文件目录")
        
        # 清理图片和视频目录
        for category_name, category_dirs in self.directories.items():
            for dir_type, dir_path in category_dirs.items():
                if category_name == "images":
                    deleted = self.clean_directory(dir_path, "*.jpg")
                    deleted += self.clean_directory(dir_path, "*.jpeg")
                    deleted += self.clean_directory(dir_path, "*.png")
                elif category_name == "videos":
                    deleted = self.clean_directory(dir_path, "*.mp4")
                
                logger.info(f"已从 {category_name}/{dir_type} 目录删除 {deleted} 个文件")
                total_deleted += deleted
        
        logger.info(f"清理完成，共删除 {total_deleted} 个文件")
        logger.info("="*50)
        return total_deleted
    
    def clean_on_upload(self, media_type, original_filename):
        """
        当有新文件上传时进行清理
        
        参数:
            media_type: 媒体类型 ("image" 或 "video")
            original_filename: 上传的原始文件名
        
        返回:
            删除的文件数
        """
        logger.info(f"收到新的上传: {media_type} - {original_filename}，开始清理")
        
        # 根据媒体类型确定要清理的目录
        if media_type == "image":
            category_name = "images"
        elif media_type == "video":
            category_name = "videos"
        else:
            logger.warning(f"未知的媒体类型: {media_type}，跳过清理")
            return 0
        
        # 获取相应的目录
        category_dirs = self.directories.get(category_name, {})
        total_deleted = 0
        
        for dir_type, dir_path in category_dirs.items():
            if category_name == "images":
                deleted = self.clean_directory(dir_path, "*.jpg")
                deleted += self.clean_directory(dir_path, "*.jpeg")
                deleted += self.clean_directory(dir_path, "*.png")
            elif category_name == "videos":
                deleted = self.clean_directory(dir_path, "*.mp4")
            
            logger.info(f"已从 {category_name}/{dir_type} 目录删除 {deleted} 个文件")
            total_deleted += deleted
        
        return total_deleted

# 如果直接运行此脚本，则清理所有目录
if __name__ == "__main__":
    cleaner = StaticCleaner()
    cleaner.clean_all() 