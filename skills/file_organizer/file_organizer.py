"""
File Organizer Skill
自动整理文件到指定文件夹
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class FileOrganizer:
    """文件整理器"""

    # 文件类型映射
    FILE_TYPES = {
        '图片': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico'],
        '文档': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
        '视频': ['.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm'],
        '音频': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
        '压缩包': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
        '代码': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.go', '.rs', '.ts', '.json', '.yaml', '.yml', '.xml'],
        '可执行': ['.exe', '.msi', '.dmg', '.app', '.deb', '.rpm'],
        '其他': []
    }

    def __init__(self):
        """初始化文件整理器"""
        self.moved_files: List[Tuple[str, str]] = []
        self.skipped_files: List[str] = []

    def get_file_type(self, filepath: str) -> str:
        """获取文件类型"""
        ext = Path(filepath).suffix.lower()

        for type_name, extensions in self.FILE_TYPES.items():
            if ext in extensions:
                return type_name
        return '其他'

    def organize_by_type(self, source_dir: str, target_dir: Optional[str] = None,
                       dry_run: bool = False) -> Dict[str, List[str]]:
        """按文件类型整理

        Args:
            source_dir: 源目录
            target_dir: 目标目录（默认同源目录）
            dry_run: 仅预览，不实际移动

        Returns:
            整理结果统计
        """
        source_dir = os.path.abspath(source_dir)
        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"目录不存在: {source_dir}")

        if target_dir is None:
            target_dir = source_dir
        else:
            target_dir = os.path.abspath(target_dir)

        self.moved_files = []
        self.skipped_files = []
        stats = {type_name: [] for type_name in self.FILE_TYPES.keys()}

        for filename in os.listdir(source_dir):
            filepath = os.path.join(source_dir, filename)

            if os.path.isdir(filepath):
                continue

            file_type = self.get_file_type(filepath)
            type_dir = os.path.join(target_dir, file_type)

            if filepath == os.path.join(type_dir, filename):
                continue

            if not dry_run:
                os.makedirs(type_dir, exist_ok=True)
                dest_path = os.path.join(type_dir, filename)

                if os.path.exists(dest_path):
                    # 重名处理
                    base, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(os.path.join(type_dir, f"{base}_{counter}{ext}")):
                        counter += 1
                    dest_path = os.path.join(type_dir, f"{base}_{counter}{ext}")

                shutil.move(filepath, dest_path)
                self.moved_files.append((filepath, dest_path))
            else:
                dest_path = os.path.join(type_dir, filename)
                self.moved_files.append((filepath, dest_path))

            stats[file_type].append(filename)

        return stats

    def organize_by_date(self, source_dir: str, target_dir: Optional[str] = None,
                        date_format: str = "%Y-%m", dry_run: bool = False) -> Dict[str, List[str]]:
        """按日期整理

        Args:
            source_dir: 源目录
            target_dir: 目标目录
            date_format: 日期格式（默认 %Y-%m）
            dry_run: 仅预览

        Returns:
            整理结果统计
        """
        source_dir = os.path.abspath(source_dir)
        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"目录不存在: {source_dir}")

        if target_dir is None:
            target_dir = source_dir
        else:
            target_dir = os.path.abspath(target_dir)

        self.moved_files = []
        self.skipped_files = []
        stats: Dict[str, List[str]] = {}

        for filename in os.listdir(source_dir):
            filepath = os.path.join(source_dir, filename)

            if os.path.isdir(filepath):
                continue

            # 获取文件修改时间
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            date_folder = mtime.strftime(date_format)

            date_dir = os.path.join(target_dir, date_folder)

            if not dry_run:
                os.makedirs(date_dir, exist_ok=True)
                dest_path = os.path.join(date_dir, filename)

                if os.path.exists(dest_path):
                    base, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(os.path.join(date_dir, f"{base}_{counter}{ext}")):
                        counter += 1
                    dest_path = os.path.join(date_dir, f"{base}_{counter}{ext}")

                shutil.move(filepath, dest_path)
                self.moved_files.append((filepath, dest_path))
            else:
                dest_path = os.path.join(date_dir, filename)
                self.moved_files.append((filepath, dest_path))

            if date_folder not in stats:
                stats[date_folder] = []
            stats[date_folder].append(filename)

        return stats

    def organize_by_extension(self, source_dir: str, target_dir: Optional[str] = None,
                            dry_run: bool = False) -> Dict[str, List[str]]:
        """按扩展名整理"""
        source_dir = os.path.abspath(source_dir)
        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"目录不存在: {source_dir}")

        if target_dir is None:
            target_dir = source_dir
        else:
            target_dir = os.path.abspath(target_dir)

        self.moved_files = []
        self.skipped_files = []
        stats: Dict[str, List[str]] = {}

        for filename in os.listdir(source_dir):
            filepath = os.path.join(source_dir, filename)

            if os.path.isdir(filepath):
                continue

            ext = Path(filepath).suffix.lower()
            if not ext:
                ext = '无扩展名'
            else:
                ext = ext[1:]  # 去掉点

            ext_dir = os.path.join(target_dir, ext)

            if not dry_run:
                os.makedirs(ext_dir, exist_ok=True)
                dest_path = os.path.join(ext_dir, filename)

                if os.path.exists(dest_path):
                    base, ext_orig = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(os.path.join(ext_dir, f"{base}_{counter}{ext_orig}")):
                        counter += 1
                    dest_path = os.path.join(ext_dir, f"{base}_{counter}{ext_orig}")

                shutil.move(filepath, dest_path)
                self.moved_files.append((filepath, dest_path))
            else:
                dest_path = os.path.join(ext_dir, filename)
                self.moved_files.append((filepath, dest_path))

            if ext not in stats:
                stats[ext] = []
            stats[ext].append(filename)

        return stats

    def get_summary(self) -> Dict[str, int]:
        """获取操作摘要"""
        return {
            'moved': len(self.moved_files),
            'skipped': len(self.skipped_files)
        }


__all__ = ["FileOrganizer"]
