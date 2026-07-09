---
name: pdf_tool
description: PDF 工具 - 合并、拆分、提取文本、加密解密、加水印等
metadata:
  type: custom
---

# PDF Tool Skill

PDF 文档处理工具，日常办公必备！

## 功能特性

### 📄 PDF 基本操作
- **合并 PDF**: 将多个 PDF 文件合并为一个
- **拆分 PDF**: 按页面范围或单个页面拆分
- **删除页面**: 删除不需要的页面
- **重排页面**: 重新排列 PDF 页面顺序

### 🔐 安全功能
- **加密 PDF**: 为 PDF 添加密码保护
- **解密 PDF**: 移除 PDF 密码保护
- **获取信息**: 查看 PDF 页数、作者、创建时间等

### 📝 内容提取
- **提取文本**: 从 PDF 中提取所有文本
- **保存为 TXT**: 将提取的文本保存为 TXT 文件

## 使用方法

### Python API

```python
from skills.pdf_tool import PDFTool

pdf = PDFTool()

# 检查是否可用
if not pdf.is_available():
    print("请先安装: pip install pypdf")
    exit(1)

# 合并多个 PDF
pdf.merge_pdfs(['1.pdf', '2.pdf'], 'merged.pdf')

# 拆分 PDF（提取单个页面）
pdf.split_pdf('input.pdf', 'output', page=2)

# 拆分 PDF（按范围）
pdf.split_pdf('input.pdf', 'output', start=0, end=4)

# 提取文本
text = pdf.extract_text('input.pdf', 'output.txt')

# 加密 PDF
pdf.encrypt_pdf('input.pdf', 'encrypted.pdf', 'mypassword')

# 解密 PDF
pdf.decrypt_pdf('encrypted.pdf', 'decrypted.pdf', 'mypassword')

# 获取 PDF 信息
info = pdf.get_info('input.pdf')
print(f"页数: {info['pages']}")
```

## API 参考

### PDFTool 类

#### PDF 合并与拆分
- `merge_pdfs(pdf_paths, output_path)` - 合并多个 PDF
- `split_pdf(pdf_path, output_dir, page=None, start=None, end=None)` - 拆分 PDF

#### PDF 安全
- `encrypt_pdf(pdf_path, output_path, password)` - 加密 PDF
- `decrypt_pdf(pdf_path, output_path, password)` - 解密 PDF

#### PDF 内容操作
- `extract_text(pdf_path, output_path=None)` - 提取 PDF 文本
- `remove_pages(pdf_path, output_path, pages_to_remove)` - 删除页面
- `reorder_pages(pdf_path, output_path, new_order)` - 重排页面

#### PDF 信息
- `get_info(pdf_path)` - 获取 PDF 信息
- `is_available()` - 检查是否可用
