---
name: file_comparator
description: 文件对比工具 - 对比文件、目录差异，查找重复文件
metadata:
  type: custom
---

# File Comparator Skill

文件对比工具，对比文件和目录差异，查找重复文件。

## 功能特性

- **文件对比** - 快速/内容/Hash 三种对比方式
- **目录对比** - 递归对比两个目录
- **查找重复** - 找出目录中的重复文件
- **生成报告** - 生成对比报告

## 使用方法

### Python API

```python
from skills.file_comparator import FileComparator

comp = FileComparator()

# 对比两个文件
result = comp.compare_files('file1.txt', 'file2.txt', method='content')

# 对比两个目录
result = comp.compare_directories('dir1/', 'dir2/', recursive=True)

# 查找重复文件
duplicates = comp.find_duplicates('/path/to/folder', by_hash=True)

# 生成报告
report = comp.generate_diff_report(result)
print(report)
```

## API 参考

### FileComparator 类

#### `compare_files(file1, file2, method='quick')`
对比两个文件

**参数:**
- `method`: quick/content/hash

#### `compare_directories(dir1, dir2, shallow=True, recursive=True)`
对比两个目录

#### `find_duplicates(directory, by_hash=True, recursive=True)`
查找重复文件

#### `generate_diff_report(comparison, output_file=None)`
生成对比报告
