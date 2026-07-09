
---
name: wechat_image_downloader
description: 微信公众号图片下载器 - 从微信公众号文章批量下载图片
metadata:
  type: custom
---

# 微信公众号图片下载器 Skill

专门用于从微信公众号文章中提取并下载所有图片的工具。

## 功能特性

### 📥 核心功能
- **自动提取**: 自动识别并提取微信文章中的所有图片
- **批量下载**: 一键下载所有图片到本地
- **智能命名**: 自动生成唯一文件名，避免覆盖
- **跳过已下载**: 支持断点续传，避免重复下载

### 🔧 智能功能
- **URL去重**: 自动去除重复的图片URL
- **请求延迟**: 避免请求过快被封禁
- **User-Agent伪装**: 模拟浏览器访问

## 使用方法

### Python API

```python
from skills.wechat_image_downloader import WeChatImageDownloader

# 创建下载器实例
dl = WeChatImageDownloader(delay=0.3)

# 从微信文章URL下载图片
result = dl.download_from_article(
    'https://mp.weixin.qq.com/s/xxx',
    'output_directory/'
)

# 查看结果
print(f"成功: {result['success']}")
print(f"失败: {result['failed']}")
print(f"保存位置: {result['output_dir']}")
```

### 命令行使用

```python
from skills.wechat_image_downloader import WeChatImageDownloader

dl = WeChatImageDownloader()
dl.download_from_article('https://mp.weixin.qq.com/s/xxx', 'images/')
```

## API 参考

### WeChatImageDownloader 类

#### 初始化
```python
WeChatImageDownloader(headers=None, timeout=30, delay=0.5)
```
- `headers`: 自定义请求头
- `timeout`: 请求超时时间（秒）
- `delay`: 请求间隔（秒）

#### 主要方法
- `download_from_article(url, output_dir)` - 从微信文章URL下载所有图片
- `extract_image_urls(html)` - 从HTML中提取微信图片URL
- `download_image(url, output_path)` - 下载单张图片
- `get_summary()` - 获取下载摘要

#### 返回结果
`download_from_article` 返回字典：
```python
{
    'success': 26,      # 成功数量
    'failed': 0,        # 失败数量
    'total': 26,        # 总数
    'output_dir': '...' # 保存目录
}
```
