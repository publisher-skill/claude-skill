"""
File Organizer Skill 使用示例
"""

import os
import sys
import tempfile
import shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from skills.file_organizer import FileOrganizer


def create_test_files(temp_dir):
    """创建测试文件"""
    test_files = [
        ('photo1.jpg', '图片'),
        ('document.pdf', '文档'),
        ('video.mp4', '视频'),
        ('music.mp3', '音频'),
        ('archive.zip', '压缩包'),
        ('script.py', '代码'),
        ('data.json', '代码'),
        ('readme.txt', '文档'),
        ('image.png', '图片'),
    ]

    for filename, _ in test_files:
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, 'w') as f:
            f.write(f"测试文件: {filename}\n")

    return test_files


def example_organize_by_type():
    """按类型整理示例"""
    print("="*60)
    print("示例1: 按文件类型整理")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\n创建测试目录: {temp_dir}")
        test_files = create_test_files(temp_dir)
        print(f"创建了 {len(test_files)} 个测试文件\n")

        organizer = FileOrganizer()

        # 先预览
        print("--- 预览整理结果 ---")
        stats = organizer.organize_by_type(temp_dir, dry_run=True)
        for type_name, files in stats.items():
            if files:
                print(f"  {type_name}: {files}")

        # 实际整理
        print("\n--- 执行整理 ---")
        stats = organizer.organize_by_type(temp_dir)

        for type_name, files in stats.items():
            if files:
                print(f"  {type_name}: {len(files)} 个文件")

        summary = organizer.get_summary()
        print(f"\n总计移动: {summary['moved']} 个文件")

        # 显示整理后的目录结构
        print("\n--- 整理后的目录 ---")
        for item in os.listdir(temp_dir):
            item_path = os.path.join(temp_dir, item)
            if os.path.isdir(item_path):
                files = os.listdir(item_path)
                print(f"  {item}/ ({len(files)} files)")


def example_organize_by_date():
    """按日期整理示例"""
    print("\n" + "="*60)
    print("示例2: 按日期整理")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\n创建测试目录: {temp_dir}")
        test_files = create_test_files(temp_dir)

        organizer = FileOrganizer()

        stats = organizer.organize_by_date(temp_dir, dry_run=True)

        for date_folder, files in stats.items():
            if files:
                print(f"  {date_folder}: {len(files)} 个文件")


def example_organize_by_extension():
    """按扩展名整理示例"""
    print("\n" + "="*60)
    print("示例3: 按扩展名整理")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\n创建测试目录: {temp_dir}")
        test_files = create_test_files(temp_dir)

        organizer = FileOrganizer()

        stats = organizer.organize_by_extension(temp_dir, dry_run=True)

        for ext, files in stats.items():
            if files:
                print(f"  .{ext}: {len(files)} 个文件")


if __name__ == "__main__":
    example_organize_by_type()
    example_organize_by_date()
    example_organize_by_extension()

    print("\n" + "="*60)
    print("提示: 在实际使用时，去掉 dry_run=True 参数来执行实际整理")
    print("="*60)
