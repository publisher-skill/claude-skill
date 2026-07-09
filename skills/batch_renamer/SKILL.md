---
name: batch_renamer
description: 批量重命名器 - 支持正则、序号、前缀后缀、替换文本等多种重命名方式
metadata:
  type: custom
---

# Batch Renamer Skill

批量重命名器，支持多种重命名方式。

## 功能特性

- **正则表达式重命名** - 强大的模式匹配
- **序号重命名** - 自动生成有序文件名
- **添加前缀/后缀** - 批量添加前缀或后缀
- **替换文本** - 批量替换文件名中的文本
- **改变大小写** - 批量修改大小写
- **预览模式** - 支持 dry-run 预览结果

## 使用方法

### Python API

```python
from skills.batch_renamer import BatchRenamer

renamer = BatchRenamer()

# 序号重命名
renamer.rename_with_sequence('/path/to/folder', prefix='photo', start=1)

# 添加前缀
renamer.add_prefix('/path/to/folder', '2024_')

# 替换文本
renamer.replace_text('/path/to/folder', 'old', 'new')

# 正则重命名
renamer.rename_with_pattern('/path/to/folder', r'IMG_(\d+)', r'photo_\1')

# 预览模式
renamer.rename_with_sequence('/path/to/folder', dry_run=True)
```

## API 参考

### BatchRenamer 类

#### `rename_with_pattern(directory, pattern, replacement, dry_run=False)`
使用正则表达式重命名

#### `rename_with_sequence(directory, prefix='file', start=1, padding=3, dry_run=False)`
使用序号重命名

#### `add_prefix(directory, prefix, dry_run=False)`
添加前缀

#### `add_suffix(directory, suffix, before_ext=True, dry_run=False)`
添加后缀

#### `replace_text(directory, old_text, new_text, case_sensitive=True, dry_run=False)`
替换文本

#### `change_case(directory, case_type='lower', dry_run=False)`
改变大小写（lower/upper/title）

#### `get_summary()`
获取操作摘要
