"""
Image Downloader Skill
网站图片批量下载工具
"""

import os
import re
import time
import hashlib
import requests
from urllib.parse import urljoin, urlparse, unquote
from pathlib import Path
from typing import List, Dict, Optional, Set, Callable, Any
from bs4 import BeautifulSoup


class ImageDownloader:
    """图片下载器"""

    # 常见图片扩展名
    IMAGE_EXTENSIONS = {
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp',
        '.svg', '.ico', '.tiff', '.tif', '.raw'
    }

    def __init__(self,
                 headers: Optional[Dict[str, str]] = None,
                 timeout: int = 30,
                 delay: float = 0.5,
                 max_retries: int = 3):
        """初始化

        Args:
            headers: 自定义请求头
            timeout: 请求超时时间（秒）
            delay: 下载间隔（秒，避免请求过快）
            max_retries: 重试次数
        """
        self.timeout = timeout
        self.delay = delay
        self.max_retries = max_retries
        self.downloaded = []
        self.failed = []
        self.skipped = []

        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def is_image_url(self, url: str) -> bool:
        """检查URL是否是图片

        Args:
            url: URL地址

        Returns:
            是否是图片URL
        """
        parsed = urlparse(url)
        path = parsed.path.lower()
        return any(ext in path for ext in self.IMAGE_EXTENSIONS)

    def extract_image_urls(self,
                          html: str,
                          base_url: str,
                          include_bg_images: bool = True,
                          deduplicate: bool = True) -> List[str]:
        """从HTML中提取图片URL

        Args:
            html: HTML内容
            base_url: 基础URL，用于补全相对路径
            include_bg_images: 是否包含背景图片
            deduplicate: 是否去重

        Returns:
            图片URL列表
        """
        image_urls = []
        soup = BeautifulSoup(html, 'html.parser')

        # 提取 <img> 标签
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src') or img.get('data-original') or img.get('data-srcset')
            if src:
                if src.startswith('data:'):
                    continue
                src = src.split('?')[0]
                src = src.split(' ')[0]
                full_url = urljoin(base_url, src)
                if self.is_image_url(full_url):
                    image_urls.append(full_url)

        # 提取 background-image
        if include_bg_images:
            for element in soup.find_all(style=True):
                style = element.get('style', '')
                bg_matches = re.findall(r'background-image\s*:\s*url\([\'"]?(.*?)[\'"]?\)', style)
                for match in bg_matches:
                    match = match.strip()
                    if match and not match.startswith('data:'):
                        match = match.split('?')[0]
                        full_url = urljoin(base_url, match)
                        if self.is_image_url(full_url):
                            image_urls.append(full_url)

        # 提取 <picture> 标签
        for picture in soup.find_all('picture'):
            for source in picture.find_all('source'):
                srcset = source.get('srcset', '')
                for src in srcset.split(','):
                    src = src.split(' ')[0].strip()
                    if src and not src.startswith('data:'):
                        full_url = urljoin(base_url, src)
                        if self.is_image_url(full_url):
                            image_urls.append(full_url)

        # 去重
        if deduplicate:
            seen = set()
            unique_urls = []
            for url in image_urls:
                if url not in seen:
                    seen.add(url)
                    unique_urls.append(url)
            image_urls = unique_urls

        return image_urls

    def get_image_filename(self, url: str, default: str = 'image.jpg') -> str:
        """从URL获取文件名

        Args:
            url: 图片URL
            default: 默认文件名

        Returns:
            文件名
        """
        parsed = urlparse(url)
        path = unquote(parsed.path)
        filename = os.path.basename(path)

        if not filename or '.' not in filename:
            ext = '.jpg'
            for img_ext in self.IMAGE_EXTENSIONS:
                if img_ext in url.lower():
                    ext = img_ext
                    break
            filename = f'{default}{ext}'

        # 清理文件名
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)

        return filename

    def get_file_hash(self, filepath: str) -> str:
        """计算文件哈希值

        Args:
            filepath: 文件路径

        Returns:
            哈希值
        """
        if not os.path.exists(filepath):
            return ''
        hash_obj = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()

    def download_image(self,
                      url: str,
                      output_path: str,
                      skip_if_exists: bool = True,
                      check_duplicate: bool = True) -> Optional[str]:
        """下载单张图片

        Args:
            url: 图片URL
            output_path: 保存路径
            skip_if_exists: 如果文件已存在则跳过
            check_duplicate: 检查是否是重复文件（相同内容）

        Returns:
            保存的文件路径，失败返回 None
        """
        if skip_if_exists and os.path.exists(output_path):
            self.skipped.append(url)
            return output_path

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        temp_path = output_path + '.tmp'

        for retry in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=self.timeout, stream=True)
                response.raise_for_status()

                with open(temp_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=65536):
                        f.write(chunk)

                if check_duplicate:
                    if os.path.exists(output_path):
                        new_hash = self.get_file_hash(temp_path)
                        existing_hash = self.get_file_hash(output_path)
                        if new_hash == existing_hash:
                            os.remove(temp_path)
                            self.skipped.append(url)
                            return output_path

                os.rename(temp_path, output_path)
                self.downloaded.append((url, output_path))
                return output_path

            except Exception as e:
                if retry < self.max_retries - 1:
                    time.sleep(self.delay)
                else:
                    self.failed.append((url, str(e)))
                    return None

        return None

    def download_from_url(self,
                         url: str,
                         output_dir: str,
                         extract_from_html: bool = True,
                         skip_if_exists: bool = True,
                         max_images: Optional[int] = None,
                         filename_pattern: Optional[str] = None) -> List[str]:
        """从URL下载图片

        Args:
            url: 目标URL
            output_dir: 输出目录
            extract_from_html: 是否从HTML中提取图片
            skip_if_exists: 如果文件已存在则跳过
            max_images: 最大下载数量
            filename_pattern: 文件名模式（如 'img_{index:03d}'）

        Returns:
            下载的文件路径列表
        """
        url = url.strip()
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        downloaded_files = []

        if extract_from_html and not self.is_image_url(url):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()

                image_urls = self.extract_image_urls(response.text, url)

                if max_images:
                    image_urls = image_urls[:max_images]

                print(f"找到 {len(image_urls)} 张图片")

                for i, img_url in enumerate(image_urls):
                    if filename_pattern:
                        filename = filename_pattern.format(index=i+1)
                        # 保留扩展名
                        orig_filename = self.get_image_filename(img_url, '')
                        ext = os.path.splitext(orig_filename)[1] or '.jpg'
                        if not filename.endswith(ext):
                            filename += ext
                        output_path = os.path.join(output_dir, filename)
                    else:
                        filename = self.get_image_filename(img_url, f'image_{i+1}')
                        output_path = os.path.join(output_dir, filename)

                    result = self.download_image(img_url, output_path, skip_if_exists)
                    if result:
                        downloaded_files.append(result)

                    if self.delay > 0 and i < len(image_urls) - 1:
                        time.sleep(self.delay)

            except Exception as e:
                print(f"获取页面失败: {e}")

        else:
            filename = self.get_image_filename(url, 'image')
            output_path = os.path.join(output_dir, filename)
            result = self.download_image(url, output_path, skip_if_exists)
            if result:
                downloaded_files.append(result)

        return downloaded_files

    def download_from_list(self,
                           url_list: List[str],
                           output_dir: str,
                           skip_if_exists: bool = True,
                           filename_prefix: str = 'image') -> List[str]:
        """从URL列表下载图片

        Args:
            url_list: URL列表
            output_dir: 输出目录
            skip_if_exists: 如果文件已存在则跳过
            filename_prefix: 文件名前缀

        Returns:
            下载的文件路径列表
        """
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        downloaded_files = []

        for i, url in enumerate(url_list):
            filename = self.get_image_filename(url, f'{filename_prefix}_{i+1}')
            output_path = os.path.join(output_dir, filename)

            result = self.download_image(url, output_path, skip_if_exists)
            if result:
                downloaded_files.append(result)

            if self.delay > 0 and i < len(url_list) - 1:
                time.sleep(self.delay)

        return downloaded_files

    def crawl_and_download(self,
                          start_url: str,
                          output_dir: str,
                          max_pages: int = 10,
                          include_subpages: bool = True,
                          skip_if_exists: bool = True) -> List[str]:
        """爬取并下载整个网站的图片

        Args:
            start_url: 起始URL
            output_dir: 输出目录
            max_pages: 最大页面数
            include_subpages: 是否包含子页面
            skip_if_exists: 如果文件已存在则跳过

        Returns:
            下载的文件路径列表
        """
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        visited = set()
        to_visit = [start_url]
        all_downloaded = []

        page_count = 0

        while to_visit and page_count < max_pages:
            url = to_visit.pop(0)

            if url in visited:
                continue

            visited.add(url)
            page_count += 1

            print(f"处理页面 {page_count}/{max_pages}: {url}")

            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()

                parsed_url = urlparse(url)
                page_name = re.sub(r'[<>:"/\\|?*]', '_', parsed_url.path.strip('/') or 'index')
                page_dir = os.path.join(output_dir, page_name)

                downloaded = self.download_from_url(
                    url, page_dir,
                    extract_from_html=True,
                    skip_if_exists=skip_if_exists
                )
                all_downloaded.extend(downloaded)

                if include_subpages and page_count < max_pages:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for a in soup.find_all('a', href=True):
                        href = a['href']
                        full_url = urljoin(url, href)
                        full_url = full_url.split('#')[0].split('?')[0]

                        full_parsed = urlparse(full_url)
                        if full_parsed.netloc == parsed_url.netloc:
                            if full_url not in visited and full_url not in to_visit:
                                to_visit.append(full_url)

            except Exception as e:
                print(f"处理页面失败 {url}: {e}")

            if self.delay > 0 and to_visit:
                time.sleep(self.delay)

        return all_downloaded

    def get_summary(self) -> Dict[str, Any]:
        """获取下载摘要

        Returns:
            摘要信息
        """
        return {
            'downloaded': len(self.downloaded),
            'failed': len(self.failed),
            'skipped': len(self.skipped),
            'downloaded_list': self.downloaded,
            'failed_list': self.failed,
        }

    def reset(self):
        """重置状态"""
        self.downloaded = []
        self.failed = []
        self.skipped = []

    def extract_weixin_image_urls(self, html: str) -> List[str]:
        """从文章HTML中提取图片URL

        Args:
            html: HTML内容

        Returns:
            图片URL列表
        """
        image_urls = []

        # 1. 提取 data-src 中的 mmbiz 图片（这是文章图片的主要方式）
        data_src_pattern = r'<img[^>]+data-src=["\'](https?://mmbiz\.(?:qpic\.cn|qlogo\.cn)/[^"\']+)["\']'
        data_src_matches = re.findall(data_src_pattern, html)
        for img_url in data_src_matches:
            image_urls.append(img_url)

        # 2. 提取 src 中的 mmbiz 图片
        src_pattern = r'<img[^>]+src=["\'](https?://mmbiz\.(?:qpic\.cn|qlogo\.cn)/[^"\']+)["\']'
        src_matches = re.findall(src_pattern, html)
        for img_url in src_matches:
            if img_url not in image_urls:
                image_urls.append(img_url)

        # 去重
        image_urls = list(dict.fromkeys(image_urls))
        return image_urls

    def download_from_v_article(self,
                                     url: str,
                                     output_dir: str,
                                     skip_if_exists: bool = True,
                                     min_file_size: int = 5000,
                                     filename_pattern: str = 'main_{index:03d}',
                                     verbose: bool = True) -> List[str]:
        """从文章下载图片

        Args:
            url: 文章URL
            output_dir: 输出目录
            skip_if_exists: 如果文件已存在则跳过
            min_file_size: 最小文件大小（字节，小于此值的会被删除）
            filename_pattern: 文件名模式
            verbose: 是否显示详细输出

        Returns:
            成功下载的文件路径列表
        """
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        downloaded_files = []

        if verbose:
            print(f'正在获取页面: {url}')

        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            response.encoding = 'utf-8'
            html = response.text

            # 提取图片URL
            image_urls = self.extract_weixin_image_urls(html)

            if verbose:
                print(f'\n找到 {len(image_urls)} 张图片\n')

            success_count = 0
            fail_count = 0

            for i, img_url in enumerate(image_urls):
                try:
                    # 确定文件格式
                    fmt = 'jpg'
                    if 'wx_fmt=png' in img_url:
                        fmt = 'png'
                    elif 'wx_fmt=gif' in img_url:
                        fmt = 'gif'
                    elif 'wx_fmt=webp' in img_url:
                        fmt = 'webp'

                    filename = filename_pattern.format(index=i+1)
                    filename = f'{filename}.{fmt}'
                    output_path = os.path.join(output_dir, filename)

                    if skip_if_exists and os.path.exists(output_path):
                        if verbose:
                            print(f'[{i+1}/{len(image_urls)}] 跳过 (已存在): {filename}')
                        downloaded_files.append(output_path)
                        continue

                    if verbose:
                        print(f'[{i+1}/{len(image_urls)}] 下载: {img_url[:100]}...')

                    # 下载图片
                    img_response = self.session.get(img_url, timeout=self.timeout)

                    if img_response.status_code == 200:
                        temp_path = output_path + '.tmp'
                        with open(temp_path, 'wb') as f:
                            f.write(img_response.content)

                        file_size = os.path.getsize(temp_path)
                        if file_size < min_file_size:  # 小于阈值的可能不是主图
                            os.remove(temp_path)
                            if verbose:
                                print(f'  跳过 (太小: {file_size} bytes)')
                        else:
                            os.rename(temp_path, output_path)
                            if verbose:
                                print(f'  成功保存: {filename} ({file_size} bytes)')
                            downloaded_files.append(output_path)
                            self.downloaded.append((img_url, output_path))
                    else:
                        if verbose:
                            print(f'  失败 (HTTP {img_response.status_code})')
                        self.failed.append((img_url, f'HTTP {img_response.status_code}'))

                except Exception as e:
                    if verbose:
                        print(f'  错误: {str(e)}')
                    self.failed.append((img_url, str(e)))

                if self.delay > 0 and i < len(image_urls) - 1:
                    time.sleep(self.delay)

            if verbose:
                print(f'\n完成!')
                print(f'成功下载: {len(downloaded_files)} 张')
                print(f'失败: {len(self.failed)} 张')
                print(f'保存位置: {output_dir}')

                # 列出所有下载的图片
                print(f'\n已下载的文件:')
                for f in sorted(os.listdir(output_dir)):
                    if f.startswith(filename_pattern.format(index='')):  # 只显示按模式下载的文件
                        filepath = os.path.join(output_dir, f)
                        size = os.path.getsize(filepath)
                        print(f'  - {f} ({size} bytes)')

        except Exception as e:
            print(f'获取页面失败: {e}')

        return downloaded_files


__all__ = ["ImageDownloader"]
