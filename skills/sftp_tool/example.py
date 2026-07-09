"""
SFTP Tool Skill 使用示例
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from skills.sftp_tool import SFTPClient


def example_connect_methods():
    """连接方式示例"""
    print("="*60)
    print("示例1: 连接方式")
    print("="*60)

    print("\n方式1: 密码认证")
    print("""
sftp = SFTPClient('example.com', 22, 'user', password='password')
sftp.connect()
# ... 操作 ...
sftp.disconnect()
    """)

    print("\n方式2: 密钥认证")
    print("""
sftp = SFTPClient('example.com', 22, 'user',
                  private_key_path='/path/to/key.pem',
                  private_key_passphrase='optional_pass')
sftp.connect()
    """)

    print("\n方式3: 使用上下文管理器（推荐）")
    print("""
with SFTPClient('example.com', 22, 'user', password='pass') as sftp:
    # 自动连接和断开
    files = sftp.list_dir('/path')
    """)


def example_file_operations():
    """文件操作示例"""
    print("\n" + "="*60)
    print("示例2: 文件操作")
    print("="*60)

    print("\n功能概览:")
    print("  - upload_file: 上传文件")
    print("  - download_file: 下载文件")
    print("  - upload_dir: 上传目录")
    print("  - download_dir: 下载目录")
    print("  - list_dir: 列出目录")
    print("  - exists: 检查是否存在")
    print("  - is_file / is_dir: 判断类型")
    print("  - mkdir / mkdirs: 创建目录")
    print("  - rmdir: 删除目录")
    print("  - delete: 删除文件")
    print("  - rename: 重命名/移动")
    print("  - stat: 获取文件信息")
    print("  - read_text / write_text: 读写文本")
    print("  - execute_command: 执行 SSH 命令")


def example_read_write():
    """读写示例"""
    print("\n" + "="*60)
    print("示例3: 读写文本文件")
    print("="*60)

    print("\n读取文本文件:")
    print("""
content = sftp.read_text('/path/to/file.txt')
print(content)
    """)

    print("\n写入文本文件:")
    print("""
sftp.write_text('/path/to/file.txt', 'Hello, world!')
    """)


def example_directory_ops():
    """目录操作示例"""
    print("\n" + "="*60)
    print("示例4: 目录操作")
    print("="*60)

    print("\n列出目录:")
    print("""
items = sftp.list_dir('/path')
for item in items:
    print(f"{item['type']} {item['name']} ({item['size']} bytes)")
    """)

    print("\n创建目录:")
    print("""
# 单个目录
sftp.mkdir('/new/path')

# 递归创建（类似 mkdir -p）
sftp.mkdirs('/path/to/deep/dir')
    """)

    print("\n删除目录:")
    print("""
# 单级目录（必须为空）
sftp.rmdir('/path/to/dir')

# 递归删除（包含所有内容）
sftp.rmdir('/path/to/dir', recursive=True)
    """)


def example_commands():
    """命令执行示例"""
    print("\n" + "="*60)
    print("示例5: 执行 SSH 命令")
    print("="*60)

    print("""
code, stdout, stderr = sftp.execute_command('ls -la /path')

print(f"返回码: {code}")
print(f"输出:\n{stdout}")

if stderr:
    print(f"错误:\n{stderr}")
    """)


def example_filter_function():
    """过滤函数示例"""
    print("\n" + "="*60)
    print("示例6: 使用过滤函数")
    print("="*60)

    print("\n只上传 .py 文件:")
    print("""
def filter_func(local_path, filename):
    return filename.endswith('.py')

sftp.upload_dir('/local/dir', '/remote/dir', filter_func=filter_func)
    """)

    print("\n只下载 .txt 文件:")
    print("""
def filter_func(remote_path, filename, file_info):
    return filename.endswith('.txt')

sftp.download_dir('/remote/dir', '/local/dir', filter_func=filter_func)
    """)


def quick_reference():
    """快速参考"""
    print("\n" + "="*60)
    print("快速参考")
    print("="*60)

    print("""
常用功能速查:

1. 连接并列出目录
   with SFTPClient('example.com', 22, 'user', password='pass') as sftp:
       items = sftp.list_dir('/path')
       for item in items:
           print(f"{item['type']} {item['name']}")

2. 上传文件
   sftp.upload_file('local.txt', '/remote/local.txt')

3. 下载文件
   sftp.download_file('/remote/file.txt', 'local.txt')

4. 上传目录
   success, failed = sftp.upload_dir('/local/dir', '/remote/dir')
   print(f"成功: {success}, 失败: {failed}")

5. 下载目录
   success, failed = sftp.download_dir('/remote/dir', '/local/dir')

6. 创建目录
   sftp.mkdir('/new/path')
   sftp.mkdirs('/path/to/deep/dir')  # 递归创建

7. 删除文件
   sftp.delete('/path/to/file.txt')

8. 重命名/移动
   sftp.rename('/old.txt', '/new.txt')

9. 读取/写入文本
   content = sftp.read_text('/file.txt')
   sftp.write_text('/file.txt', 'Hello!')

10. 执行命令
    code, stdout, stderr = sftp.execute_command('ls -la')
    print(stdout)
    """)


if __name__ == "__main__":
    example_connect_methods()
    example_file_operations()
    example_read_write()
    example_directory_ops()
    example_commands()
    example_filter_function()
    quick_reference()
