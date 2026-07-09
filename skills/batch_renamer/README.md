# Batch Renamer Skill

批量重命名器，支持多种重命名方式。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

```python
from skills.batch_renamer import BatchRenamer

renamer = BatchRenamer()

# 序号重命名
renamer.rename_with_sequence('/path/to/folder', prefix='photo', start=1)

# 添加前缀
renamer.add_prefix('/path/to/folder', '2024_')

# 替换文本
renamer.replace_text('/path/to/folder', 'old', 'new')

# 预览模式
renamer.rename_with_sequence('/path/to/folder', dry_run=True)
```

## 运行示例

```bash
cd skills/batch_renamer
python example.py
```
