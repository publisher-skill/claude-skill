"""
Directory Tree Skill
生成目录树结构
"""

import os
from pathlib import Path
from typing import List, Optional, Set, Callable


class DirectoryTree:
    """目录树生成器"""

    def __init__(self):
        """初始化"""
        self.indent = '  '
        self.branch = '├── '
        self.last_branch = '└── '

    def generate(self, directory: str, max_depth: Optional[int] = None,
                exclude_patterns: Optional[List[str]] = None,
                include_files: bool = True) -> str:
        """生成目录树字符串

        Args:
            directory: 目录路径
            max_depth: 最大深度
            exclude_patterns: 排除的模式列表
            include_files: 是否包含文件

        Returns:
            目录树字符串
        """
        directory = os.path.abspath(directory)
        if not os.path.exists(directory):
            raise FileNotFoundError(f"目录不存在: {directory}")

        if exclude_patterns is None:
            exclude_patterns = ['.git', '__pycache__', '.pyc', '.pyo', '.pyd']

        lines = [os.path.basename(directory) + '/']
        self._generate_recursive(directory, lines, 1, max_depth, set(exclude_patterns), include_files)
        return '\n'.join(lines)

    def _generate_recursive(self, directory: str, lines: List[str], depth: int,
                          max_depth: Optional[int], exclude_patterns: Set[str],
                          include_files: bool):
        """递归生成"""
        if max_depth is not None and depth > max_depth:
            return

        try:
            items = os.listdir(directory)
        except PermissionError:
            lines.append(self.indent * depth + '[权限不足]')
            return

        # 分离目录和文件
        dirs = []
        files = []

        for item in items:
            if any(pattern in item for pattern in exclude_patterns):
                continue
            if item.startswith('.'):
                continue

            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                dirs.append(item)
            else:
                files.append(item)

        # 排序
        dirs.sort()
        files.sort()

        # 处理目录
        all_items = dirs + (files if include_files else [])

        for i, item in enumerate(all_items):
            item_path = os.path.join(directory, item)
            is_last = i == len(all_items) - 1

            prefix = self.last_branch if is_last else self.branch

            if os.path.isdir(item_path):
                lines.append(self.indent * depth + prefix + item + '/')
                self._generate_recursive(item_path, lines, depth + 1, max_depth, exclude_patterns, include_files)
            else:
                lines.append(self.indent * depth + prefix + item)

    def generate_with_sizes(self, directory: str, max_depth: Optional[int] = None,
                           exclude_patterns: Optional[List[str]] = None) -> str:
        """生成带文件大小的目录树

        Args:
            directory: 目录路径
            max_depth: 最大深度
            exclude_patterns: 排除的模式列表

        Returns:
            目录树字符串
        """
        directory = os.path.abspath(directory)
        if not os.path.exists(directory):
            raise FileNotFoundError(f"目录不存在: {directory}")

        if exclude_patterns is None:
            exclude_patterns = ['.git', '__pycache__']

        lines = [os.path.basename(directory) + '/']
        self._generate_with_sizes_recursive(directory, lines, 1, max_depth, set(exclude_patterns))
        return '\n'.join(lines)

    def _generate_with_sizes_recursive(self, directory: str, lines: List[str], depth: int,
                                      max_depth: Optional[int], exclude_patterns: Set[str]):
        """递归生成带大小的树"""
        if max_depth is not None and depth > max_depth:
            return

        try:
            items = os.listdir(directory)
        except PermissionError:
            lines.append(self.indent * depth + '[权限不足]')
            return

        dirs = []
        files = []

        for item in items:
            if any(pattern in item for pattern in exclude_patterns):
                continue
            if item.startswith('.'):
                continue

            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                dirs.append(item)
            else:
                files.append((item, os.path.getsize(item_path)))

        dirs.sort()
        files.sort(key=lambda x: x[0])

        all_items = dirs + [f[0] for f in files]
        file_sizes = {f[0]: f[1] for f in files}

        for i, item in enumerate(all_items):
            item_path = os.path.join(directory, item)
            is_last = i == len(all_items) - 1

            prefix = self.last_branch if is_last else self.branch

            if os.path.isdir(item_path):
                dir_size = self._get_dir_size(item_path, exclude_patterns)
                lines.append(f"{self.indent * depth}{prefix}{item}/ ({self._format_size(dir_size)})")
                self._generate_with_sizes_recursive(item_path, lines, depth + 1, max_depth, exclude_patterns)
            else:
                size = file_sizes.get(item, 0)
                lines.append(f"{self.indent * depth}{prefix}{item} ({self._format_size(size)})")

    def _get_dir_size(self, directory: str, exclude_patterns: Set[str]) -> int:
        """获取目录大小"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            # 过滤排除的目录
            dirnames[:] = [d for d in dirnames if d not in exclude_patterns and not d.startswith('.')]

            for filename in filenames:
                if any(pattern in filename for pattern in exclude_patterns):
                    continue
                if filename.startswith('.'):
                    continue

                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
        return total_size

    def _format_size(self, size: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"

    def save_to_file(self, tree_str: str, output_file: str):
        """保存到文件

        Args:
            tree_str: 目录树字符串
            output_file: 输出文件路径
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(tree_str)

    def generate_markdown(self, directory: str, max_depth: Optional[int] = None,
                        exclude_patterns: Optional[List[str]] = None,
                        include_files: bool = True) -> str:
        """生成 Markdown 格式的目录树

        Args:
            directory: 目录路径
            max_depth: 最大深度
            exclude_patterns: 排除的模式列表
            include_files: 是否包含文件

        Returns:
            Markdown 字符串
        """
        tree_str = self.generate(directory, max_depth, exclude_patterns, include_files)
        lines = ['```', tree_str, '```']
        return '\n'.join(lines)


__all__ = ["DirectoryTree"]
