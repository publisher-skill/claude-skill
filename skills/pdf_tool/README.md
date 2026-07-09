# PDF Tool Skill

PDF 文档处理工具，日常办公必备！

## 安装依赖

```bash
pip install pypdf
```

或使用目录下的 requirements.txt：

```bash
cd skills/pdf_tool
pip install -r requirements.txt
```

## 快速开始

```python
from skills.pdf_tool import PDFTool

pdf = PDFTool()

# 合并 PDF
pdf.merge_pdfs(['part1.pdf', 'part2.pdf'], 'combined.pdf')

# 提取文本
text = pdf.extract_text('document.pdf', 'output.txt')

# 加密 PDF
pdf.encrypt_pdf('document.pdf', 'protected.pdf', 'mypassword')
```

## 使用示例

### 合并多个 PDF

```python
pdfs_to_merge = ['report_part1.pdf', 'report_part2.pdf', 'report_part3.pdf']
pdf.merge_pdfs(pdfs_to_merge, 'report_complete.pdf')
```

### 拆分 PDF

```python
# 提取第3页
pdf.split_pdf('document.pdf', 'output_dir', page=2)

# 提取第1-5页
pdf.split_pdf('document.pdf', 'output_dir', start=0, end=4)

# 拆分为单页
pdf.split_pdf('document.pdf', 'output_dir')
```

### 提取文本

```python
# 只返回文本，不保存
text = pdf.extract_text('document.pdf')

# 保存为 TXT 文件
text = pdf.extract_text('document.pdf', 'document_content.txt')
```

### 加密/解密

```python
# 加密
pdf.encrypt_pdf('document.pdf', 'document_secure.pdf', 'mypassword123')

# 解密
pdf.decrypt_pdf('document_secure.pdf', 'document_unlocked.pdf', 'mypassword123')
```

### 删除页面

```python
# 删除第2和第5页（从0开始计数）
pdf.remove_pages('document.pdf', 'document_clean.pdf', [1, 4])
```

### 重排页面

```python
# 重新排列：原顺序2，3，1，4
pdf.reorder_pages('document.pdf', 'document_new.pdf', [1, 2, 0, 3])
```

### 获取 PDF 信息

```python
info = pdf.get_info('document.pdf')
print(f"页数: {info['pages']}")
print(f"作者: {info['author']}")
print(f"标题: {info['title']}")
print(f"是否加密: {info['encrypted']}")
```

## 运行示例

```bash
cd skills/pdf_tool
python example.py
```
