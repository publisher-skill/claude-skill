
import requests
import re
import os
import time
from urllib.parse import urlparse
from typing import List, Dict, Tuple


class WeChatImageDownloader:
    """微信公众号图片下载器"""

    def __init__(self, headers=None, timeout=30, delay=0.5):
        """
        初始化下载器

        Args:
            headers: 自定义请求头
            timeout: 请求超时时间（秒）
            delay: 请求间隔（秒）
        """
        self.timeout = timeout
        self.delay = delay

        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        self.success_count = 0
        self.fail_count = 0
        self.downloaded_files = []

    def extract_image_urls(self, html: str) -> List[str]:
        """
        从HTML中提取微信图片URL

        Args:
            html: HTML内容

        Returns:
            图片URL列表
        """
        # 匹配微信图片域名
        img_urls = re.findall(r'https?://mmbiz\.qpic\.cn/[^\s"\'&<>]+', html)
        # 去重
        img_urls = list(set(img_urls))
        return img_urls

    def download_image(self, url: str, output_path: str, skip_if_exists: bool = True) -> bool:
        """
        下载单张图片

        Args:
            url: 图片URL
            output_path: 保存路径
            skip_if_exists: 如果文件已存在则跳过

        Returns:
            是否成功
        """
        try:
            if skip_if_exists and os.path.exists(output_path):
                self.success_count += 1
                self.downloaded_files.append(output_path)
                return True

            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                f.write(response.content)

            self.success_count += 1
            self.downloaded_files.append(output_path)
            return True

        except Exception as e:
            print(f"下载失败 {url}: {str(e)}")
            self.fail_count += 1
            return False

    def download_from_article(self, url: str, output_dir: str) -> Dict:
        """
        从微信文章URL下载所有图片

        Args:
            url: 微信文章URL
            output_dir: 输出目录

        Returns:
            下载结果字典
        """
        # 重置统计
        self.success_count = 0
        self.fail_count = 0
        self.downloaded_files = []

        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)

        print(f"正在获取文章: {url}")
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()
        html = response.text

        # 提取图片URL
        img_urls = self.extract_image_urls(html)
        print(f"找到 {len(img_urls)} 张图片")

        # 下载图片
        for i, img_url in enumerate(img_urls, 1):
            # 生成唯一文件名
            url_hash = abs(hash(img_url)) % 10000
            filename = f'image_{i:02d}_{url_hash}.jpg'
            output_path = os.path.join(output_dir, filename)

            print(f"[{i}/{len(img_urls)}] 下载中: {filename}")
            self.download_image(img_url, output_path)

            if i < len(img_urls):
                time.sleep(self.delay)

        # 返回结果
        result = {
            'success': self.success_count,
            'failed': self.fail_count,
            'total': len(img_urls),
            'output_dir': os.path.abspath(output_dir),
            'files': self.downloaded_files
        }

        print(f"\n下载完成! 成功: {result['success']}, 失败: {result['failed']}")
        print(f"保存位置: {result['output_dir']}")

        return result

    def get_summary(self) -> Dict:
        """
        获取下载摘要

        Returns:
            摘要字典
        """
        return {
            'success': self.success_count,
            'failed': self.fail_count,
            'total': self.success_count + self.fail_count,
            'files': self.downloaded_files
        }

    def reset(self):
        """重置统计"""
        self.success_count = 0
        self.fail_count = 0
        self.downloaded_files = []
