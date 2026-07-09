"""
Batch Renamer Skill 使用示例
"""

import os
import sys
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from skills.batch_renamer import BatchRenamer


def create_test_files(temp_dir):
    """创建测试文件"""
    test_files = [
        'photo1.jpg', 'photo2.jpg', 'photo3.jpg',
        'vacation_1.jpg', 'vacation_2.jpg',
        'Document1.pdf', 'Document2.pdf',
    ]

    for filename in test_files:
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, 'w') as f:
            f.write(f"测试文件: {filename}\n")

    return test_files


def example_sequence_rename():
    """序号重命名示例"""
    print("="*60)
    print("示例1: 序号重命名")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\n创建测试目录: {temp_dir}")
        test_files = create_test_files(temp_dir)
        print(f"创建了 {len(test_files)} 个测试文件\n")

        renamer = BatchRenamer()

        print("--- 预览序号重命名 ---")
        changes = renamer.rename_with_sequence(temp_dir, prefix='image', start=1, padding=2, dry_run=True)

        for old, new in changes:
            print(f"  {old:20} -> {new}")

        summary = renamer.get_summary()
        print(f"\n将重命名: {summary['renamed']} 个文件")


def example_add_prefix():
    """添加前缀示例"""
    print("\n" + "="*60)
    print("示例2: 添加前缀")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\n创建测试目录: {temp_dir}")
        test_files = create_test_files(temp_dir)

        renamer = BatchRenamer()

        print("--- 预览添加前缀 ---")
        changes = renamer.add_prefix(temp_dir, '2024_', dry_run=True)

        for old, new in changes[:5]:
            print(f"  {old:20} -> {new}")
        if len(changes) > 5:
            print(f"  ... 还有 {len(changes) - 5} 个")


def example_replace_text():
    """替换文本示例"""
    print("\n" + "="*60)
    print("示例3: 替换文本")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\n创建测试目录: {temp_dir}")
        test_files = create_test_files(temp_dir)

        renamer = BatchRenamer()

        print("--- 预览替换文本 ---")
        changes = renamer.replace_text(temp_dir, 'photo', 'image', dry_run=True)

        for old, new in changes:
            print(f"  {old:20} -> {new}")


def example_regex_rename():
    """正则重命名示例"""
    print("\n" + "="*60)
    print("示例4: 正则表达式重命名")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\n创建测试目录: {temp_dir}")
        test_files = create_test_files(temp_dir)

        renamer = BatchRenamer()

        print("--- 预览正则重命名 ---")
        print("  模式: vacation_(\\d+) -> holiday_\\1")
        changes = renamer.rename_with_pattern(
            temp_dir, r'vacation_(\d+)', r'holiday_\1', dry_run=True
        )

        for old, new in changes:
            print(f"  {old:20} -> {new}")


def example_change_case():
    """改变大小写示例"""
    print("\n" + "="*60)
    print("示例5: 改变大小写")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\n创建测试目录: {temp_dir}")
        test_files = create_test_files(temp_dir)

        renamer = BatchRenamer()

        print("--- 预览转小写 ---")
        changes = renamer.change_case(temp_dir, case_type='lower', dry_run=True)

        for old, new in changes[:5]:
            print(f"  {old:20} -> {new}")
        if len(changes) > 5:
            print(f"  ... 还有 {len(changes) - 5} 个")


if __name__ == "__main__":
    example_sequence_rename()
    example_add_prefix()
    example_replace_text()
    example_regex_rename()
    example_change_case()

    print("\n" + "="*60)
    print("提示: 在实际使用时，去掉 dry_run=True 参数来执行实际重命名")
    print("="*60)
