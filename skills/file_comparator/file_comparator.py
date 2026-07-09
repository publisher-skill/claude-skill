"""
File Comparator Skill
文件和文件夹对比工具
"""

import os
import filecmp
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
from datetime import datetime


class FileComparator:
    """文件对比器"""

    def __init__(self):
        """初始化"""
        pass

    def compare_files(self, file1: str, file2: str,
                    method: str = 'quick') -> Dict[str, any]:
        """对比两个文件

        Args:
            file1: 文件1路径
            file2: 文件2路径
            method: 对比方法（quick/content/hash）

        Returns:
            对比结果
        """
        for f in [file1, file2]:
            if not os.path.exists(f):
                raise FileNotFoundError(f"文件不存在: {f}")
            if not os.path.isfile(f):
                raise ValueError(f"不是文件: {f}")

        result = {
            'file1': file1,
            'file2': file2,
            'identical': False,
            'method': method,
        }

        stat1 = os.stat(file1)
        stat2 = os.stat(file2)

        result['size_match'] = stat1.st_size == stat2.st_size

        if method == 'quick':
            # 快速对比：大小+修改时间
            result['mtime_match'] = stat1.st_mtime == stat2.st_mtime
            result['identical'] = result['size_match'] and result['mtime_match']

        elif method == 'content':
            # 内容对比
            result['identical'] = filecmp.cmp(file1, file2, shallow=False)

        elif method == 'hash':
            # Hash 对比
            hash1 = self._compute_file_hash(file1)
            hash2 = self._compute_file_hash(file2)
            result['hash1'] = hash1
            result['hash2'] = hash2
            result['identical'] = hash1 == hash2

        else:
            raise ValueError(f"未知的对比方法: {method}")

        result['size1'] = stat1.st_size
        result['size2'] = stat2.st_size
        result['mtime1'] = datetime.fromtimestamp(stat1.st_mtime).isoformat()
        result['mtime2'] = datetime.fromtimestamp(stat2.st_mtime).isoformat()

        return result

    def compare_directories(self, dir1: str, dir2: str,
                           shallow: bool = True,
                           recursive: bool = True) -> Dict[str, any]:
        """对比两个目录

        Args:
            dir1: 目录1路径
            dir2: 目录2路径
            shallow: 是否浅层对比
            recursive: 是否递归

        Returns:
            对比结果
        """
        for d in [dir1, dir2]:
            if not os.path.exists(d):
                raise FileNotFoundError(f"目录不存在: {d}")
            if not os.path.isdir(d):
                raise ValueError(f"不是目录: {d}")

        result = {
            'dir1': dir1,
            'dir2': dir2,
            'common': [],
            'only_in_dir1': [],
            'only_in_dir2': [],
            'differing': [],
            'funny': [],
        }

        dc = filecmp.dircmp(dir1, dir2, ignore=None)
        self._process_dircmp(dc, result, recursive)

        return result

    def _process_dircmp(self, dc: filecmp.dircmp, result: Dict[str, any],
                       recursive: bool = True, prefix: str = ''):
        """处理 dircmp 结果"""
        for name in dc.common_files:
            result['common'].append(os.path.join(prefix, name))

        for name in dc.left_only:
            result['only_in_dir1'].append(os.path.join(prefix, name))

        for name in dc.right_only:
            result['only_in_dir2'].append(os.path.join(prefix, name))

        for name in dc.diff_files:
            result['differing'].append(os.path.join(prefix, name))

        for name in dc.funny_files:
            result['funny'].append(os.path.join(prefix, name))

        if recursive:
            for subdir, sub_dc in dc.subdirs.items():
                self._process_dircmp(sub_dc, result, recursive, os.path.join(prefix, subdir))

    def find_duplicates(self, directory: str,
                       by_hash: bool = True,
                       recursive: bool = True) -> Dict[str, List[str]]:
        """查找重复文件

        Args:
            directory: 目录路径
            by_hash: 是否用 hash 查找（否则用大小）
            recursive: 是否递归

        Returns:
            重复文件分组
        """
        directory = os.path.abspath(directory)
        if not os.path.exists(directory):
            raise FileNotFoundError(f"目录不存在: {directory}")

        file_groups: Dict[str, List[str]] = {}

        for root, _, files in os.walk(directory):
            if not recursive and root != directory:
                continue

            for filename in files:
                filepath = os.path.join(root, filename)

                if by_hash:
                    key = self._compute_file_hash(filepath)
                else:
                    key = str(os.path.getsize(filepath))

                if key not in file_groups:
                    file_groups[key] = []
                file_groups[key].append(filepath)

        # 过滤掉只有一个文件的分组
        duplicates = {k: v for k, v in file_groups.items() if len(v) > 1}

        return duplicates

    def _compute_file_hash(self, filepath: str,
                         algorithm: str = 'md5') -> str:
        """计算文件 hash"""
        hash_obj = hashlib.new(algorithm)

        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                hash_obj.update(chunk)

        return hash_obj.hexdigest()

    def generate_diff_report(self, comparison: Dict[str, any],
                           output_file: Optional[str] = None) -> str:
        """生成对比报告

        Args:
            comparison: 对比结果
            output_file: 输出文件（可选）

        Returns:
            报告字符串
        """
        lines = []
        lines.append("="*60)
        lines.append("文件/目录对比报告")
        lines.append("="*60)

        if 'dir1' in comparison:
            # 目录对比
            lines.append(f"\n目录1: {comparison['dir1']}")
            lines.append(f"目录2: {comparison['dir2']}")
            lines.append("")

            if comparison['common']:
                lines.append(f"共同文件 ({len(comparison['common'])}):")
                for f in comparison['common'][:10]:
                    lines.append(f"  {f}")
                if len(comparison['common']) > 10:
                    lines.append(f"  ... 还有 {len(comparison['common']) - 10} 个")
                lines.append("")

            if comparison['only_in_dir1']:
                lines.append(f"仅在目录1 ({len(comparison['only_in_dir1'])}):")
                for f in comparison['only_in_dir1'][:10]:
                    lines.append(f"  {f}")
                if len(comparison['only_in_dir1']) > 10:
                    lines.append(f"  ... 还有 {len(comparison['only_in_dir1']) - 10} 个")
                lines.append("")

            if comparison['only_in_dir2']:
                lines.append(f"仅在目录2 ({len(comparison['only_in_dir2'])}):")
                for f in comparison['only_in_dir2'][:10]:
                    lines.append(f"  {f}")
                if len(comparison['only_in_dir2']) > 10:
                    lines.append(f"  ... 还有 {len(comparison['only_in_dir2']) - 10} 个")
                lines.append("")

            if comparison['differing']:
                lines.append(f"有差异的文件 ({len(comparison['differing'])}):")
                for f in comparison['differing']:
                    lines.append(f"  {f}")
                lines.append("")

            summary = f"\n总结: {len(comparison['common'])} 个相同, "
            summary += f"{len(comparison['differing'])} 个不同, "
            summary += f"{len(comparison['only_in_dir1'])} 个只在目录1, "
            summary += f"{len(comparison['only_in_dir2'])} 个只在目录2"
            lines.append(summary)

        else:
            # 文件对比
            lines.append(f"\n文件1: {comparison['file1']}")
            lines.append(f"文件2: {comparison['file2']}")
            lines.append(f"\n是否相同: {'是' if comparison['identical'] else '否'}")
            lines.append(f"对比方法: {comparison['method']}")
            lines.append(f"\n大小1: {comparison['size1']} bytes")
            lines.append(f"大小2: {comparison['size2']} bytes")
            lines.append(f"大小匹配: {'是' if comparison['size_match'] else '否'}")

        report = '\n'.join(lines)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)

        return report


__all__ = ["FileComparator"]
