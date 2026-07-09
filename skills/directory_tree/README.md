# Directory Tree Skill

目录树生成器，生成美观的目录树结构。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

```python
from skills.directory_tree import DirectoryTree

tree = DirectoryTree()

# 生成目录树
tree_str = tree.generate('/path/to/folder')
print(tree_str)

# 显示文件大小
tree_str = tree.generate_with_sizes('/path/to/folder')

# 保存到文件
tree.save_to_file(tree_str, 'output.txt')
```

## 运行示例

```bash
cd skills/directory_tree
python example.py
```
