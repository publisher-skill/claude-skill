"""
SFTP Tool Skill
SFTP/SSH 远程文件管理工具
"""

import os
import stat
import paramiko
import time
import socket
from pathlib import Path
from typing import List, Dict, Optional, Callable, Any, Tuple


class SFTPClient:
    """SFTP 客户端"""

    def __init__(self,
                 host: str,
                 port: int = 22,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 private_key_path: Optional[str] = None,
                 private_key_passphrase: Optional[str] = None,
                 timeout: int = 30):
        """初始化 SFTP 客户端

        Args:
            host: 主机名或IP地址
            port: 端口号
            username: 用户名
            password: 密码（密码认证）
            private_key_path: 私钥文件路径（密钥认证）
            private_key_passphrase: 私钥密码
            timeout: 超时时间（秒）
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.private_key_path = private_key_path
        self.private_key_passphrase = private_key_passphrase
        self.timeout = timeout

        self.ssh_client: Optional[paramiko.SSHClient] = None
        self.sftp: Optional[paramiko.SFTPClient] = None
        self.connected = False

    def connect(self, auto_add_host_key: bool = True) -> bool:
        """连接到 SFTP 服务器

        Args:
            auto_add_host_key: 是否自动添加主机密钥

        Returns:
            是否连接成功
        """
        try:
            self.ssh_client = paramiko.SSHClient()

            if auto_add_host_key:
                self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if self.private_key_path:
                private_key = paramiko.RSAKey.from_private_key_file(
                    self.private_key_path,
                    password=self.private_key_passphrase
                )
                self.ssh_client.connect(
                    hostname=self.host,
                    port=self.port,
                    username=self.username,
                    pkey=private_key,
                    timeout=self.timeout,
                    banner_timeout=30
                )
            else:
                self.ssh_client.connect(
                    hostname=self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    timeout=self.timeout,
                    banner_timeout=30
                )

            self.sftp = self.ssh_client.open_sftp()
            self.connected = True
            return True

        except Exception as e:
            print(f"连接失败: {e}")
            self.connected = False
            return False

    def disconnect(self):
        """断开连接"""
        if self.sftp:
            try:
                self.sftp.close()
            except:
                pass

        if self.ssh_client:
            try:
                self.ssh_client.close()
            except:
                pass

        self.connected = False

    def __enter__(self):
        """上下文管理器 - 进入"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器 - 退出"""
        self.disconnect()

    def _ensure_connected(self):
        """确保已连接"""
        if not self.connected or not self.sftp:
            raise RuntimeError("SFTP 未连接，请先调用 connect()")

    def list_dir(self, remote_path: str = '.', detailed: bool = True) -> List[Dict]:
        """列出目录内容

        Args:
            remote_path: 远程路径
            detailed: 是否返回详细信息

        Returns:
            文件信息列表
        """
        self._ensure_connected()

        items = []

        try:
            attrs_list = self.sftp.listdir_attr(remote_path)

            for attr in attrs_list:
                item = {
                    'name': attr.filename,
                    'size': attr.st_size,
                    'modified': attr.st_mtime,
                    'is_dir': stat.S_ISDIR(attr.st_mode),
                    'is_file': stat.S_ISREG(attr.st_mode),
                    'is_symlink': stat.S_ISLNK(attr.st_mode),
                    'mode': attr.st_mode,
                }

                if item['is_dir']:
                    item['type'] = 'dir'
                elif item['is_file']:
                    item['type'] = 'file'
                elif item['is_symlink']:
                    item['type'] = 'symlink'
                else:
                    item['type'] = 'other'

                items.append(item)

            # 按类型和名称排序
            items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))

        except Exception as e:
            print(f"列出目录失败 {remote_path}: {e}")

        return items

    def exists(self, remote_path: str) -> bool:
        """检查路径是否存在

        Args:
            remote_path: 远程路径

        Returns:
            是否存在
        """
        self._ensure_connected()

        try:
            self.sftp.stat(remote_path)
            return True
        except FileNotFoundError:
            return False
        except Exception:
            return False

    def is_file(self, remote_path: str) -> bool:
        """检查是否是文件

        Args:
            remote_path: 远程路径

        Returns:
            是否是文件
        """
        self._ensure_connected()

        try:
            stat_obj = self.sftp.stat(remote_path)
            return stat.S_ISREG(stat_obj.st_mode)
        except Exception:
            return False

    def is_dir(self, remote_path: str) -> bool:
        """检查是否是目录

        Args:
            remote_path: 远程路径

        Returns:
            是否是目录
        """
        self._ensure_connected()

        try:
            stat_obj = self.sftp.stat(remote_path)
            return stat.S_ISDIR(stat_obj.st_mode)
        except Exception:
            return False

    def mkdir(self, remote_path: str, exist_ok: bool = False) -> bool:
        """创建目录

        Args:
            remote_path: 远程路径
            exist_ok: 已存在时是否不报错

        Returns:
            是否成功
        """
        self._ensure_connected()

        try:
            if exist_ok and self.exists(remote_path):
                return True
            self.sftp.mkdir(remote_path)
            return True
        except Exception as e:
            if exist_ok and isinstance(e, (FileExistsError, PermissionError)):
                return True
            print(f"创建目录失败 {remote_path}: {e}")
            return False

    def mkdirs(self, remote_path: str, exist_ok: bool = True) -> bool:
        """递归创建目录（类似 mkdir -p）

        Args:
            remote_path: 远程路径
            exist_ok: 已存在时是否不报错

        Returns:
            是否成功
        """
        self._ensure_connected()

        if not remote_path or remote_path == '/':
            return True

        parts = Path(remote_path).parts

        current_path = ''
        for i, part in enumerate(parts):
            if i == 0 and part == '/':
                current_path = '/'
                continue

            current_path = os.path.join(current_path, part) if current_path else part

            if not self.exists(current_path):
                if not self.mkdir(current_path):
                    return False

        return True

    def rmdir(self, remote_path: str, recursive: bool = False) -> bool:
        """删除目录

        Args:
            remote_path: 远程路径
            recursive: 是否递归删除子目录

        Returns:
            是否成功
        """
        self._ensure_connected()

        try:
            if recursive:
                items = self.list_dir(remote_path)

                for item in items:
                    item_path = os.path.join(remote_path, item['name'])

                    if item['is_dir']:
                        self.rmdir(item_path, recursive=True)
                    else:
                        self.delete(item_path)

            self.sftp.rmdir(remote_path)
            return True

        except Exception as e:
            print(f"删除目录失败 {remote_path}: {e}")
            return False

    def delete(self, remote_path: str) -> bool:
        """删除文件

        Args:
            remote_path: 远程路径

        Returns:
            是否成功
        """
        self._ensure_connected()

        try:
            self.sftp.remove(remote_path)
            return True
        except Exception as e:
            print(f"删除文件失败 {remote_path}: {e}")
            return False

    def rename(self, old_path: str, new_path: str) -> bool:
        """重命名或移动文件

        Args:
            old_path: 原路径
            new_path: 新路径

        Returns:
            是否成功
        """
        self._ensure_connected()

        try:
            # 确保目标目录存在
            new_dir = os.path.dirname(new_path)
            if new_dir and not self.exists(new_dir):
                self.mkdirs(new_dir)

            self.sftp.rename(old_path, new_path)
            return True
        except Exception as e:
            print(f"重命名失败 {old_path} -> {new_path}: {e}")
            return False

    def stat(self, remote_path: str) -> Optional[Dict]:
        """获取文件信息

        Args:
            remote_path: 远程路径

        Returns:
            文件信息
        """
        self._ensure_connected()

        try:
            attr = self.sftp.stat(remote_path)

            return {
                'size': attr.st_size,
                'modified': attr.st_mtime,
                'accessed': attr.st_atime,
                'mode': attr.st_mode,
                'is_dir': stat.S_ISDIR(attr.st_mode),
                'is_file': stat.S_ISREG(attr.st_mode),
            }
        except Exception as e:
            print(f"获取文件信息失败 {remote_path}: {e}")
            return None

    def upload_file(self, local_path: str, remote_path: str,
                    make_dirs: bool = True, callback: Optional[Callable] = None) -> bool:
        """上传单个文件

        Args:
            local_path: 本地路径
            remote_path: 远程路径
            make_dirs: 是否自动创建目录
            callback: 进度回调函数

        Returns:
            是否成功
        """
        self._ensure_connected()

        if not os.path.exists(local_path):
            print(f"本地文件不存在: {local_path}")
            return False

        try:
            if make_dirs:
                remote_dir = os.path.dirname(remote_path)
                if remote_dir and not self.exists(remote_dir):
                    self.mkdirs(remote_dir)

            self.sftp.put(local_path, remote_path, callback=callback)
            return True

        except Exception as e:
            print(f"上传失败 {local_path} -> {remote_path}: {e}")
            return False

    def download_file(self, remote_path: str, local_path: str,
                      make_dirs: bool = True, callback: Optional[Callable] = None) -> bool:
        """下载单个文件

        Args:
            remote_path: 远程路径
            local_path: 本地路径
            make_dirs: 是否自动创建目录
            callback: 进度回调函数

        Returns:
            是否成功
        """
        self._ensure_connected()

        try:
            if make_dirs:
                local_dir = os.path.dirname(local_path)
                if local_dir and not os.path.exists(local_dir):
                    os.makedirs(local_dir, exist_ok=True)

            self.sftp.get(remote_path, local_path, callback=callback)
            return True

        except Exception as e:
            print(f"下载失败 {remote_path} -> {local_path}: {e}")
            return False

    def upload_dir(self, local_dir: str, remote_dir: str,
                   recursive: bool = True, filter_func: Optional[Callable] = None) -> Tuple[int, int]:
        """上传整个目录

        Args:
            local_dir: 本地目录
            remote_dir: 远程目录
            recursive: 是否递归子目录
            filter_func: 过滤函数（返回 True 表示上传）

        Returns:
            (成功数, 失败数)
        """
        self._ensure_connected()

        if not os.path.isdir(local_dir):
            print(f"本地目录不存在: {local_dir}")
            return 0, 1

        success = 0
        failed = 0

        self.mkdirs(remote_dir)

        for item in os.listdir(local_dir):
            local_item = os.path.join(local_dir, item)
            remote_item = os.path.join(remote_dir, item)

            if filter_func and not filter_func(local_item, item):
                continue

            if os.path.isfile(local_item):
                if self.upload_file(local_item, remote_item):
                    success += 1
                else:
                    failed += 1

            elif os.path.isdir(local_item) and recursive:
                sub_success, sub_failed = self.upload_dir(local_item, remote_item, recursive=True)
                success += sub_success
                failed += sub_failed

        return success, failed

    def download_dir(self, remote_dir: str, local_dir: str,
                     recursive: bool = True, filter_func: Optional[Callable] = None) -> Tuple[int, int]:
        """下载整个目录

        Args:
            remote_dir: 远程目录
            local_dir: 本地目录
            recursive: 是否递归子目录
            filter_func: 过滤函数（返回 True 表示下载）

        Returns:
            (成功数, 失败数)
        """
        self._ensure_connected()

        if not self.exists(remote_dir):
            print(f"远程目录不存在: {remote_dir}")
            return 0, 1

        os.makedirs(local_dir, exist_ok=True)

        success = 0
        failed = 0

        items = self.list_dir(remote_dir)

        for item in items:
            remote_item = os.path.join(remote_dir, item['name'])
            local_item = os.path.join(local_dir, item['name'])

            if filter_func and not filter_func(remote_item, item['name'], item):
                continue

            if item['is_file']:
                if self.download_file(remote_item, local_item):
                    success += 1
                else:
                    failed += 1

            elif item['is_dir'] and recursive:
                sub_success, sub_failed = self.download_dir(remote_item, local_item, recursive=True)
                success += sub_success
                failed += sub_failed

        return success, failed

    def read_text(self, remote_path: str, encoding: str = 'utf-8') -> Optional[str]:
        """读取远程文本文件

        Args:
            remote_path: 远程路径
            encoding: 编码格式

        Returns:
            文件内容
        """
        self._ensure_connected()

        try:
            with self.sftp.open(remote_path, 'r') as f:
                return f.read().decode(encoding)
        except Exception as e:
            print(f"读取文件失败 {remote_path}: {e}")
            return None

    def write_text(self, remote_path: str, content: str,
                   encoding: str = 'utf-8', make_dirs: bool = True) -> bool:
        """写入远程文本文件

        Args:
            remote_path: 远程路径
            content: 内容
            encoding: 编码格式
            make_dirs: 是否自动创建目录

        Returns:
            是否成功
        """
        self._ensure_connected()

        try:
            if make_dirs:
                remote_dir = os.path.dirname(remote_path)
                if remote_dir and not self.exists(remote_dir):
                    self.mkdirs(remote_dir)

            with self.sftp.open(remote_path, 'w') as f:
                f.write(content.encode(encoding))
            return True
        except Exception as e:
            print(f"写入文件失败 {remote_path}: {e}")
            return False

    def execute_command(self, command: str, timeout: int = 60) -> Tuple[int, str, str]:
        """执行 SSH 命令

        Args:
            command: 命令
            timeout: 超时时间

        Returns:
            (返回码, stdout, stderr)
        """
        if not self.ssh_client:
            raise RuntimeError("SSH 未连接")

        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command, timeout=timeout)

            stdout_str = stdout.read().decode('utf-8', errors='replace')
            stderr_str = stderr.read().decode('utf-8', errors='replace')

            return stdout.channel.recv_exit_status(), stdout_str, stderr_str

        except Exception as e:
            print(f"执行命令失败: {e}")
            return -1, '', str(e)

    def get_file_size(self, remote_path: str) -> Optional[int]:
        """获取文件大小

        Args:
            remote_path: 远程路径

        Returns:
            文件大小（字节）
        """
        stat_info = self.stat(remote_path)
        if stat_info:
            return stat_info['size']
        return None


__all__ = ["SFTPClient"]
