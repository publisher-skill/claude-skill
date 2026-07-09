---
name: data_processor
description: 数据处理器 - CSV/Excel/JSON 读写、转换、过滤、合并等数据处理
metadata:
  type: custom
---

# Data Processor Skill

数据处理器，CSV/JSON 读写、转换、过滤、合并等。

## 功能特性

- **CSV 读写** - 读取和写入 CSV 文件
- **JSON 读写** - 读取和写入 JSON 文件
- **格式转换** - CSV 与 JSON 互转
- **数据过滤** - 按条件过滤数据
- **数据排序** - 按字段排序
- **数据合并** - 合并多个 CSV 文件
- **数据去重** - 去除重复数据
- **数据统计** - 获取数据统计信息

## 使用方法

### Python API

```python
from skills.data_processor import DataProcessor

proc = DataProcessor()

# 读取 CSV
data = proc.read_csv('data.csv')

# 写入 CSV
proc.write_csv(data, 'output.csv')

# 过滤数据
filtered = proc.filter_data(data, lambda x: int(x['age']) > 18)

# 转换格式
proc.csv_to_json('data.csv', 'data.json')

# 数据统计
stats = proc.get_statistics(data)
```

## API 参考

### DataProcessor 类

#### `read_csv(filepath, delimiter=',', encoding='utf-8')`
读取 CSV 文件

#### `write_csv(data, filepath, delimiter=',', encoding='utf-8', headers=None)`
写入 CSV 文件

#### `read_json(filepath, encoding='utf-8')`
读取 JSON 文件

#### `write_json(data, filepath, encoding='utf-8', indent=2)`
写入 JSON 文件

#### `csv_to_json(csv_file, json_file, delimiter=',', encoding='utf-8')`
CSV 转 JSON

#### `json_to_csv(json_file, csv_file, delimiter=',', encoding='utf-8')`
JSON 转 CSV

#### `filter_data(data, condition)`
过滤数据

#### `select_fields(data, fields)`
选择字段

#### `sort_data(data, key, reverse=False)`
排序数据

#### `merge_csv_files(filepaths, output_file, delimiter=',', encoding='utf-8', include_source=False)`
合并 CSV 文件

#### `deduplicate_data(data, key_fields=None)`
数据去重

#### `transform_field(data, field, transform_func)`
转换字段

#### `get_statistics(data, numeric_fields=None)`
获取数据统计
