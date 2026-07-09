"""
Data Processor Skill
CSV/Excel 数据处理工具
"""

import os
import csv
import json
from typing import List, Dict, Any, Optional, Union, Callable
from pathlib import Path


class DataProcessor:
    """数据处理器"""

    def __init__(self):
        """初始化"""
        pass

    def read_csv(self, filepath: str, delimiter: str = ',',
                encoding: str = 'utf-8') -> List[Dict]:
        """读取 CSV 文件

        Args:
            filepath: 文件路径
            delimiter: 分隔符
            encoding: 编码

        Returns:
            数据列表
        """
        filepath = os.path.abspath(filepath)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件不存在: {filepath}")

        data = []
        with open(filepath, 'r', encoding=encoding, newline='') as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                data.append(dict(row))

        return data

    def write_csv(self, data: List[Dict], filepath: str,
                 delimiter: str = ',', encoding: str = 'utf-8',
                 headers: Optional[List[str]] = None):
        """写入 CSV 文件

        Args:
            data: 数据列表
            filepath: 输出路径
            delimiter: 分隔符
            encoding: 编码
            headers: 表头（可选）
        """
        if not data:
            raise ValueError("数据为空")

        if headers is None:
            headers = list(data[0].keys())

        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)

        with open(filepath, 'w', encoding=encoding, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers, delimiter=delimiter)
            writer.writeheader()
            for row in data:
                writer.writerow(row)

    def read_json(self, filepath: str, encoding: str = 'utf-8') -> Any:
        """读取 JSON 文件

        Args:
            filepath: 文件路径
            encoding: 编码

        Returns:
            JSON 数据
        """
        filepath = os.path.abspath(filepath)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件不存在: {filepath}")

        with open(filepath, 'r', encoding=encoding) as f:
            return json.load(f)

    def write_json(self, data: Any, filepath: str,
                  encoding: str = 'utf-8', indent: int = 2):
        """写入 JSON 文件

        Args:
            data: 数据
            filepath: 输出路径
            encoding: 编码
            indent: 缩进
        """
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)

        with open(filepath, 'w', encoding=encoding) as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)

    def csv_to_json(self, csv_file: str, json_file: str,
                    delimiter: str = ',', encoding: str = 'utf-8'):
        """CSV 转 JSON

        Args:
            csv_file: CSV 文件路径
            json_file: JSON 文件路径
            delimiter: 分隔符
            encoding: 编码
        """
        data = self.read_csv(csv_file, delimiter, encoding)
        self.write_json(data, json_file, encoding)

    def json_to_csv(self, json_file: str, csv_file: str,
                   delimiter: str = ',', encoding: str = 'utf-8'):
        """JSON 转 CSV

        Args:
            json_file: JSON 文件路径
            csv_file: CSV 文件路径
            delimiter: 分隔符
            encoding: 编码
        """
        data = self.read_json(json_file, encoding)
        if not isinstance(data, list):
            raise ValueError("JSON 数据必须是数组格式")
        if data and not isinstance(data[0], dict):
            raise ValueError("JSON 数组元素必须是对象")

        self.write_csv(data, csv_file, delimiter, encoding)

    def filter_data(self, data: List[Dict],
                   condition: Callable[[Dict], bool]) -> List[Dict]:
        """过滤数据

        Args:
            data: 数据列表
            condition: 过滤函数

        Returns:
            过滤后的数据
        """
        return [row for row in data if condition(row)]

    def select_fields(self, data: List[Dict],
                     fields: List[str]) -> List[Dict]:
        """选择字段

        Args:
            data: 数据列表
            fields: 要保留的字段

        Returns:
            处理后的数据
        """
        return [{k: row.get(k, '') for k in fields} for row in data]

    def sort_data(self, data: List[Dict],
                 key: str, reverse: bool = False) -> List[Dict]:
        """排序数据

        Args:
            data: 数据列表
            key: 排序字段
            reverse: 是否逆序

        Returns:
            排序后的数据
        """
        return sorted(data, key=lambda x: x.get(key, ''), reverse=reverse)

    def merge_csv_files(self, filepaths: List[str],
                       output_file: str,
                       delimiter: str = ',',
                       encoding: str = 'utf-8',
                       include_source: bool = False):
        """合并多个 CSV 文件

        Args:
            filepaths: 文件路径列表
            output_file: 输出文件
            delimiter: 分隔符
            encoding: 编码
            include_source: 是否包含来源文件列
        """
        all_data = []

        for filepath in filepaths:
            data = self.read_csv(filepath, delimiter, encoding)
            if include_source:
                filename = os.path.basename(filepath)
                for row in data:
                    row['_source_file'] = filename
            all_data.extend(data)

        if all_data:
            self.write_csv(all_data, output_file, delimiter, encoding)

    def deduplicate_data(self, data: List[Dict],
                        key_fields: Optional[List[str]] = None) -> List[Dict]:
        """数据去重

        Args:
            data: 数据列表
            key_fields: 关键字段列表（None 则整行对比）

        Returns:
            去重后的数据
        """
        seen = set()
        result = []

        for row in data:
            if key_fields:
                key = tuple(str(row.get(k, '')) for k in key_fields)
            else:
                key = tuple(sorted((k, str(v)) for k, v in row.items()))

            if key not in seen:
                seen.add(key)
                result.append(row)

        return result

    def transform_field(self, data: List[Dict],
                       field: str,
                       transform_func: Callable[[Any], Any]) -> List[Dict]:
        """转换字段

        Args:
            data: 数据列表
            field: 字段名
            transform_func: 转换函数

        Returns:
            处理后的数据
        """
        result = []
        for row in data:
            new_row = row.copy()
            if field in new_row:
                new_row[field] = transform_func(new_row[field])
            result.append(new_row)
        return result

    def get_statistics(self, data: List[Dict],
                      numeric_fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """获取数据统计

        Args:
            data: 数据列表
            numeric_fields: 数值字段列表

        Returns:
            统计信息
        """
        if not data:
            return {'total_rows': 0, 'fields': []}

        stats = {
            'total_rows': len(data),
            'fields': list(data[0].keys()),
            'field_null_counts': {},
            'field_unique_counts': {},
        }

        for field in stats['fields']:
            values = [row.get(field, '') for row in data]
            null_count = sum(1 for v in values if v is None or v == '')
            stats['field_null_counts'][field] = null_count
            stats['field_unique_counts'][field] = len(set(values))

            # 如果是数值字段，计算统计信息
            if numeric_fields and field in numeric_fields:
                try:
                    nums = [float(v) for v in values if v not in (None, '')]
                    if nums:
                        stats[f'{field}_min'] = min(nums)
                        stats[f'{field}_max'] = max(nums)
                        stats[f'{field}_avg'] = sum(nums) / len(nums)
                except (ValueError, TypeError):
                    pass

        return stats


__all__ = ["DataProcessor"]
