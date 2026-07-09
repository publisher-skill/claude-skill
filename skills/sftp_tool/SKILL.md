---
name: sftp_tool
description: SFTP/SSH 远程文件管理工具 - 上传下载、列表、重命名、删除、执行命令等
metadata:
  type: custom
---

# SFTP Tool Skill

SFTP/SSH 远程文件管理工具，功能丰富易用。

## 功能特性

### 📁 文件管理
- **上传文件/目录**: 支持单个文件或整个目录上传
- **下载文件/目录**: 支持单个文件或整个目录下载
- **列出目录**: 查看远程目录内容
- **创建/删除目录**: 支持递归创建
- **重命名/移动**: 文件和目录重命名
- **删除文件/目录**: 支持递归删除
- **检查存在**: 验证路径是否存在

### 📄 文件操作
- **读取文本**: 直接读取远程文本文件
- **写入文本**: 直接写入远程文本文件
- **获取文件信息**: 文件大小、修改时间等
- **过滤函数**: 自定义上传/下载过滤

### 🔧 SSH 功能
- **执行命令**: 通过 SSH 执行远程命令
- **密码/密钥认证**: 支持两种认证方式
- **超时设置**: 防止连接挂起
- **上下文管理**: 使用 with 语句自动管理连接

### 🛡️ 安全特性
- **主机密钥自动添加**: 首次连接自动添加
- **私钥加密**: 支持带密码的私钥
- **超时保护**: 防止无响应连接

## 使用方法

### Python API

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

    # 创建目录
    sftp.mkdir('/new/path')

    # 删除文件
    sftp.delete('/old/file.txt')

    # 执行命令
    code, stdout, stderr = sftp.execute_command('ls -la')
```

```python
# 密钥认证
with SFTPClient('example.com', 22, 'user',
                private_key_path='/path/key.pem',
                private_key_passphrase='pass') as sftp:

    # 上传目录
    sftp.upload_dir('/local/dir', '/remote/dir')

    # 下载目录
    sftp.download_dir('/remote/dir', '/local/dir')
```

## API 参考

### SFTPClient 类

#### 初始化
```python
SFTPClient(host, port=22, username=None, password=None,
           private_key_path=None, private_key_passphrase=None,
           timeout=30)
```

#### 连接管理
- `connect(auto_add_host_key=True)` - 连接服务器
- `disconnect()` - 断开连接
- 使用 `with` 语句自动管理连接

#### 目录操作
- `list_dir(remote_path='.', detailed=True)` - 列出目录
- `mkdir(remote_path, exist_ok=False)` - 创建目录
- `mkdirs(remote_path, exist_ok=True)` - 递归创建目录
- `rmdir(remote_path, recursive=False)` - 删除目录

#### 文件操作
- `exists(remote_path)` - 检查是否存在
- `is_file(remote_path)` - 是否是文件
- `is_dir(remote_path)` - 是否是目录
- `stat(remote_path)` - 获取文件信息
- `delete(remote_path)` - 删除文件
- `rename(old_path, new_path)` - 重命名/移动
- `read_text(remote_path, encoding='utf-8')` - 读取文本
- `write_text(remote_path, content, encoding='utf-8')` - 写入文本

#### 上传/下载
- `upload_file(local_path, remote_path, make_dirs=True, callback=None)` - 上传文件
- `download_file(remote_path, local_path, make_dirs=True, callback=None)` - 下载文件
- `upload_dir(local_dir, remote_dir, recursive=True, filter_func=None)` - 上传目录
- `download_dir(remote_dir, local_dir, recursive=True, filter_func=None)` - 下载目录

#### SSH 命令
- `execute_command(command, timeout=60)` - 执行远程命令
