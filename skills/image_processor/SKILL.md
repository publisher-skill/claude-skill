---
name: image_processor
description: 图片处理器 - 批量压缩、格式转换、尺寸调整、加水印
metadata:
  type: custom
---

# Image Processor Skill

图片批量处理工具，日常办公必备！

## 功能特性

### 📐 尺寸调整
- **调整尺寸**: 自定义宽高，自动保持宽高比
- **旋转图片**: 90/180/270 度旋转

### 📦 格式压缩
- **格式转换**: JPEG/PNG/WEBP/BMP 互转
- **批量压缩**: 压缩图片大小，保持画质
- **质量控制**: 0-100 质量可调

### 🖼️ 水印处理
- **添加水印**: 支持多位置、透明度调整
- **批量水印**: 一键给多张图加水印

### 📊 信息查看
- **获取信息**: 尺寸、格式、大小等信息
- **批量操作**: 一键处理整个文件夹

## 使用方法

### Python API

```python
from skills.image_processor import ImageProcessor

img = ImageProcessor()

# 检查是否可用
if not img.is_available():
    print("请先安装: pip install Pillow")
    exit(1)

# 调整尺寸
img.resize_image('input.jpg', 'output.jpg', 800, 600)

# 转换格式
img.convert_format('input.png', 'output.jpg', format='JPEG', quality=85)

# 压缩图片
img.compress_image('input.jpg', 'compressed.jpg', quality=70)

# 添加水印
img.add_watermark('input.jpg', 'output.jpg', 'watermark.png', position='se', opacity=0.5)

# 批量压缩
success, failed = img.batch_process('input_dir', 'output_dir', img.compress_image, quality=75)
```

## API 参考

### ImageProcessor 类

#### 图片处理
- `resize_image(image_path, output_path, width, height, keep_ratio=True)` - 调整尺寸
- `rotate_image(image_path, output_path, angle)` - 旋转图片
- `convert_format(image_path, output_path, format='JPEG', quality=85)` - 转换格式
- `compress_image(image_path, output_path, quality=75)` - 压缩图片
- `add_watermark(image_path, output_path, watermark_path, position='se', opacity=0.5)` - 添加水印

#### 批量操作
- `batch_process(input_dir, output_dir, process_func, file_ext=None, **kwargs)` - 批量处理

#### 信息查看
- `get_info(image_path)` - 获取图片信息
- `is_available()` - 检查是否可用
