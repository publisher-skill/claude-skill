"""
PDF Tool Skill 使用示例
"""

import os
import sys
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from skills.pdf_tool import PDFTool


def create_test_pdfs(temp_dir):
    """创建测试 PDF"""
    try:
        from pypdf import PdfWriter
        from pathlib import Path

        # 创建几个简单的测试 PDF
        for i in range(3):
            writer = PdfWriter()
            writer.add_blank_page(width=612, height=792)
            output_path = os.path.join(temp_dir, f"test{i+1}.pdf")
            with open(output_path, 'wb') as f:
                writer.write(f)
            print(f"创建测试 PDF: {output_path}")

        return True
    except Exception as e:
        print(f"无法创建测试 PDF: {e}")
        return False


def example_basic_use():
    """基本使用示例"""
    print("="*60)
    print("示例 1: PDF 工具基本使用")
    print("="*60)

    pdf = PDFTool()

    # 检查是否可用
    if not pdf.is_available():
        print("\n❌ PDF 工具不可用")
        print("请运行: pip install pypdf")
        return

    print("\n✅ PDF 工具已就绪")

    with tempfile.TemporaryDirectory() as temp_dir:
        if not create_test_pdfs(temp_dir):
            print("跳过示例演示")
            return

        print("\n" + "="*60)
        print("可用功能:")
        print("="*60)
        print("1. merge_pdfs    - 合并 PDF")
        print("2. split_pdf     - 拆分 PDF")
        print("3. extract_text  - 提取文本")
        print("4. encrypt_pdf   - 加密 PDF")
        print("5. decrypt_pdf   - 解密 PDF")
        print("6. get_info      - 获取 PDF 信息")
        print("7. remove_pages  - 删除页面")
        print("8. reorder_pages - 重排页面")


def example_merge_pdfs():
    """合并 PDF 示例"""
    print("\n" + "="*60)
    print("示例 2: 合并 PDF")
    print("="*60)

    print("""
使用方法:
    pdf.merge_pdfs(['file1.pdf', 'file2.pdf'], 'merged.pdf')
    """)


def example_split_pdf():
    """拆分 PDF 示例"""
    print("\n" + "="*60)
    print("示例 3: 拆分 PDF")
    print("="*60)

    print("""
使用方法:
    # 拆分所有页面
    pdf.split_pdf('input.pdf', 'output_dir')

    # 提取单个页面（第3页，从0开始）
    pdf.split_pdf('input.pdf', 'output_dir', page=2)

    # 提取范围（第1-5页）
    pdf.split_pdf('input.pdf', 'output_dir', start=0, end=4)
    """)


def example_encryption():
    """加密解密示例"""
    print("\n" + "="*60)
    print("示例 4: 加密/解密 PDF")
    print("="*60)

    print("""
使用方法:
    # 加密
    pdf.encrypt_pdf('document.pdf', 'secure.pdf', 'password123')

    # 解密
    pdf.decrypt_pdf('secure.pdf', 'unlocked.pdf', 'password123')
    """)


def quick_reference():
    """快速参考"""
    print("\n" + "="*60)
    print("PDF 工具速查")
    print("="*60)
    print("""
日常办公最常用:

1. 合并月度报告
    pdf.merge_pdfs(['Jan.pdf', 'Feb.pdf'], 'Quarter1.pdf')

2. 提取合同文本
    text = pdf.extract_text('contract.pdf', 'contract_text.txt')

3. 保护敏感文档
    pdf.encrypt_pdf('confidential.pdf', 'protected.pdf', 'secret123')

4. 拆分大型文档
    pdf.split_pdf('large.pdf', 'pages', start=0, end=9)

5. 获取文档信息
    info = pdf.get_info('document.pdf')
    print(f"页数: {info['pages']}")
    """)


if __name__ == "__main__":
    example_basic_use()
    example_merge_pdfs()
    example_split_pdf()
    example_encryption()
    quick_reference()
