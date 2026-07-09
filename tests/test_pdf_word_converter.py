"""
PDF-Word Converter 测试
"""

import pytest
import sys
import os
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.pdf_word_converter import PdfWordConverter


class TestPdfWordConverter:
    """测试 PdfWordConverter 类"""

    def test_init(self):
        """测试初始化"""
        converter = PdfWordConverter()
        # 只是检查初始化不会出错
        assert converter is not None

    def test_is_available_methods(self):
        """测试可用性检查方法"""
        converter = PdfWordConverter()
        # 这些方法应该总是可用的
        assert isinstance(converter.is_pdf_to_word_available(), bool)
        assert isinstance(converter.is_word_to_pdf_available(), bool)

    def test_pdf_to_word_file_not_found(self):
        """测试PDF文件不存在的情况"""
        converter = PdfWordConverter()
        if converter.is_pdf_to_word_available():
            with pytest.raises(FileNotFoundError):
                converter.pdf_to_word("nonexistent.pdf")

    def test_word_to_pdf_file_not_found(self):
        """测试Word文件不存在的情况"""
        converter = PdfWordConverter()
        if converter.is_word_to_pdf_available():
            with pytest.raises(FileNotFoundError):
                converter.word_to_pdf("nonexistent.docx")

    def test_convert_folder_invalid_dir(self):
        """测试无效的文件夹"""
        converter = PdfWordConverter()
        with pytest.raises(FileNotFoundError):
            converter.convert_folder("nonexistent_dir")

    def test_convert_folder_invalid_mode(self):
        """测试无效的转换模式"""
        converter = PdfWordConverter()
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValueError):
                converter.convert_folder(tmpdir, mode="invalid_mode")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
