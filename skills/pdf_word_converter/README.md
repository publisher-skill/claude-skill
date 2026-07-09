# PDF-Word Converter Skill

PDF与Word文档相互转换工具。

## 安装依赖

```bash
pip install -r requirements.txt
```

或者单独安装：

```bash
pip install pdf2docx docx2pdf python-docx
```

## 注意事项

- **PDF转Word**: 仅依赖 `pdf2docx`，跨平台可用
- **Word转PDF**: 需要Microsoft Word (Windows) 或 LibreOffice (Linux/Mac)

## 快速开始

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
# 检查依赖
python converter.py check

# PDF转Word
python converter.py pdf2word input.pdf output.docx

# Word转PDF
python converter.py word2pdf input.docx output.pdf

# 批量转换文件夹
python converter.py folder ./input_dir ./output_dir --mode pdf2word
```

## 功能特性

- ✅ PDF转Word (.pdf -> .docx)
- ✅ Word转PDF (.docx/.doc -> .pdf)
- ✅ 批量转换文件夹
- ✅ 支持页码范围（PDF转Word）
- ✅ 保留原始格式
- ✅ 命令行支持
- ✅ 友好的错误提示

## 运行示例

```bash
cd claude_skills/pdf_word_converter
python example.py
```
