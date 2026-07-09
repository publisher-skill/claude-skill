"""
Image Downloader Skill 使用示例
"""

import os
import sys
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from skills.image_downloader import ImageDownloader


def example_basic_usage():
    """基本使用示例"""
    print("="*60)
    print("示例1: 基本使用")
    print("="*60)

    dl = ImageDownloader(delay=0.5)

    print("\n功能概览:")
    print("  - download_image: 下载单张图片")
    print("  - download_from_url: 从网页下载所有图片")
    print("  - download_from_list: 批量下载URL列表")
    print("  - crawl_and_download: 全站爬取下载")


def example_extract_images():
    """提取图片URL示例"""
    print("\n" + "="*60)
    print("示例2: 提取图片URL")
    print("="*60)

    dl = ImageDownloader()

    # 测试HTML
    html = """
    <html>
        <body>
            <img src="https://example.com/1.jpg" />
            <img data-src="https://example.com/2.jpg" />
            <div style="background-image: url('https://example.com/3.jpg');"></div>
            <picture>
                <source srcset="https://example.com/4.webp" />
                <img src="https://example.com/4.jpg" />
            </picture>
        </body>
    </html>
    """

    urls = dl.extract_image_urls(html, 'https://example.com')
    print(f"\n提取到 {len(urls)} 张图片:")
    for url in urls:
        print(f"  {url}")


def example_filename_handling():
    """文件名处理示例"""
    print("\n" + "="*60)
    print("示例3: 文件名处理")
    print("="*60)

    dl = ImageDownloader()

    test_urls = [
        'https://example.com/photos/image1.jpg',
        'https://example.com/images/cat-photo.png',
        'https://example.com/attachments/document.pdf?token=123',
    ]

    print("\n从URL提取文件名:")
    for url in test_urls:
        filename = dl.get_image_filename(url, 'default.jpg')
        print(f"  {url}")
        print(f"    -> {filename}")


def example_summary():
    """摘要示例"""
    print("\n" + "="*60)
    print("示例4: 下载摘要")
    print("="*60)

    print("\n下载完成后可获取摘要:")
    print("  summary = dl.get_summary()")
    print("  print(f'成功: {summary[\"downloaded\"]}')")
    print("  print(f'失败: {summary[\"failed\"]}')")
    print("  print(f'跳过: {summary[\"skipped\"]}')")


def example_weixin_download():
    """微信公众号文章下载示例"""
    print("\n" + "="*60)
    print("示例5: 微信公众号文章图片下载")
    print("="*60)

    print("""
使用方法:
from skills.image_downloader import ImageDownloader

# 创建下载器（可以设置较长的 delay 避免被封）
dl = ImageDownloader(delay=0.5)

# 从微信文章下载图片
downloaded = dl.download_from_weixin_article(
    'https://mp.weixin.qq.com/s/y-5TzQPXfi-8_LPt33Nhbw',
    'weixin_images',
    min_file_size=5000,  # 小于5KB的不保存（可能是图标）
    filename_pattern='main_{index:03d}'
)

# 查看结果
summary = dl.get_summary()
print(f'成功下载: {summary[\"downloaded\"]}')
print(f'失败: {summary[\"failed\"]}')

# 特殊功能:
# 1. 专门提取微信 mmbiz.qpic.cn/mmbiz.qlogo.cn 的图片
# 2. 从 data-src 属性提取（微信文章主要是 data-src）
# 3. 根据 wx_fmt 参数自动识别图片格式
# 4. 自动过滤小尺寸图片（避免下载图标）
""")


def quick_reference():
    """快速参考"""
    print("\n" + "="*60)
    print("快速参考")
    print("="*60)

    print("""
常用功能速查:

1. 从网页下载所有图片
   dl = ImageDownloader(delay=1.0)
   dl.download_from_url('https://example.com/gallery', 'images/')

2. 下载单张图片
   dl.download_image('https://example.com/img.jpg', 'images/img.jpg')

3. 批量下载URL列表
   urls = ['https://a.com/1.jpg', 'https://a.com/2.jpg']
   dl.download_from_list(urls, 'images/')

4. 全站爬取
   dl.crawl_and_download('https://example.com', 'images/site/', max_pages=20)

5. 微信公众号文章图片下载
   dl.download_from_weixin_article(
       'https://mp.weixin.qq.com/s/xxx',
       'weixin_images/',
       min_file_size=5000,  # 过滤小图
       filename_pattern='article_{index:03d}'
   )

6. 自定义下载参数
   dl = ImageDownloader(
       headers={'User-Agent': 'MyBot'},
       timeout=60,
       delay=2.0,  # 2秒间隔
       max_retries=5
   )

7. 自定义文件名
   dl.download_from_url(
       'https://example.com',
       'images/',
       filename_pattern='img_{index:03d}'
   )

8. 查看结果
   summary = dl.get_summary()
   print(f'成功: {summary[\"downloaded\"]}')
   print(f'失败: {summary[\"failed\"]}')
   for url, error in summary['failed_list']:
       print(f'{url}: {error}')
""")


if __name__ == "__main__":
    example_basic_usage()
    example_extract_images()
    example_filename_handling()
    example_summary()
    example_weixin_download()
    quick_reference()
