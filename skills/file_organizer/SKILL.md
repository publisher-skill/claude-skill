---
name: file_organizer
description: 文件整理器 - 按类型、日期、扩展名自动整理文件夹中的文件
metadata:
  type: custom
---

# File Organizer Skill

文件整理器，可以按类型、日期、扩展名自动整理文件夹中的文件。

## 功能特性

- **按类型整理** - 自动识别文件类型（图片、文档、视频、音频等）
- **按日期整理** - 按文件修改日期创建文件夹整理
- **按扩展名整理** - 按文件扩展名分类整理
- **预览模式** - 支持 dry-run 预览整理结果
- **自动重命名** - 处理重名文件

## 使用方法

### Python API

```python
from skills.file_organizer import FileOrganizer

organizer = FileOrganizer()

# 按类型整理
stats = organizer.organize_by_type('/path/to/folder')

# 按日期整理
stats = organizer.organize_by_date('/path/to/folder')

# 按扩展名整理
stats = organizer.organize_by_extension('/path/to/folder')

# 预览模式（不实际移动）
stats = organizer.organize_by_type('/path/to/folder', dry_run=True)

# 获取摘要
summary = organizer.get_summary()
```

## API 参考

### FileOrganizer 类

#### `__init__()`
初始化文件整理器

#### `organize_by_type(source_dir, target_dir=None, dry_run=False)`
按文件类型整理

**参数:**
- `source_dir`: 源目录路径
- `target_dir`: 目标目录路径（默认同源目录）
- `dry_run`: 是否仅预览（True/False）

#### `organize_by_date(source_dir, target_dir=None, date_format="%Y-%m", dry_run=False)`
按日期整理

**参数:**
- `date_format`: 日期格式，如 "%Y-%m" 或 "%Y-%m-%d"

#### `organize_by_extension(source_dir, target_dir=None, dry_run=False)`
按扩展名整理

#### `get_summary()`
获取操作摘要统计
