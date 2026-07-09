"""
Web Crawler Skill 使用示例
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from  web_crawler import WebCrawler


def example_basic_usage():
    """基础使用示例"""
    print("=== 基础使用示例 ===\n")

    crawler = WebCrawler()

    # 抓取网页
    url = "https://example.com"
    html = crawler.fetch(url)
    print(f"成功抓取: {url}")
    print(f"HTML长度: {len(html)} 字符\n")

    # 提取文本
    text = crawler.extract_text(html)
    print("页面文本:")
    print(text[:200] + "..." if len(text) > 200 else text)
    print()

    # 提取链接
    links = crawler.extract_links(html, base_url=url)
    print(f"找到 {len(links)} 个链接:")
    for link in links[:5]:
        print(f"  - {link}")
    if len(links) > 5:
        print(f"  ... 还有 {len(links) - 5} 个\n")


def example_css_selector():
    """CSS选择器示例"""
    print("=== CSS选择器示例 ===\n")

    crawler = WebCrawler()
    url = "https://example.com"
    html = crawler.fetch(url)

    # 使用CSS选择器
    titles = crawler.select(html, "h1")
    print(f"标题: {titles}")

    # 提取属性
    image_urls = crawler.select_attr(html, "img", "src")
    print(f"图片URL: {image_urls}\n")


def example_advanced():
    """高级功能示例"""
    print("=== 高级功能示例 ===\n")

    # 自定义请求头
    custom_headers = {
        "User-Agent": "WebCrawler/1.0 (Custom Bot)",
        "Accept": "text/html,application/xhtml+xml"
    }

    crawler = WebCrawler(headers=custom_headers, timeout=15)

    # 获取BeautifulSoup对象进行更复杂的解析
    url = "https://example.com"
    html = crawler.fetch(url)
    soup = crawler.get_soup(html)

    # 直接操作soup
    title_tag = soup.find("title")
    if title_tag:
        print(f"页面标题: {title_tag.get_text()}\n")

    # 检查URL有效性
    test_urls = ["https://example.com", "not-a-url", "ftp://example.com"]
    for test_url in test_urls:
        is_valid = crawler.is_valid_url(test_url)
        print(f"URL '{test_url}': {'有效' if is_valid else '无效'}")


if __name__ == "__main__":
    example_basic_usage()
    print("\n" + "="*50 + "\n")
    example_css_selector()
    print("\n" + "="*50 + "\n")
    example_advanced()
