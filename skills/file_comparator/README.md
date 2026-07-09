# File Comparator Skill

文件对比工具，对比文件和目录差异，查找重复文件。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

```python
from skills.file_comparator import FileComparator

comp = FileComparator()

# 对比两个文件
result = comp.compare_files('file1.txt', 'file2.txt', method='content')

# 对比两个目录
result = comp.compare_directories('dir1/', 'dir2/', recursive=True)

# 查找重复文件
duplicates = comp.find_duplicates('/path/to/folder')
```

## 运行示例

```bash
cd skills/file_comparator
python example.py
```
