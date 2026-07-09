---
name: directory_tree
description: 目录树生成器 - 生成美观的目录树结构，支持文件大小显示和导出
metadata:
  type: custom
---

# Directory Tree Skill

目录树生成器，生成美观的目录树结构。

## 功能特性

- **生成目录树** - 直观的树形结构显示
- **文件大小显示** - 显示文件和目录大小
- **深度限制** - 限制显示深度
- **排除模式** - 排除特定文件/目录
- **导出功能** - 导出为文本或 Markdown

## 使用方法

### Python API

```python
from skills.directory_tree import DirectoryTree

tree = DirectoryTree()

# 生成目录树
tree_str = tree.generate('/path/to/folder')
print(tree_str)

# 显示文件大小
tree_str = tree.generate_with_sizes('/path/to/folder')

# 限制深度
tree_str = tree.generate('/path/to/folder', max_depth=3)

# 保存到文件
tree.save_to_file(tree_str, 'output.txt')
```

## API 参考

### DirectoryTree 类

#### `generate(directory, max_depth=None, exclude_patterns=None, include_files=True)`
生成目录树字符串

#### `generate_with_sizes(directory, max_depth=None, exclude_patterns=None)`
生成带文件大小的目录树

#### `generate_markdown(directory, max_depth=None, exclude_patterns=None, include_files=True)`
生成 Markdown 格式的目录树

#### `save_to_file(tree_str, output_file)`
保存到文件
