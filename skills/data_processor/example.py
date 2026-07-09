"""
Data Processor Skill 使用示例
"""

import os
import sys
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from skills.data_processor import DataProcessor


def create_test_csv(filepath):
    """创建测试 CSV 文件"""
    data = [
        {'name': 'Alice', 'age': '25', 'city': 'Beijing'},
        {'name': 'Bob', 'age': '30', 'city': 'Shanghai'},
        {'name': 'Charlie', 'age': '35', 'city': 'Guangzhou'},
        {'name': 'Alice', 'age': '25', 'city': 'Beijing'},  # 重复数据
    ]

    proc = DataProcessor()
    proc.write_csv(data, filepath)


def example_read_write_csv():
    """CSV 读写示例"""
    print("="*60)
    print("示例1: CSV 读写")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = os.path.join(temp_dir, 'input.csv')
        output_file = os.path.join(temp_dir, 'output.csv')

        create_test_csv(input_file)
        print(f"\n创建测试文件: {input_file}")

        proc = DataProcessor()

        data = proc.read_csv(input_file)
        print(f"\n读取到 {len(data)} 行数据:")
        for row in data:
            print(f"  {row}")

        proc.write_csv(data, output_file)
        print(f"\n已写入: {output_file}")


def example_data_filtering():
    """数据过滤示例"""
    print("\n" + "="*60)
    print("示例2: 数据过滤和排序")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = os.path.join(temp_dir, 'input.csv')
        create_test_csv(input_file)

        proc = DataProcessor()
        data = proc.read_csv(input_file)

        # 过滤数据
        filtered = proc.filter_data(data, lambda x: int(x['age']) > 25)
        print(f"\n过滤后 (age > 25): {len(filtered)} 行")
        for row in filtered:
            print(f"  {row}")

        # 排序数据
        sorted_data = proc.sort_data(data, 'age', reverse=True)
        print(f"\n按 age 降序排列:")
        for row in sorted_data:
            print(f"  {row}")


def example_deduplication():
    """数据去重示例"""
    print("\n" + "="*60)
    print("示例3: 数据去重")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = os.path.join(temp_dir, 'input.csv')
        create_test_csv(input_file)

        proc = DataProcessor()
        data = proc.read_csv(input_file)

        print(f"\n原始数据: {len(data)} 行")

        deduplicated = proc.deduplicate_data(data, key_fields=['name', 'age'])
        print(f"去重后: {len(deduplicated)} 行")
        for row in deduplicated:
            print(f"  {row}")


def example_format_conversion():
    """格式转换示例"""
    print("\n" + "="*60)
    print("示例4: CSV 与 JSON 互转")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        csv_file = os.path.join(temp_dir, 'data.csv')
        json_file = os.path.join(temp_dir, 'data.json')
        csv_back_file = os.path.join(temp_dir, 'data_back.csv')

        create_test_csv(csv_file)

        proc = DataProcessor()

        # CSV 转 JSON
        proc.csv_to_json(csv_file, json_file)
        print(f"\nCSV 已转为 JSON: {json_file}")

        json_data = proc.read_json(json_file)
        print(f"JSON 数据: {json_data}")

        # JSON 转 CSV
        proc.json_to_csv(json_file, csv_back_file)
        print(f"\nJSON 已转回 CSV: {csv_back_file}")


def example_statistics():
    """数据统计示例"""
    print("\n" + "="*60)
    print("示例5: 数据统计")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = os.path.join(temp_dir, 'input.csv')
        create_test_csv(input_file)

        proc = DataProcessor()
        data = proc.read_csv(input_file)

        stats = proc.get_statistics(data, numeric_fields=['age'])

        print(f"\n统计信息:")
        print(f"  总行数: {stats['total_rows']}")
        print(f"  字段: {stats['fields']}")
        print(f"  空值统计: {stats['field_null_counts']}")
        print(f"  唯一值统计: {stats['field_unique_counts']}")


if __name__ == "__main__":
    example_read_write_csv()
    example_data_filtering()
    example_deduplication()
    example_format_conversion()
    example_statistics()
