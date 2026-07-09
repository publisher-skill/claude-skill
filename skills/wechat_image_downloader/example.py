
"""
微信公众号图片下载器 - 使用示例
"""

from wechat_image_downloader import WeChatImageDownloader


def example_basic():
    """基本使用示例"""
    print("=== 基本使用示例 ===")

    # 创建下载器，设置请求间隔为0.3秒
    dl = WeChatImageDownloader(delay=0.3)

    # 下载微信文章图片
    result = dl.download_from_article(
        'https://mp.weixin.qq.com/s/JL733gXR6CvNKMg_2XtxGQ',
        'wechat_images/'
    )

    print(f"成功: {result['success']}")
    print(f"失败: {result['failed']}")
    print(f"保存到: {result['output_dir']}")


def example_custom_headers():
    """自定义请求头示例"""
    print("\n=== 自定义请求头示例 ===")

    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://mp.weixin.qq.com/'
    }

    dl = WeChatImageDownloader(headers=custom_headers, timeout=60, delay=0.5)
    result = dl.download_from_article(
        'https://mp.weixin.qq.com/s/JL733gXR6CvNKMg_2XtxGQ',
        'custom_images/'
    )


def example_extract_only():
    """仅提取URL不下载示例"""
    print("\n=== 仅提取URL示例 ===")

    dl = WeChatImageDownloader()

    # 获取文章HTML
    import requests
    url = 'https://mp.weixin.qq.com/s/JL733gXR6CvNKMg_2XtxGQ'
    response = requests.get(url, headers=dl.headers)
    html = response.text

    # 提取图片URL
    img_urls = dl.extract_image_urls(html)
    print(f"提取到 {len(img_urls)} 个图片URL:")
    for i, url in enumerate(img_urls[:5], 1):
        print(f"{i}. {url}")


if __name__ == '__main__':
    example_basic()
    # example_custom_headers()
    # example_extract_only()
