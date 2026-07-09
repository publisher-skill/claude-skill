"""
File Comparator Skill 使用示例
"""

import os
import sys
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from skills.file_comparator import FileComparator


def create_test_files():
    """创建测试文件"""
    temp_dir = tempfile.mkdtemp()

    # 创建两个类似的目录
    dir1 = os.path.join(temp_dir, 'dir1')
    dir2 = os.path.join(temp_dir, 'dir2')
    os.makedirs(dir1)
    os.makedirs(dir2)

    # 创建相同的文件
    with open(os.path.join(dir1, 'common.txt'), 'w') as f:
        f.write('这是共同文件\n')
    with open(os.path.join(dir2, 'common.txt'), 'w') as f:
        f.write('这是共同文件\n')

    # 创建不同的文件
    with open(os.path.join(dir1, 'different.txt'), 'w') as f:
        f.write('这是目录1的版本\n')
    with open(os.path.join(dir2, 'different.txt'), 'w') as f:
        f.write('这是目录2的版本\n')

    # 创建只在一边的文件
    with open(os.path.join(dir1, 'only_in_dir1.txt'), 'w') as f:
        f.write('只在目录1\n')
    with open(os.path.join(dir2, 'only_in_dir2.txt'), 'w') as f:
        f.write('只在目录2\n')

    # 创建重复文件测试用
    duplicate_dir = os.path.join(temp_dir, 'duplicates')
    os.makedirs(duplicate_dir)

    for i in range(3):
        filename = os.path.join(duplicate_dir, f'copy{i}.txt')
        with open(filename, 'w') as f:
            f.write('重复的内容\n')

    return temp_dir, dir1, dir2, duplicate_dir


def example_compare_files():
    """对比文件示例"""
    print("="*60)
    print("示例1: 对比两个文件")
    print("="*60)

    temp_dir = tempfile.mkdtemp()

    try:
        # 创建两个相同的文件
        file1 = os.path.join(temp_dir, 'file1.txt')
        file2 = os.path.join(temp_dir, 'file2.txt')

        with open(file1, 'w') as f:
            f.write('Hello, World!\n')
        with open(file2, 'w') as f:
            f.write('Hello, World!\n')

        comp = FileComparator()

        # 快速对比
        result = comp.compare_files(file1, file2, method='quick')
        print(f"\n快速对比 - 是否相同: {'是' if result['identical'] else '否'}")

        # 内容对比
        result = comp.compare_files(file1, file2, method='content')
        print(f"内容对比 - 是否相同: {'是' if result['identical'] else '否'}")

        # Hash 对比
        result = comp.compare_files(file1, file2, method='hash')
        print(f"Hash 对比 - 是否相同: {'是' if result['identical'] else '否'}")
        if 'hash1' in result:
            print(f"  Hash: {result['hash1']}")

        # 修改其中一个文件
        with open(file2, 'w') as f:
            f.write('Hello, Claude!\n')

        result = comp.compare_files(file1, file2, method='content')
        print(f"\n修改后对比 - 是否相同: {'是' if result['identical'] else '否'}")

    finally:
        import shutil
        shutil.rmtree(temp_dir)


def example_compare_directories():
    """对比目录示例"""
    print("\n" + "="*60)
    print("示例2: 对比两个目录")
    print("="*60)

    temp_dir, dir1, dir2, _ = create_test_files()

    try:
        comp = FileComparator()

        result = comp.compare_directories(dir1, dir2, recursive=True)

        report = comp.generate_diff_report(result)
        print("\n--- 对比报告 ---")
        print(report)

    finally:
        import shutil
        shutil.rmtree(temp_dir)


def example_find_duplicates():
    """查找重复文件示例"""
    print("\n" + "="*60)
    print("示例3: 查找重复文件")
    print("="*60)

    temp_dir, _, _, duplicate_dir = create_test_files()

    try:
        comp = FileComparator()

        duplicates = comp.find_duplicates(duplicate_dir, by_hash=True)

        if duplicates:
            print(f"\n找到 {len(duplicates)} 组重复文件:")
            for i, (key, files) in enumerate(duplicates.items(), 1):
                print(f"\n组 {i} (hash: {key[:16]}...):")
                for f in files:
                    print(f"  {os.path.basename(f)}")
        else:
            print("\n没有找到重复文件")

    finally:
        import shutil
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    example_compare_files()
    example_compare_directories()
    example_find_duplicates()
