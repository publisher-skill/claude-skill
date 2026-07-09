"""
Batch Renamer Skill
批量重命名文件
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Optional, Callable, Dict, Any


class BatchRenamer:
    """批量重命名器"""

    def __init__(self):
        """初始化"""
        self.rename_history: List[Tuple[str, str]] = []
        self.skipped_files: List[str] = []

    def rename_with_pattern(self, directory: str, pattern: str,
                           replacement: str, dry_run: bool = False) -> List[Tuple[str, str]]:
        """使用正则表达式重命名

        Args:
            directory: 目录路径
            pattern: 正则表达式模式
            replacement: 替换字符串
            dry_run: 仅预览

        Returns:
            重命名列表
        """
        directory = os.path.abspath(directory)
        if not os.path.exists(directory):
            raise FileNotFoundError(f"目录不存在: {directory}")

        self.rename_history = []
        self.skipped_files = []

        try:
            regex = re.compile(pattern)
        except re.error as e:
            raise ValueError(f"正则表达式错误: {e}")

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            if os.path.isdir(filepath):
                continue

            new_name = regex.sub(replacement, filename)

            if new_name != filename:
                self._do_rename(directory, filename, new_name, dry_run)
            else:
                self.skipped_files.append(filename)

        return self.rename_history

    def rename_with_sequence(self, directory: str, prefix: str = "file",
                           start: int = 1, padding: int = 3,
                           dry_run: bool = False) -> List[Tuple[str, str]]:
        """使用序号重命名

        Args:
            directory: 目录路径
            prefix: 文件名前缀
            start: 起始序号
            padding: 序号填充位数
            dry_run: 仅预览

        Returns:
            重命名列表
        """
        directory = os.path.abspath(directory)
        if not os.path.exists(directory):
            raise FileNotFoundError(f"目录不存在: {directory}")

        self.rename_history = []
        self.skipped_files = []

        files = []
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                files.append(filename)

        # 按名称排序
        files.sort()

        for i, filename in enumerate(files, start):
            ext = Path(filename).suffix
            new_name = f"{prefix}{str(i).zfill(padding)}{ext}"
            self._do_rename(directory, filename, new_name, dry_run)

        return self.rename_history

    def add_prefix(self, directory: str, prefix: str,
                   dry_run: bool = False) -> List[Tuple[str, str]]:
        """添加前缀

        Args:
            directory: 目录路径
            prefix: 前缀字符串
            dry_run: 仅预览

        Returns:
            重命名列表
        """
        directory = os.path.abspath(directory)
        if not os.path.exists(directory):
            raise FileNotFoundError(f"目录不存在: {directory}")

        self.rename_history = []
        self.skipped_files = []

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            if os.path.isdir(filepath):
                continue

            if filename.startswith(prefix):
                self.skipped_files.append(filename)
                continue

            new_name = f"{prefix}{filename}"
            self._do_rename(directory, filename, new_name, dry_run)

        return self.rename_history

    def add_suffix(self, directory: str, suffix: str,
                   before_ext: bool = True, dry_run: bool = False) -> List[Tuple[str, str]]:
        """添加后缀

        Args:
            directory: 目录路径
            suffix: 后缀字符串
            before_ext: 是否在扩展名前添加
            dry_run: 仅预览

        Returns:
            重命名列表
        """
        directory = os.path.abspath(directory)
        if not os.path.exists(directory):
            raise FileNotFoundError(f"目录不存在: {directory}")

        self.rename_history = []
        self.skipped_files = []

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            if os.path.isdir(filepath):
                continue

            if before_ext:
                base, ext = os.path.splitext(filename)
                new_name = f"{base}{suffix}{ext}"
            else:
                new_name = f"{filename}{suffix}"

            self._do_rename(directory, filename, new_name, dry_run)

        return self.rename_history

    def replace_text(self, directory: str, old_text: str, new_text: str,
                     case_sensitive: bool = True, dry_run: bool = False) -> List[Tuple[str, str]]:
        """替换文本

        Args:
            directory: 目录路径
            old_text: 要替换的文本
            new_text: 新文本
            case_sensitive: 是否区分大小写
            dry_run: 仅预览

        Returns:
            重命名列表
        """
        directory = os.path.abspath(directory)
        if not os.path.exists(directory):
            raise FileNotFoundError(f"目录不存在: {directory}")

        self.rename_history = []
        self.skipped_files = []

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            if os.path.isdir(filepath):
                continue

            if case_sensitive:
                if old_text in filename:
                    new_name = filename.replace(old_text, new_text)
                    self._do_rename(directory, filename, new_name, dry_run)
                else:
                    self.skipped_files.append(filename)
            else:
                if old_text.lower() in filename.lower():
                    # 使用正则进行不区分大小写替换
                    new_name = re.sub(re.escape(old_text), new_text, filename, flags=re.IGNORECASE)
                    self._do_rename(directory, filename, new_name, dry_run)
                else:
                    self.skipped_files.append(filename)

        return self.rename_history

    def change_case(self, directory: str, case_type: str = "lower",
                   dry_run: bool = False) -> List[Tuple[str, str]]:
        """改变大小写

        Args:
            directory: 目录路径
            case_type: lower/upper/title
            dry_run: 仅预览

        Returns:
            重命名列表
        """
        directory = os.path.abspath(directory)
        if not os.path.exists(directory):
            raise FileNotFoundError(f"目录不存在: {directory}")

        valid_types = ['lower', 'upper', 'title']
        if case_type not in valid_types:
            raise ValueError(f"case_type 必须是 {valid_types} 之一")

        self.rename_history = []
        self.skipped_files = []

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            if os.path.isdir(filepath):
                continue

            base, ext = os.path.splitext(filename)

            if case_type == 'lower':
                new_base = base.lower()
            elif case_type == 'upper':
                new_base = base.upper()
            else:  # title
                new_base = base.title()

            new_name = f"{new_base}{ext}"

            if new_name != filename:
                self._do_rename(directory, filename, new_name, dry_run)
            else:
                self.skipped_files.append(filename)

        return self.rename_history

    def _do_rename(self, directory: str, old_name: str, new_name: str, dry_run: bool):
        """执行重命名"""
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)

        if os.path.exists(new_path) and new_path != old_path:
            # 处理重名
            base, ext = os.path.splitext(new_name)
            counter = 1
            while os.path.exists(os.path.join(directory, f"{base}_{counter}{ext}")):
                counter += 1
            new_name = f"{base}_{counter}{ext}"
            new_path = os.path.join(directory, new_name)

        if not dry_run:
            os.rename(old_path, new_path)

        self.rename_history.append((old_name, new_name))

    def get_summary(self) -> Dict[str, int]:
        """获取操作摘要"""
        return {
            'renamed': len(self.rename_history),
            'skipped': len(self.skipped_files)
        }


__all__ = ["BatchRenamer"]
