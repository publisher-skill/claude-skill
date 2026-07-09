#!/usr/bin/env python
"""
PDF-Word Converter 命令行工具
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from  pdf_word_converter import PdfWordConverter


def main():
    parser = argparse.ArgumentParser(
        description="PDF与Word相互转换工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s pdf2word input.pdf output.docx
  %(prog)s word2pdf input.docx output.pdf
  %(prog)s folder ./input_dir ./output_dir --mode pdf2word
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # PDF转Word命令
    pdf2word_parser = subparsers.add_parser("pdf2word", help="PDF转Word")
    pdf2word_parser.add_argument("pdf_path", help="输入PDF文件")
    pdf2word_parser.add_argument("docx_path", nargs="?", help="输出Word文件（可选）")
    pdf2word_parser.add_argument("--start", type=int, default=0, help="起始页码（从0开始）")
    pdf2word_parser.add_argument("--end", type=int, default=None, help="结束页码")

    # Word转PDF命令
    word2pdf_parser = subparsers.add_parser("word2pdf", help="Word转PDF")
    word2pdf_parser.add_argument("docx_path", help="输入Word文件")
    word2pdf_parser.add_argument("pdf_path", nargs="?", help="输出PDF文件（可选）")

    # 批量转换命令
    folder_parser = subparsers.add_parser("folder", help="批量转换文件夹")
    folder_parser.add_argument("input_dir", help="输入文件夹")
    folder_parser.add_argument("output_dir", nargs="?", help="输出文件夹（可选）")
    folder_parser.add_argument("--mode", choices=["pdf2word", "word2pdf"],
                              default="pdf2word", help="转换模式（默认: pdf2word）")

    # 检查命令
    check_parser = subparsers.add_parser("check", help="检查依赖是否可用")

    args = parser.parse_args()

    converter = PdfWordConverter()

    if args.command == "check":
        print("检查依赖:")
        print(f"  PDF转Word: {'可用' if converter.is_pdf_to_word_available() else '不可用'}")
        print(f"  Word转PDF: {'可用' if converter.is_word_to_pdf_available() else '不可用'}")
        if not converter.is_pdf_to_word_available():
            print("  提示: pip install pdf2docx")
        if not converter.is_word_to_pdf_available():
            print("  提示: pip install docx2pdf")
        return

    if args.command == "pdf2word":
        try:
            result = converter.pdf_to_word(
                args.pdf_path,
                args.docx_path,
                start=args.start,
                end=args.end
            )
            print(f"转换成功: {result}")
        except Exception as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "word2pdf":
        try:
            result = converter.word_to_pdf(args.docx_path, args.pdf_path)
            print(f"转换成功: {result}")
        except Exception as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "folder":
        try:
            results = converter.convert_folder(
                args.input_dir,
                args.output_dir,
                mode=args.mode
            )
            print(f"转换完成，成功 {len(results)} 个文件")
            for f in results:
                print(f"  - {f}")
        except Exception as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
