
# 微信公众号图片下载器

专门用于从微信公众号文章中批量下载图片的工具。

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

```python
from wechat_image_downloader import WeChatImageDownloader

# 创建下载器
dl = WeChatImageDownloader(delay=0.3)

# 下载文章图片
result = dl.download_from_article(
    'https://mp.weixin.qq.com/s/JL733gXR6CvNKMg_2XtxGQ',
    'wechat_images/'
)
```

## 使用示例

更多示例请参考 `example.py`。
