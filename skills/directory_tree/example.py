"""
Directory Tree Skill 使用示例
"""

import os
import sys
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from skills.directory_tree import DirectoryTree


def create_test_structure(root_dir):
    """创建测试目录结构"""
    os.makedirs(os.path.join(root_dir, 'src'))
    os.makedirs(os.path.join(root_dir, 'docs'))
    os.makedirs(os.path.join(root_dir, 'tests'))
    os.makedirs(os.path.join(root_dir, 'src/utils'))
    os.makedirs(os.path.join(root_dir, 'src/components'))

    files = [
        'README.md',
        'requirements.txt',
        'src/main.py',
        'src/__init__.py',
        'src/utils/helpers.py',
        'src/utils/__init__.py',
        'src/components/button.py',
        'tests/test_main.py',
        'docs/getting-started.md',
    ]

    for filepath in files:
        full_path = os.path.join(root_dir, filepath)
        with open(full_path, 'w') as f:
            f.write(f"测试文件: {filepath}\n")


def example_basic_tree():
    """基础目录树示例"""
    print("="*60)
    print("示例1: 基础目录树")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\n创建测试目录: {temp_dir}")
        create_test_structure(temp_dir)

        tree = DirectoryTree()

        print("\n--- 目录树 ---")
        tree_str = tree.generate(temp_dir)
        print(tree_str)


def example_with_size():
    """带文件大小的目录树示例"""
    print("\n" + "="*60)
    print("示例2: 带文件大小的目录树")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\n创建测试目录: {temp_dir}")
        create_test_structure(temp_dir)

        tree = DirectoryTree()

        print("\n--- 目录树（带大小） ---")
        tree_str = tree.generate_with_sizes(temp_dir)
        print(tree_str)


def example_depth_limit():
    """限制深度示例"""
    print("\n" + "="*60)
    print("示例3: 限制显示深度")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\n创建测试目录: {temp_dir}")
        create_test_structure(temp_dir)

        tree = DirectoryTree()

        print("\n--- 目录树（深度=2） ---")
        tree_str = tree.generate(temp_dir, max_depth=2)
        print(tree_str)


def example_markdown():
    """Markdown 格式示例"""
    print("\n" + "="*60)
    print("示例4: Markdown 格式")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\n创建测试目录: {temp_dir}")
        create_test_structure(temp_dir)

        tree = DirectoryTree()

        print("\n--- Markdown 格式 ---")
        md_str = tree.generate_markdown(temp_dir)
        print(md_str)


def example_save_to_file():
    """保存到文件示例"""
    print("\n" + "="*60)
    print("示例5: 保存到文件")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\n创建测试目录: {temp_dir}")
        create_test_structure(temp_dir)

        tree = DirectoryTree()
        tree_str = tree.generate(temp_dir)

        output_file = os.path.join(temp_dir, 'directory_tree.txt')
        tree.save_to_file(tree_str, output_file)

        print(f"\n已保存到: {output_file}")
        print("文件内容预览:")
        print("-" * 60)
        with open(output_file, 'r') as f:
            print(f.read()[:200] + "..." if len(tree_str) > 200 else f.read())


if __name__ == "__main__":
    example_basic_tree()
    example_with_size()
    example_depth_limit()
    example_markdown()
    example_save_to_file()
