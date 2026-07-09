---
name: web-crawler
description: 基于requests和BeautifulSoup的网页爬虫skill，支持抓取网页内容、提取链接、下载图片等功能
metadata:
  type: custom
---

# Web Crawler Skill

一个功能强大的网页爬虫工具，基于requests和BeautifulSoup4构建。

## 功能特性

- 抓取网页HTML内容
- 提取页面中的所有链接
- 下载图片到本地
- 提取页面文本内容
- CSS选择器支持
- 自动处理编码
- 支持自定义请求头

## 使用方法

### 基础使用

```python
from claude_skills.web_crawler import WebCrawler

# 创建爬虫实例
crawler = WebCrawler()

# 抓取网页
html = crawler.fetch("https://example.com")

# 提取所有链接
links = crawler.extract_links(html)

# 下载图片
crawler.download_image("https://example.com/image.jpg", "output/image.jpg")

# 使用CSS选择器提取内容
titles = crawler.select(html, "h1.title")
```

### 高级配置

```python
# 自定义请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
crawler = WebCrawler(headers=headers, timeout=30)
```

## API 参考

### WebCrawler类

#### `__init__(headers=None, timeout=10)`

初始化爬虫实例。

**参数:**
- `headers` (dict, optional): 自定义HTTP请求头
- `timeout` (int, optional): 请求超时时间（秒）

#### `fetch(url, params=None)`

获取网页HTML内容。

**参数:**
- `url` (str): 目标URL
- `params` (dict, optional): URL查询参数

**返回:**
- `str`: HTML内容

#### `extract_links(html, base_url=None)`

从HTML中提取所有链接。

**参数:**
- `html` (str): HTML内容
- `base_url` (str, optional): 基础URL，用于补全相对链接

**返回:**
- `list`: 链接列表

#### `extract_text(html)`

从HTML中提取纯文本内容。

**参数:**
- `html` (str): HTML内容

**返回:**
- `str`: 纯文本内容

#### `select(html, selector)`

使用CSS选择器提取元素。

**参数:**
- `html` (str): HTML内容
- `selector` (str): CSS选择器

**返回:**
- `list`: 匹配的元素文本列表

#### `download_image(url, save_path)`

下载图片到本地。

**参数:**
- `url` (str): 图片URL
- `save_path` (str): 保存路径

#### `get_soup(html)`

获取BeautifulSoup对象，进行更复杂的解析。

**参数:**
- `html` (str): HTML内容

**返回:**
- `BeautifulSoup`: Soup对象
