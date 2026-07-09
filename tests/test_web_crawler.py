"""
Web Crawler 测试
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.web_crawler import WebCrawler


class TestWebCrawler:
    """测试 WebCrawler 类"""

    def test_init_default(self):
        """测试默认初始化"""
        crawler = WebCrawler()
        assert crawler.timeout == 10
        assert "User-Agent" in crawler.headers

    def test_init_custom(self):
        """测试自定义初始化"""
        custom_headers = {"X-Custom": "test"}
        crawler = WebCrawler(headers=custom_headers, timeout=30)
        assert crawler.timeout == 30
        assert crawler.headers["X-Custom"] == "test"

    def test_is_valid_url(self):
        """测试URL有效性检查"""
        crawler = WebCrawler()
        assert crawler.is_valid_url("https://example.com") is True
        assert crawler.is_valid_url("http://example.org/path") is True
        assert crawler.is_valid_url("not-a-url") is False
        assert crawler.is_valid_url("") is False
        assert crawler.is_valid_url("ftp://example.com") is True

    def test_get_base_url(self):
        """测试获取基础URL"""
        crawler = WebCrawler()
        assert crawler.get_base_url("https://example.com/path") == "https://example.com"
        assert crawler.get_base_url("http://example.org:8080/path") == "http://example.org:8080"

    def test_get_soup(self):
        """测试获取BeautifulSoup对象"""
        crawler = WebCrawler()
        html = "<html><body><h1>Test</h1></body></html>"
        soup = crawler.get_soup(html)
        assert soup is not None
        assert soup.find("h1").get_text() == "Test"

    def test_extract_text(self):
        """测试提取文本"""
        crawler = WebCrawler()
        html = "<html><body><h1>Title</h1><p>Paragraph</p></body></html>"
        text = crawler.extract_text(html)
        assert "Title" in text
        assert "Paragraph" in text

    def test_extract_links(self):
        """测试提取链接"""
        crawler = WebCrawler()
        html = """
        <html>
            <body>
                <a href="https://example.com">Link 1</a>
                <a href="/page2">Link 2</a>
                <a href="page3">Link 3</a>
            </body>
        </html>
        """
        links = crawler.extract_links(html)
        assert len(links) == 3
        assert "https://example.com" in links

        links_with_base = crawler.extract_links(html, base_url="https://example.org")
        assert "https://example.org/page2" in links_with_base

    def test_select(self):
        """测试CSS选择器"""
        crawler = WebCrawler()
        html = """
        <html>
            <body>
                <h1 class="title">Title 1</h1>
                <h1 class="title">Title 2</h1>
                <p>Paragraph</p>
            </body>
        </html>
        """
        titles = crawler.select(html, "h1.title")
        assert len(titles) == 2
        assert "Title 1" in titles
        assert "Title 2" in titles

    def test_select_attr(self):
        """测试提取属性"""
        crawler = WebCrawler()
        html = """
        <html>
            <body>
                <img src="image1.jpg" alt="Image 1">
                <img src="image2.jpg" alt="Image 2">
            </body>
        </html>
        """
        srcs = crawler.select_attr(html, "img", "src")
        assert len(srcs) == 2
        assert "image1.jpg" in srcs
        assert "image2.jpg" in srcs

    def test_extract_images(self):
        """测试提取图片URL"""
        crawler = WebCrawler()
        html = """
        <html>
            <body>
                <img src="image1.jpg">
                <img src="/images/image2.jpg">
            </body>
        </html>
        """
        images = crawler.extract_images(html)
        assert len(images) == 2

        images_with_base = crawler.extract_images(html, base_url="https://example.com")
        assert "https://example.com/images/image2.jpg" in images_with_base


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
