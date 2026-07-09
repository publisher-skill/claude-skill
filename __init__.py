# Claude Skills Package
# 从根目录或从 skills 导入

__version__ = "1.0.0"

from skills.web_crawler import WebCrawler
from skills.pdf_word_converter import PdfWordConverter

__all__ = ["WebCrawler", "PdfWordConverter"]
