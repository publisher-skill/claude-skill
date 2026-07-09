"""
Web Crawler Skill
基于requests和BeautifulSoup的网页爬虫工具
"""

import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Any


class WebCrawler:
    """网页爬虫类"""

    def __init__(self, headers: Optional[Dict[str, str]] = None, timeout: int = 10):
        """
        初始化爬虫实例

        Args:
            headers: 自定义HTTP请求头
            timeout: 请求超时时间（秒）
        """
        self.timeout = timeout
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def fetch(self, url: str, params: Optional[Dict[str, Any]] = None) -> str:
        """
        获取网页HTML内容

        Args:
            url: 目标URL
            params: URL查询参数

        Returns:
            HTML内容字符串

        Raises:
            requests.RequestException: 请求失败时抛出
        """
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text

    def get_soup(self, html: str, parser: str = "html.parser") -> BeautifulSoup:
        """
        获取BeautifulSoup对象

        Args:
            html: HTML内容
            parser: 解析器类型（html.parser, lxml, html5lib）

        Returns:
            BeautifulSoup对象
        """
        return BeautifulSoup(html, parser)

    def extract_links(self, html: str, base_url: Optional[str] = None) -> List[str]:
        """
        从HTML中提取所有链接

        Args:
            html: HTML内容
            base_url: 基础URL，用于补全相对链接

        Returns:
            链接列表
        """
        soup = self.get_soup(html)
        links = []
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if base_url:
                href = urljoin(base_url, href)
            links.append(href)
        return links

    def extract_text(self, html: str) -> str:
        """
        从HTML中提取纯文本内容

        Args:
            html: HTML内容

        Returns:
            纯文本内容
        """
        soup = self.get_soup(html)
        return soup.get_text(separator="\n", strip=True)

    def select(self, html: str, selector: str) -> List[str]:
        """
        使用CSS选择器提取元素文本

        Args:
            html: HTML内容
            selector: CSS选择器

        Returns:
            匹配的元素文本列表
        """
        soup = self.get_soup(html)
        elements = soup.select(selector)
        return [elem.get_text(strip=True) for elem in elements]

    def select_attr(self, html: str, selector: str, attr: str) -> List[str]:
        """
        使用CSS选择器提取元素属性

        Args:
            html: HTML内容
            selector: CSS选择器
            attr: 属性名

        Returns:
            属性值列表
        """
        soup = self.get_soup(html)
        elements = soup.select(selector)
        values = []
        for elem in elements:
            if elem.has_attr(attr):
                values.append(elem[attr])
        return values

    def extract_images(self, html: str, base_url: Optional[str] = None) -> List[str]:
        """
        提取所有图片URL

        Args:
            html: HTML内容
            base_url: 基础URL，用于补全相对链接

        Returns:
            图片URL列表
        """
        soup = self.get_soup(html)
        images = []
        for img_tag in soup.find_all("img", src=True):
            src = img_tag["src"]
            if base_url:
                src = urljoin(base_url, src)
            images.append(src)
        return images

    def download_image(self, url: str, save_path: str, make_dirs: bool = True) -> None:
        """
        下载图片到本地

        Args:
            url: 图片URL
            save_path: 保存路径
            make_dirs: 是否自动创建目录
        """
        if make_dirs:
            dir_path = os.path.dirname(save_path)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)

        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()

        with open(save_path, "wb") as f:
            f.write(response.content)

    def fetch_json(self, url: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        获取JSON数据

        Args:
            url: API URL
            params: 查询参数

        Returns:
            解析后的JSON数据
        """
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def is_valid_url(self, url: str) -> bool:
        """
        检查URL是否有效

        Args:
            url: 待检查的URL

        Returns:
            是否有效
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def get_base_url(self, url: str) -> str:
        """
        获取URL的基础部分

        Args:
            url: 完整URL

        Returns:
            基础URL (scheme://netloc)
        """
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"


__all__ = ["WebCrawler"]
