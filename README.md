# Claude Skills Collection

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub repo](https://img.shields.io/badge/GitHub-publisher--skill%2Fclaude--skill-green?logo=github)](https://github.com/publisher-skill/claude-skill)

这是一个实用的Python技能工具集合，包含多个独立的功能模块，可以作为Claude Code的自定义skills使用，也可以单独导入使用。

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
│   ├── web_crawler/                   # 网页爬虫模块
│   │   ├── __init__.py
│   │   ├── SKILL.md                   # Skill 定义 (Claude Code)
│   │   ├── README.md                  # 详细文档
│   │   ├── web_crawler.py             # 主模块
│   │   ├── example.py                 # 使用示例
│   │   └── requirements.txt           # 依赖
│   └── pdf_word_converter/            # PDF-Word 转换模块
│       ├── __init__.py
│       ├── SKILL.md                   # Skill 定义 (Claude Code)
│       ├── README.md                  # 详细文档
│       ├── pdf_word_converter.py      # 主模块
│       ├── converter.py               # 命令行工具
│       ├── example.py                 # 使用示例
│       └── requirements.txt           # 依赖
└── tests/                             # 测试目录
    ├── __init__.py
    ├── test_web_crawler.py
    └── test_pdf_word_converter.py
```

## Skill 列表

| Skill 名称 | 描述 | 目录 |
|-----------|------|------|
| **Web Crawler** | 基于 requests 和 BeautifulSoup 的网页爬虫工具 | [skills/web_crawler/](./skills/web_crawler/) |
| **PDF-Word Converter** | PDF 与 Word 文档相互转换工具 | [skills/pdf_word_converter/](./skills/pdf_word_converter/) |

## 安装

### 安装所有skills

```bash
git clone https://github.com/publisher-skill/claude-skill.git
cd claude-skill
pip install -r requirements.txt
```

### 单独安装某个skill

```bash
# Web Crawler
pip install requests beautifulsoup4 lxml

# PDF-Word Converter
pip install pdf2docx docx2pdf python-docx
```

### 开发模式安装

```bash
pip install -e ".[dev]"
```

## 使用方式

### 方式1: 作为 Claude Code Skill 使用 (推荐)

每个 skill 在 `skills/` 目录下都可以独立运行，包含完整的 `SKILL.md` 定义文件。

### 方式2: 作为 Python 包导入使用

```python
# 从 skills 导入
from skills.web_crawler import WebCrawler
from skills.pdf_word_converter import PdfWordConverter

# 或者从根目录导入
import sys
sys.path.insert(0, '/path/to/claude-skill')
from web_crawler import WebCrawler
```

## 快速开始

### 运行综合示例

```bash
python example.py
```

### Web Crawler 使用示例

```python
from skills.web_crawler import WebCrawler

crawler = WebCrawler()

# 抓取网页
html = crawler.fetch("https://example.com")

# 提取链接
links = crawler.extract_links(html, "https://example.com")

# 下载图片
crawler.download_image("https://example.com/image.jpg", "output/image.jpg")

# 使用CSS选择器
titles = crawler.select(html, "h1.title")
```

### PDF-Word Converter 使用示例

```python
from skills.pdf_word_converter import PdfWordConverter

converter = PdfWordConverter()

# PDF转Word
converter.pdf_to_word("input.pdf", "output.docx")

# Word转PDF
converter.word_to_pdf("input.docx", "output.pdf")

# 批量转换
converter.convert_folder("input_dir", "output_dir", mode="pdf2word")
```

### 命令行使用

```bash
# PDF-Word Converter 命令行
python skills/pdf_word_converter/converter.py check
python skills/pdf_word_converter/converter.py pdf2word input.pdf
python skills/pdf_word_converter/converter.py word2pdf input.docx
```

详细文档请查看各skill子目录下的 README.md。

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

想要贡献新的skill？请查看 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解详细指南。

简要步骤：

1. 在 `skills/` 目录下创建新的子目录
2. 创建必要的文件（`__init__.py`, 主模块, `SKILL.md`, `README.md`, `example.py`, `requirements.txt`）
3. 在 `skills/__init__.py` 中导出新Skill
4. 更新根目录 `README.md` 添加新Skill说明
5. 提交 Pull Request

## License

MIT License - 详见 [LICENSE](./LICENSE) 文件

## 链接

- GitHub 仓库: https://github.com/publisher-skill/claude-skill
- 问题反馈: https://github.com/publisher-skill/claude-skill/issues
