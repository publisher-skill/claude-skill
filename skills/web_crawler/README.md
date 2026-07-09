# Web Crawler Skill

基于 requests 和 BeautifulSoup 的网页爬虫工具。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

```python
from claude_skills.web_crawler import WebCrawler

crawler = WebCrawler()

# 抓取网页
html = crawler.fetch("https://example.com")

# 提取链接
links = crawler.extract_links(html, "https://example.com")

# 提取文本
text = crawler.extract_text(html)

# CSS选择器
titles = crawler.select(html, "h1")
```

## 更多示例

运行示例代码：

```bash
cd claude_skills/web_crawler
python example.py
```

## 功能列表

- ✅ 网页内容抓取
- ✅ 链接提取
- ✅ 文本提取
- ✅ CSS选择器支持
- ✅ 图片URL提取
- ✅ 图片下载
- ✅ JSON数据获取
- ✅ 自定义请求头
- ✅ 自动编码检测
