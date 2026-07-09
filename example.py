#!/usr/bin/env python
"""
Claude Skills - 综合示例
演示所有技能的使用方法
"""

import sys
import os


def demo_web_crawler():
    """演示 Web Crawler"""
    print("\n" + "="*60)
    print("Web Crawler - 网页爬虫示例")
    print("="*60 + "\n")

    try:
        from skills.web_crawler import WebCrawler

        crawler = WebCrawler()

        # 抓取示例网页
        url = "https://example.com"
        print(f"正在抓取: {url}")
        html = crawler.fetch(url)
        print(f"成功抓取 HTML，长度: {len(html)} 字符\n")

        # 提取文本
        text = crawler.extract_text(html)
        print("页面文本摘要:")
        print("-" * 40)
        print(text[:200] + "..." if len(text) > 200 else text)
        print("-" * 40 + "\n")

        # 提取链接
        links = crawler.extract_links(html, base_url=url)
        print(f"找到 {len(links)} 个链接:")
        for i, link in enumerate(links[:5], 1):
            print(f"  {i}. {link}")
        if len(links) > 5:
            print(f"  ... 还有 {len(links) - 5} 个链接\n")

        # 使用 CSS 选择器
        titles = crawler.select(html, "h1")
        print(f"页面标题: {titles}")

        return True

    except ImportError:
        print("警告: Web Crawler 依赖未安装")
        print("请运行: pip install requests beautifulsoup4 lxml")
        return False
    except Exception as e:
        print(f"Web Crawler 演示出错: {e}")
        return False


def demo_pdf_word_converter():
    """演示 PDF-Word Converter"""
    print("\n" + "="*60)
    print("PDF-Word Converter - 文档转换示例")
    print("="*60 + "\n")

    try:
        from skills.pdf_word_converter import PdfWordConverter

        converter = PdfWordConverter()

        # 检查依赖
        print("依赖检查:")
        print(f"  PDF转Word: {'✅ 可用' if converter.is_pdf_to_word_available() else '❌ 不可用'}")
        print(f"  Word转PDF: {'✅ 可用' if converter.is_word_to_pdf_available() else '❌ 不可用'}")
        print()

        # 提示安装依赖
        if not converter.is_pdf_to_word_available():
            print("提示: 安装 PDF转Word 依赖: pip install pdf2docx")
        if not converter.is_word_to_pdf_available():
            print("提示: 安装 Word转PDF 依赖: pip install docx2pdf")
            print("      (还需要 Microsoft Word 或 LibreOffice)")
        print()

        # 尝试创建测试文档
        if converter.is_pdf_to_word_available() or converter.is_word_to_pdf_available():
            print("使用方法:")
            print("  from skills.pdf_word_converter import PdfWordConverter")
            print()
            print("  converter = PdfWordConverter()")
            print("  converter.pdf_to_word('input.pdf', 'output.docx')")
            print("  converter.word_to_pdf('input.docx', 'output.pdf')")
            print("  converter.convert_folder('input_dir', 'output_dir', mode='pdf2word')")
            print()
            print("  命令行使用:")
            print("    python skills/pdf_word_converter/converter.py check")
            print("    python skills/pdf_word_converter/converter.py pdf2word input.pdf")
            print("    python skills/pdf_word_converter/converter.py word2pdf input.docx")

        return True

    except ImportError:
        print("警告: PDF-Word Converter 依赖未安装")
        print("请运行: pip install pdf2docx docx2pdf python-docx")
        return False
    except Exception as e:
        print(f"PDF-Word Converter 演示出错: {e}")
        return False


def main():
    """主函数"""
    print("="*60)
    print("Claude Skills - 技能工具集合")
    print("="*60)

    # 添加当前目录到路径
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    # 演示各个技能
    results = {}
    results["Web Crawler"] = demo_web_crawler()
    results["PDF-Word Converter"] = demo_pdf_word_converter()

    # 总结
    print("\n" + "="*60)
    print("总结")
    print("="*60)
    for name, success in results.items():
        status = "✅ 成功" if success else "❌ 失败"
        print(f"  {name}: {status}")

    print("\n提示:")
    print("- 安装所有依赖: pip install -r requirements.txt")
    print("- 运行单个技能的示例:")
    print("    python skills/web_crawler/example.py")
    print("    python skills/pdf_word_converter/example.py")
    print("- 运行测试: pytest tests/")
    print("\n项目结构:")
    print("- skills/ - Claude Code skills (可独立运行)")
    print("- tests/  - 测试文件")


if __name__ == "__main__":
    main()
