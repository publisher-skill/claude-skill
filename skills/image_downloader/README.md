# Image Downloader Skill

网站图片批量下载工具，功能丰富易用。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

```python
from skills.image_downloader import ImageDownloader

dl = ImageDownloader(delay=1.0)

# 从网页下载所有图片
downloaded = dl.download_from_url(
    'https://example.com/gallery',
    'images/gallery/'
)

# 查看结果
summary = dl.get_summary()
print(f"下载成功: {summary['downloaded']}")
```

## 使用示例

### 下载单张图片

```python
dl = ImageDownloader()
dl.download_image(
    'https://example.com/image.jpg',
    'images/my_image.jpg'
)
```

### 从网页批量下载

```python
dl = ImageDownloader(delay=0.5)

downloaded = dl.download_from_url(
    'https://example.com/photo-gallery',
    'images/gallery/',
    max_images=100,  # 限制数量
    filename_pattern='pic_{index:03d}'  # 自定义命名
)
```

### 批量下载URL列表

```python
dl = ImageDownloader()

urls = [
    'https://example.com/1.jpg',
    'https://example.com/2.jpg',
    'https://example.com/3.jpg',
]

dl.download_from_list(
    urls,
    'images/collection/',
    filename_prefix='photo'
)
```

### 全站爬取

```python
dl = ImageDownloader(delay=1.0)

downloaded = dl.crawl_and_download(
    'https://example.com',
    'images/site/',
    max_pages=20,  # 最多爬取20个页面
    include_subpages=True
)
```

### 查看下载结果

```python
summary = dl.get_summary()

print(f"成功: {summary['downloaded']}")
print(f"失败: {summary['failed']}")
print(f"跳过: {summary['skipped']}")

# 详细失败信息
for url, error in summary['failed_list']:
    print(f"{url}: {error}")
```

## 运行示例

```bash
cd skills/image_downloader
python example.py
```
