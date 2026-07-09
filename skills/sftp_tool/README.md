# SFTP Tool Skill

SFTP/SSH 远程文件管理工具，功能丰富易用。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

```python
from skills.sftp_tool import SFTPClient

# 密码认证
with SFTPClient('example.com', 22, 'user', password='pass') as sftp:

    # 上传文件
    sftp.upload_file('local.txt', 'remote.txt')

    # 下载文件
    sftp.download_file('remote.txt', 'local.txt')

    # 列出目录
    files = sftp.list_dir('/path')
```

## 使用示例

### 密码认证连接

```python
sftp = SFTPClient('example.com', 22, 'username', password='password')
sftp.connect()
# ... 操作 ...
sftp.disconnect()
```

### 密钥认证连接

```python
sftp = SFTPClient('example.com', 22, 'username',
                  private_key_path='/path/to/key.pem',
                  private_key_passphrase='optional_password')
sftp.connect()
```

### 使用上下文管理器（推荐）

```python
with SFTPClient('example.com', 22, 'user', password='pass') as sftp:
    # 自动连接和断开
    files = sftp.list_dir('/path')
```

### 上传文件

```python
# 上传单个文件
sftp.upload_file('local.txt', '/remote/path/local.txt')

# 上传整个目录
success, failed = sftp.upload_dir(
    '/local/dir',
    '/remote/dir',
    recursive=True
)

# 使用过滤函数
def filter_func(local_path, filename):
    # 只上传 .py 文件
    return filename.endswith('.py')

sftp.upload_dir('/local/dir', '/remote/dir', filter_func=filter_func)
```

### 下载文件

```python
# 下载单个文件
sftp.download_file('/remote/file.txt', 'local.txt')

# 下载整个目录
success, failed = sftp.download_dir(
    '/remote/dir',
    '/local/dir',
    recursive=True
)
```

### 目录操作

```python
# 创建目录
sftp.mkdir('/new/path')

# 递归创建目录（类似 mkdir -p）
sftp.mkdirs('/path/to/dir')

# 删除目录
sftp.rmdir('/path/to/dir')

# 递归删除
sftp.rmdir('/path/to/dir', recursive=True)
```

### 文件操作

```python
# 列出目录
items = sftp.list_dir('/path')
for item in items:
    print(f"{item['type']} {item['name']} ({item['size']} bytes)")

# 检查是否存在
if sftp.exists('/path/to/file.txt'):
    print('文件存在')

# 获取文件信息
info = sftp.stat('/path/to/file.txt')
print(f"大小: {info['size']}")

# 重命名/移动
sftp.rename('/old/path.txt', '/new/path.txt')

# 删除文件
sftp.delete('/path/to/file.txt')
```

### 文本文件读写

```python
# 读取文本
content = sftp.read_text('/path/to/file.txt')
print(content)

# 写入文本
sftp.write_text('/path/to/file.txt', 'Hello, world!')
```

### 执行 SSH 命令

```python
# 执行命令
code, stdout, stderr = sftp.execute_command('ls -la /path')

print(f"返回码: {code}")
print(f"输出:\n{stdout}")

if stderr:
    print(f"错误:\n{stderr}")
```

### 更多示例

```bash
cd skills/sftp_tool
python example.py
```
