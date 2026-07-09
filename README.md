# Claude Skills Collection

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub repo](https://img.shields.io/badge/GitHub-publisher--skill%2Fclaude--skill-green?logo=github)](https://github.com/publisher-skill/claude-skill)

这是一个实用的 Python 技能工具集合，包含多个独立的功能模块，可以作为 Claude Code 的自定义 skills 使用，也可以单独导入使用。

## Skill 列表

### 📁 文件处理类 (4个)

| Skill 名称 | 描述 | 目录 |
|-----------|------|------|
| **File Organizer** | 按类型、日期、扩展名自动整理文件 | [skills/file_organizer/](./skills/file_organizer/) |
| **Batch Renamer** | 批量重命名文件（正则、序号、前缀等） | [skills/batch_renamer/](./skills/batch_renamer/) |
| **Directory Tree** | 生成目录树，显示文件大小 | [skills/directory_tree/](./skills/directory_tree/) |
| **File Comparator** | 对比文件/目录差异，查找重复文件 | [skills/file_comparator/](./skills/file_comparator/) |

### 📊 数据处理类 (1个+)

| Skill 名称 | 描述 | 目录 |
|-----------|------|------|
| **Data Processor** | CSV/JSON 读写、转换、过滤、合并 | [skills/data_processor/](./skills/data_processor/) |

### 🔒 开发工具类 (1个+)

| Skill 名称 | 描述 | 目录 |
|-----------|------|------|
| **Password Generator** | 密码生成器（安全密码、易记密码、PIN码） | [skills/password_generator/](./skills/password_generator/) |

### 🌐 网络工具类 (2个)

| Skill 名称 | 描述 | 目录 |
|-----------|------|------|
| **Web Crawler** | 基于 requests 和 BeautifulSoup 的网页爬虫工具 | [skills/web_crawler/](./skills/web_crawler/) |
| **PDF-Word Converter** | PDF 与 Word 文档相互转换工具 | [skills/pdf_word_converter/](./skills/pdf_word_converter/) |

## 安装

### 安装所有 skills

```bash
git clone https://github.com/publisher-skill/claude-skill.git
cd claude-skill
pip install -r requirements.txt
```

### 单独安装某个 skill

每个 skill 都有自己的 `requirements.txt`，可以单独安装：

```bash
# Web Crawler
cd skills/web_crawler
pip install -r requirements.txt

# PDF-Word Converter
cd skills/pdf_word_converter
pip install -r requirements.txt
```

### 开发模式安装

```bash
pip install -e ".[dev]"
```

## 快速开始

### 运行综合示例

```bash
python example.py
```

### 文件整理示例

```python
from skills.file_organizer import FileOrganizer

organizer = FileOrganizer()

# 按类型整理下载文件夹
stats = organizer.organize_by_type('~/Downloads')

# 预览整理结果
stats = organizer.organize_by_type('~/Downloads', dry_run=True)
```

### 密码生成示例

```python
from skills.password_generator import PasswordGenerator

gen = PasswordGenerator()

# 生成安全密码
password = gen.generate(length=16)

# 生成易记密码
memorable = gen.generate_memorable(word_count=4)

# 检查强度
result = gen.check_strength(password)
print(f"强度: {result['strength_text']}")
```

### 数据处理示例

```python
from skills.data_processor import DataProcessor

proc = DataProcessor()

# 读取 CSV
data = proc.read_csv('data.csv')

# 过滤数据
filtered = proc.filter_data(data, lambda x: int(x['age']) > 18)

# 格式转换
proc.csv_to_json('data.csv', 'data.json')
```

更多示例请参考各个 skill 目录下的 `example.py` 和 `README.md`。

## 项目结构

```
claude-skill/
├── README.md                          # 本文件
├── __init__.py                        # 包入口
├── pyproject.toml                     # 项目配置
├── requirements.txt                   # 所有依赖
├── example.py                         # 综合示例
├── LICENSE                            # MIT 许可证
├── CONTRIBUTING.md                    # 贡献指南
├── .gitignore                         # Git 忽略文件
├── skills/                            # Claude Code Skills
│   ├── __init__.py
│   │
│   ├── file_organizer/               # 文件整理器
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── file_organizer.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── batch_renamer/                 # 批量重命名器
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── batch_renamer.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── directory_tree/                # 目录树生成器
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── directory_tree.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── file_comparator/               # 文件对比工具
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── file_comparator.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── data_processor/                # 数据处理器
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── data_processor.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── password_generator/            # 密码生成器
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── password_generator.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── web_crawler/                  # 网页爬虫
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── web_crawler.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   └── pdf_word_converter/           # PDF-Word 转换
│       ├── __init__.py
│       ├── SKILL.md
│       ├── README.md
│       ├── pdf_word_converter.py
│       ├── converter.py
│       ├── example.py
│       └── requirements.txt
│
└── tests/                             # 测试目录
    ├── __init__.py
    ├── test_web_crawler.py
    └── test_pdf_word_converter.py
```

## 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_web_crawler.py -v

# 显示覆盖率
pytest --cov=skills tests/
```

## 添加新 Skill

想要贡献新的 skill？请查看 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解详细指南。

简要步骤：

1. 在 `skills/` 目录下创建新的子目录
2. 创建必要的文件（`__init__.py`, 主模块, `SKILL.md`, `README.md`, `example.py`, `requirements.txt`）
3. 在 `skills/__init__.py` 中添加新 skill
4. 更新根目录 `README.md` 添加新 skill 说明
5. 提交 Pull Request

## License

MIT License - 详见 [LICENSE](./LICENSE) 文件

## 链接

- GitHub 仓库: https://github.com/publisher-skill/claude-skill
- 问题反馈: https://github.com/publisher-skill/claude-skill/issues
