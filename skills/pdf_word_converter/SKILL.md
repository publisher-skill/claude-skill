---
name: pdf-word-converter
description: PDF与Word文档相互转换的skill，支持PDF转Word、Word转PDF
metadata:
  type: custom
---

# PDF-Word Converter Skill

PDF与Word文档相互转换工具。

## 功能特性

- PDF转Word (.pdf -> .docx)
- Word转PDF (.docx/.doc -> .pdf)
- 批量转换文件夹
- 保留原始格式
- 命令行支持

## 安装依赖

```bash
pip install pdf2docx docx2pdf python-docx
```

注意：Word转PDF需要Microsoft Word (Windows) 或 LibreOffice (Linux/Mac)。

## 使用方法

### Python API

```python
from claude_skills.pdf_word_converter import PdfWordConverter

converter = PdfWordConverter()

# PDF转Word
converter.pdf_to_word("input.pdf", "output.docx")

# Word转PDF
converter.word_to_pdf("input.docx", "output.pdf")

# 批量转换文件夹
converter.convert_folder("input_dir", "output_dir", "pdf2word")
```

### 命令行使用

```bash
# PDF转Word
python converter.py pdf2word input.pdf output.docx

# Word转PDF
python converter.py word2pdf input.docx output.pdf

# 批量转换
python converter.py folder input_dir output_dir --mode pdf2word
```

## API 参考

### PdfWordConverter类

#### `__init__()`

初始化转换器。

#### `pdf_to_word(pdf_path, docx_path, start=0, end=None)`

将PDF转换为Word文档。

**参数:**
- `pdf_path` (str): 输入PDF文件路径
- `docx_path` (str): 输出Word文件路径
- `start` (int, optional): 起始页码（从0开始）
- `end` (int, optional): 结束页码

#### `word_to_pdf(docx_path, pdf_path)`

将Word文档转换为PDF。

**参数:**
- `docx_path` (str): 输入Word文件路径
- `pdf_path` (str): 输出PDF文件路径

#### `convert_folder(input_dir, output_dir, mode)`

批量转换文件夹中的文档。

**参数:**
- `input_dir` (str): 输入文件夹路径
- `output_dir` (str): 输出文件夹路径
- `mode` (str): 转换模式，'pdf2word' 或 'word2pdf'
