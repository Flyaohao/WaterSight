#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import logging
import shutil
from datetime import datetime
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class StaticCleaner:
    """静态文件清理工具，用于保持static目录的整洁"""
    
    def __init__(self, base_dir=None, max_files=1):
        """
        初始化清理工具
        
        参数:
            base_dir: 项目根目录，默认为当前文件所在目录
            max_files: 每个目录中保留的最大文件数量，默认为1（只保留最新的文件）
        """
        if base_dir is None:
            self.base_dir = Path(__file__).resolve().parent
        else:
            self.base_dir = Path(base_dir)
        
        self.max_files = max_files
        
        # 定义需要清理的目录
        self.static_dir = self.base_dir / "static"
        self.static1_dir = self.base_dir / "static1"
        self.uploads_dir = self.base_dir / "uploads"  # 新增uploads目录
        
        self.directories = {
            "static": {
                "datasets": self.static_dir / "datasets",
                "processed": self.static_dir / "processed"
            },
            "static1": {
                "datasets": self.static1_dir / "datasets",
                "processed": self.static1_dir / "processed"
            },
            "uploads": {
                "root": self.uploads_dir  # 新增uploads目录
            }
        }
        
        # 确保所有目录存在
        for category in self.directories.values():
            for dir_path in category.values():
                os.makedirs(dir_path, exist_ok=True)
    
    def clean_directory(self, directory, keep_latest=True):
        """
        清理指定目录下的文件，只保留最近的几个
        
        参数:
            directory: 要清理的目录路径
            keep_latest: 是否保留最新的文件
        
        返回:
            删除的文件和目录数
        """
        directory = Path(directory)
        if not directory.exists():
            logger.warning(f"目录不存在: {directory}")
            return 0
        
        # 获取目录中所有内容
        items = [item for item in directory.glob("*")]
        
        # 如果文件数量少于或等于保留数量，则不需要清理
        if len(items) <= self.max_files:
            logger.info(f"目录 {directory} 中的内容数量({len(items)})未超过保留数量({self.max_files})，不需要清理")
            return 0
        
        # 按修改时间排序
        items.sort(key=lambda x: x.stat().st_mtime, reverse=keep_latest)
        
        # 保留最近的几个文件，删除其余的
        items_to_delete = items[self.max_files:]
        deleted_count = 0
        
        for item_path in items_to_delete:
            try:
                if item_path.is_dir():
                    shutil.rmtree(item_path)
                    logger.info(f"已删除目录: {item_path}")
                else:
                    os.remove(item_path)
                    logger.info(f"已删除文件: {item_path}")
                deleted_count += 1
            except Exception as e:
                logger.error(f"删除 {item_path} 失败: {str(e)}")
        
        return deleted_count
    
    def clean_all(self):
        """清理所有静态目录，包括uploads目录"""
        total_deleted = 0
        
        logger.info("="*50)
        logger.info("开始清理静态文件目录")
        
        # 清理static和static1目录
        for category_name, category_dirs in self.directories.items():
            for dir_type, dir_path in category_dirs.items():
                deleted = self.clean_directory(dir_path)
                logger.info(f"已从 {category_name}/{dir_type} 目录删除 {deleted} 个文件或目录")
                total_deleted += deleted
        
        logger.info(f"清理完成，共删除 {total_deleted} 个文件或目录")
        logger.info("="*50)
        return total_deleted

    def clean_uploads_only(self):
        """只清理uploads目录，保留其他目录内容"""
        total_deleted = 0
        
        logger.info("="*50)
        logger.info("开始清理uploads目录")
        
        # 只清理uploads目录
        if "uploads" in self.directories:
            for dir_type, dir_path in self.directories["uploads"].items():
                deleted = self.clean_directory(dir_path)
                logger.info(f"已从 uploads/{dir_type} 目录删除 {deleted} 个文件或目录")
                total_deleted += deleted
        
        logger.info(f"清理完成，共删除 {total_deleted} 个文件或目录")
        logger.info("="*50)
        return total_deleted

    def clean_static_directories(self, timestamp=None):
        """
        清理static和static1目录，但跳过指定的时间戳相关文件
        
        参数:
            timestamp: 要保留的时间戳（字符串），如果提供，包含该时间戳的文件将被保留
        
        返回:
            删除的文件和目录数
        """
        total_deleted = 0
        
        logger.info("="*50)
        logger.info("开始清理static和static1目录")
        
        # 只清理static和static1目录
        for category_name, category_dirs in self.directories.items():
            if category_name in ["static", "static1"]:
                for dir_type, dir_path in category_dirs.items():
                    items = [item for item in Path(dir_path).glob("*")]
                    items.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                    
                    # 如果文件数量少于或等于保留数量，则不需要清理
                    if len(items) <= self.max_files:
                        logger.info(f"目录 {dir_path} 中的内容数量({len(items)})未超过保留数量({self.max_files})，不需要清理")
                        continue
                    
                    # 保留最新的文件和包含指定时间戳的文件
                    to_keep = set(items[:self.max_files])  # 最新的文件
                    
                    # 如果提供了时间戳，保留包含该时间戳的文件
                    if timestamp:
                        timestamp_str = str(timestamp)
                        for item in items:
                            if timestamp_str in str(item):
                                to_keep.add(item)
                                logger.info(f"保留含时间戳的文件: {item}")
                    
                    # 删除不在保留列表中的文件
                    for item_path in items:
                        if item_path not in to_keep:
                            try:
                                if item_path.is_dir():
                                    shutil.rmtree(item_path)
                                    logger.info(f"已删除目录: {item_path}")
                                else:
                                    os.remove(item_path)
                                    logger.info(f"已删除文件: {item_path}")
                                total_deleted += 1
                            except Exception as e:
                                logger.error(f"删除 {item_path} 失败: {str(e)}")
        
        logger.info(f"清理完成，共删除 {total_deleted} 个文件或目录")
        logger.info("="*50)
        return total_deleted
    
# 直接运行此脚本时，清理所有目录
if __name__ == "__main__":
    cleaner = StaticCleaner()
    deleted_count = cleaner.clean_all()
    print(f"清理完成，共删除 {deleted_count} 个文件或目录") 