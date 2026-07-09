---
name: image_downloader
description: 图片下载器 - 从网站批量下载图片，支持单张图片、HTML页面、网站全站爬取
metadata:
  type: custom
---

# Image Downloader Skill

网站图片批量下载工具，功能丰富易用。

## 功能特性

### 📥 多种下载方式
- **单张图片**: 直接下载单个图片URL
- **HTML页面**: 提取网页中所有图片
- **URL列表**: 批量下载多个图片链接
- **全站爬取**: 递归爬取并下载整个网站的图片

### 🔧 智能功能
- **自动去重**: 检测重复文件（内容比对）
- **跳过已下载**: 避免重复下载
- **重试机制**: 下载失败自动重试
- **请求延迟**: 避免请求过快被封禁
- **图片来源**: 提取 `<img>`, `<picture>`, CSS `background-image`

### 📁 文件管理
- **智能命名**: 从URL提取文件名
- **自定义命名**: 支持自定义文件名模式
- **目录组织**: 按页面或自定义规则保存
- **清理文件名**: 自动处理非法字符

## 使用方法

### Python API

```python
from skills.image_downloader import ImageDownloader

dl = ImageDownloader(delay=1.0)

# 下载单张图片
dl.download_image('https://example.com/img.jpg', 'images/img.jpg')

# 从网页下载所有图片
downloaded = dl.download_from_url(
    'https://example.com/gallery',
    'images/gallery/',
    max_images=50
)

# 批量下载URL列表
urls = ['https://a.com/1.jpg', 'https://a.com/2.jpg']
dl.download_from_list(urls, 'images/')

# 全站爬取
dl.crawl_and_download(
    'https://example.com',
    'images/site/',
    max_pages=20
)

# 查看摘要
summary = dl.get_summary()
print(f"成功: {summary['downloaded']}")
print(f"失败: {summary['failed']}")
```

## API 参考

### ImageDownloader 类

#### 初始化
```python
ImageDownloader(headers=None, timeout=30, delay=0.5, max_retries=3)
```

#### 下载方法
- `download_image(url, output_path, skip_if_exists=True, check_duplicate=True)` - 下载单张图片
- `download_from_url(url, output_dir, extract_from_html=True, skip_if_exists=True, max_images=None, filename_pattern=None)` - 从URL下载
- `download_from_list(url_list, output_dir, skip_if_exists=True, filename_prefix='image')` - 从列表下载
- `crawl_and_download(start_url, output_dir, max_pages=10, include_subpages=True, skip_if_exists=True)` - 全站爬取

#### 辅助方法
- `extract_image_urls(html, base_url, include_bg_images=True, deduplicate=True)` - 提取图片URL
- `is_image_url(url)` - 检查是否是图片URL
- `get_image_filename(url, default)` - 获取文件名
- `get_summary()` - 获取下载摘要
- `reset()` - 重置状态
