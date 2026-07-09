"""
PDF Tool Skill
PDF 文档处理工具
"""

import os
from typing import List, Optional, Tuple


class PDFTool:
    """PDF 工具"""

    def __init__(self):
        """初始化"""
        self._pypdf_available = False
        self._check_dependencies()

    def _check_dependencies(self):
        """检查依赖"""
        try:
            import pypdf
            self._pypdf_available = True
        except ImportError:
            self._pypdf_available = False

    def merge_pdfs(self, pdf_paths: List[str], output_path: str) -> str:
        """合并多个 PDF

        Args:
            pdf_paths: PDF 文件路径列表
            output_path: 输出文件路径

        Returns:
            输出文件路径
        """
        if not self._pypdf_available:
            raise ImportError("请先安装: pip install pypdf")

        from pypdf import PdfWriter

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        merger = PdfWriter()
        for pdf in pdf_paths:
            if os.path.exists(pdf):
                merger.append(pdf)

        merger.write(output_path)
        merger.close()
        return output_path

    def split_pdf(self, pdf_path: str, output_dir: str, page: Optional[int] = None,
                  start: Optional[int] = None, end: Optional[int] = None) -> List[str]:
        """拆分 PDF

        Args:
            pdf_path: PDF 文件路径
            output_dir: 输出目录
            page: 拆分单个页面（从0开始）
            start: 起始页面
            end: 结束页面

        Returns:
            输出文件路径列表
        """
        if not self._pypdf_available:
            raise ImportError("请先安装: pip install pypdf")

        from pypdf import PdfReader, PdfWriter

        os.makedirs(output_dir, exist_ok=True)

        reader = PdfReader(pdf_path)
        output_files = []

        if page is not None:
            writer = PdfWriter()
            if page < len(reader.pages):
                writer.add_page(reader.pages[page])
                output_path = os.path.join(output_dir, f"page_{page + 1}.pdf")
                writer.write(output_path)
                writer.close()
                output_files.append(output_path)
        elif start is not None or end is not None:
            start_page = start or 0
            end_page = end or len(reader.pages) - 1
            end_page = min(end_page, len(reader.pages) - 1)

            writer = PdfWriter()
            for i in range(start_page, end_page + 1):
                writer.add_page(reader.pages[i])
            output_path = os.path.join(output_dir, f"pages_{start_page + 1}-{end_page + 1}.pdf")
            writer.write(output_path)
            writer.close()
            output_files.append(output_path)
        else:
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                output_path = os.path.join(output_dir, f"page_{i + 1}.pdf")
                writer.write(output_path)
                writer.close()
                output_files.append(output_path)

        return output_files

    def extract_text(self, pdf_path: str, output_path: Optional[str] = None) -> str:
        """提取 PDF 文本

        Args:
            pdf_path: PDF 文件路径
            output_path: 输出文件路径（可选）

        Returns:
            提取的文本内容
        """
        if not self._pypdf_available:
            raise ImportError("请先安装: pip install pypdf")

        from pypdf import PdfReader

        reader = PdfReader(pdf_path)
        text_content = []

        for i, page in enumerate(reader.pages):
            try:
                text = page.extract_text()
                if text:
                    text_content.append(f"--- 第 {i + 1} 页 ---\n")
                    text_content.append(text)
                    text_content.append("\n")
            except Exception as e:
                text_content.append(f"--- 第 {i + 1} 页提取失败: {e} ---\n")

        full_text = "\n".join(text_content)

        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(full_text)

        return full_text

    def encrypt_pdf(self, pdf_path: str, output_path: str, password: str) -> str:
        """加密 PDF

        Args:
            pdf_path: PDF 文件路径
            output_path: 输出文件路径
            password: 密码

        Returns:
            输出文件路径
        """
        if not self._pypdf_available:
            raise ImportError("请先安装: pip install pypdf")

        from pypdf import PdfReader, PdfWriter

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(password)
        writer.write(output_path)
        writer.close()

        return output_path

    def decrypt_pdf(self, pdf_path: str, output_path: str, password: str) -> str:
        """解密 PDF

        Args:
            pdf_path: PDF 文件路径
            output_path: 输出文件路径
            password: 密码

        Returns:
            输出文件路径
        """
        if not self._pypdf_available:
            raise ImportError("请先安装: pip install pypdf")

        from pypdf import PdfReader, PdfWriter

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        reader = PdfReader(pdf_path)
        if reader.is_encrypted:
            reader.decrypt(password)

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        writer.write(output_path)
        writer.close()

        return output_path

    def get_info(self, pdf_path: str) -> dict:
        """获取 PDF 信息

        Args:
            pdf_path: PDF 文件路径

        Returns:
            PDF 信息字典
        """
        if not self._pypdf_available:
            raise ImportError("请先安装: pip install pypdf")

        from pypdf import PdfReader

        reader = PdfReader(pdf_path)

        info = {
            "pages": len(reader.pages),
            "encrypted": reader.is_encrypted,
        }

        metadata = reader.metadata
        if metadata:
            info["title"] = getattr(metadata, "title", None)
            info["author"] = getattr(metadata, "author", None)
            info["subject"] = getattr(metadata, "subject", None)
            info["creator"] = getattr(metadata, "creator", None)
            info["producer"] = getattr(metadata, "producer", None)
            info["created"] = getattr(metadata, "creation_date", None)
            info["modified"] = getattr(metadata, "modification_date", None)

        return info

    def reorder_pages(self, pdf_path: str, output_path: str, new_order: List[int]) -> str:
        """重新排列 PDF 页面

        Args:
            pdf_path: PDF 文件路径
            output_path: 输出文件路径
            new_order: 新的页面顺序（从0开始）

        Returns:
            输出文件路径
        """
        if not self._pypdf_available:
            raise ImportError("请先安装: pip install pypdf")

        from pypdf import PdfReader, PdfWriter

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        for page_idx in new_order:
            if 0 <= page_idx < len(reader.pages):
                writer.add_page(reader.pages[page_idx])

        writer.write(output_path)
        writer.close()

        return output_path

    def remove_pages(self, pdf_path: str, output_path: str, pages_to_remove: List[int]) -> str:
        """删除指定页面

        Args:
            pdf_path: PDF 文件路径
            output_path: 输出文件路径
            pages_to_remove: 要删除的页面列表（从0开始）

        Returns:
            输出文件路径
        """
        if not self._pypdf_available:
            raise ImportError("请先安装: pip install pypdf")

        from pypdf import PdfReader, PdfWriter

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            if i not in pages_to_remove:
                writer.add_page(page)

        writer.write(output_path)
        writer.close()

        return output_path

    def is_available(self) -> bool:
        """检查是否可用"""
        return self._pypdf_available


__all__ = ["PDFTool"]
