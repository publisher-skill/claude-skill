"""
PDF-Word Converter Skill
PDF与Word文档相互转换工具
"""

import os
import sys
from pathlib import Path
from typing import Optional, List, Callable
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PdfWordConverter:
    """PDF与Word转换器"""

    def __init__(self):
        """初始化转换器"""
        self._pdf2docx_available = False
        self._docx2pdf_available = False
        self._check_dependencies()

    def _check_dependencies(self):
        """检查依赖库"""
        try:
            import pdf2docx
            self._pdf2docx_available = True
            logger.debug("pdf2docx 库可用")
        except ImportError:
            logger.warning("pdf2docx 库未安装，PDF转Word功能不可用")

        try:
            import docx2pdf
            self._docx2pdf_available = True
            logger.debug("docx2pdf 库可用")
        except ImportError:
            logger.warning("docx2pdf 库未安装，Word转PDF功能不可用")

    def pdf_to_word(
        self,
        pdf_path: str,
        docx_path: Optional[str] = None,
        start: int = 0,
        end: Optional[int] = None
    ) -> str:
        """
        将PDF转换为Word文档

        Args:
            pdf_path: 输入PDF文件路径
            docx_path: 输出Word文件路径（可选，默认同目录同名）
            start: 起始页码（从0开始）
            end: 结束页码

        Returns:
            输出文件路径

        Raises:
            ImportError: 依赖库未安装
            FileNotFoundError: 输入文件不存在
            Exception: 转换失败
        """
        if not self._pdf2docx_available:
            raise ImportError("请先安装: pip install pdf2docx")

        pdf_path = os.path.abspath(pdf_path)
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")

        # 如果未指定输出路径，自动生成
        if docx_path is None:
            docx_path = os.path.splitext(pdf_path)[0] + ".docx"

        docx_path = os.path.abspath(docx_path)

        logger.info(f"正在转换: {pdf_path} -> {docx_path}")

        from pdf2docx import Converter
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=start, end=end)
        cv.close()

        logger.info(f"转换完成: {docx_path}")
        return docx_path

    def word_to_pdf(
        self,
        docx_path: str,
        pdf_path: Optional[str] = None
    ) -> str:
        """
        将Word文档转换为PDF

        Args:
            docx_path: 输入Word文件路径
            pdf_path: 输出PDF文件路径（可选，默认同目录同名）

        Returns:
            输出文件路径

        Raises:
            ImportError: 依赖库未安装
            FileNotFoundError: 输入文件不存在
            Exception: 转换失败
        """
        if not self._docx2pdf_available:
            raise ImportError("请先安装: pip install docx2pdf")

        docx_path = os.path.abspath(docx_path)
        if not os.path.exists(docx_path):
            raise FileNotFoundError(f"Word文件不存在: {docx_path}")

        # 如果未指定输出路径，自动生成
        if pdf_path is None:
            pdf_path = os.path.splitext(docx_path)[0] + ".pdf"

        pdf_path = os.path.abspath(pdf_path)

        logger.info(f"正在转换: {docx_path} -> {pdf_path}")

        from docx2pdf import convert
        convert(docx_path, pdf_path)

        logger.info(f"转换完成: {pdf_path}")
        return pdf_path

    def convert_folder(
        self,
        input_dir: str,
        output_dir: Optional[str] = None,
        mode: str = "pdf2word"
    ) -> List[str]:
        """
        批量转换文件夹中的文档

        Args:
            input_dir: 输入文件夹路径
            output_dir: 输出文件夹路径（可选，默认同目录）
            mode: 转换模式，'pdf2word' 或 'word2pdf'

        Returns:
            转换成功的文件路径列表
        """
        input_dir = os.path.abspath(input_dir)
        if not os.path.isdir(input_dir):
            raise FileNotFoundError(f"文件夹不存在: {input_dir}")

        if output_dir is None:
            output_dir = input_dir
        else:
            output_dir = os.path.abspath(output_dir)
            os.makedirs(output_dir, exist_ok=True)

        if mode not in ["pdf2word", "word2pdf"]:
            raise ValueError("mode 必须是 'pdf2word' 或 'word2pdf'")

        # 根据模式确定文件扩展名
        if mode == "pdf2word":
            input_ext = ".pdf"
            output_ext = ".docx"
            convert_func = self.pdf_to_word
        else:
            input_ext = (".docx", ".doc")
            output_ext = ".pdf"
            convert_func = self.word_to_pdf

        results = []
        files = os.listdir(input_dir)

        logger.info(f"开始批量转换，模式: {mode}，文件夹: {input_dir}")

        for filename in files:
            filepath = os.path.join(input_dir, filename)

            if os.path.isfile(filepath) and filename.lower().endswith(input_ext):
                try:
                    # 生成输出文件名
                    name, _ = os.path.splitext(filename)
                    output_filename = name + output_ext
                    output_path = os.path.join(output_dir, output_filename)

                    # 执行转换
                    result = convert_func(filepath, output_path)
                    results.append(result)
                except Exception as e:
                    logger.error(f"转换失败 {filename}: {e}")

        logger.info(f"批量转换完成，成功 {len(results)} 个文件")
        return results

    def is_pdf_to_word_available(self) -> bool:
        """检查PDF转Word功能是否可用"""
        return self._pdf2docx_available

    def is_word_to_pdf_available(self) -> bool:
        """检查Word转PDF功能是否可用"""
        return self._docx2pdf_available


__all__ = ["PdfWordConverter"]
