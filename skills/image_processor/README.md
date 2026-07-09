# Image Processor Skill

图片批量处理工具，日常办公必备！

## 安装依赖

```bash
pip install Pillow
```

或使用目录下的 requirements.txt：

```bash
cd skills/image_processor
pip install -r requirements.txt
```

## 快速开始

```python
from skills.image_processor import ImageProcessor

img = ImageProcessor()

# 压缩图片
img.compress_image('photo.jpg', 'compressed.jpg', quality=70)

# 调整尺寸
img.resize_image('photo.jpg', 'small.jpg', 800, 600)

# 添加水印
img.add_watermark('photo.jpg', 'watermarked.jpg', 'logo.png')
```

## 使用示例

### 调整图片尺寸

```python
# 调整到指定大小（保持宽高比）
img.resize_image('photo.jpg', 'output.jpg', 800, 600)

# 强制指定尺寸（不保持比例）
img.resize_image('photo.jpg', 'output.jpg', 800, 600, keep_ratio=False)
```

### 转换图片格式

```python
# PNG 转 JPEG
img.convert_format('photo.png', 'photo.jpg', format='JPEG', quality=85)

# JPEG 转 WEBP
img.convert_format('photo.jpg', 'photo.webp', format='WEBP', quality=90)
```

### 压缩图片

```python
# 压缩到 70% 质量
img.compress_image('photo.jpg', 'compressed.jpg', quality=70)

# 更小的文件
img.compress_image('photo.jpg', 'small.jpg', quality=50)
```

### 添加水印

```python
# 右下角水印
img.add_watermark('photo.jpg', 'output.jpg', 'logo.png', position='se')

# 居中水印，半透明
img.add_watermark('photo.jpg', 'output.jpg', 'logo.png', position='c', opacity=0.3)

# 左上角水印
img.add_watermark('photo.jpg', 'output.jpg', 'logo.png', position='tl', opacity=0.6)
```

### 旋转图片

```python
# 旋转 90 度
img.rotate_image('photo.jpg', 'rotated.jpg', 90)

# 旋转 180 度
img.rotate_image('photo.jpg', 'upside_down.jpg', 180)

# 旋转 270 度
img.rotate_image('photo.jpg', 'sideways.jpg', 270)
```

### 批量处理

```python
# 批量压缩整个文件夹
success, failed = img.batch_process(
    'original/',
    'compressed/',
    img.compress_image,
    quality=70
)

print(f"成功: {len(success)}")
print(f"失败: {len(failed)}")
for filename, error in failed:
    print(f"{filename}: {error}")

# 批量调整尺寸
success, failed = img.batch_process(
    'original/',
    'resized/',
    img.resize_image,
    width=800,
    height=600
)

# 批量添加水印
success, failed = img.batch_process(
    'original/',
    'watermarked/',
    img.add_watermark,
    watermark_path='logo.png',
    position='se',
    opacity=0.5
)
```

### 获取图片信息

```python
info = img.get_info('photo.jpg')
print(f"尺寸: {info['width']}x{info['height']}")
print(f"格式: {info['format']}")
print(f"大小: {info['size_bytes']} bytes")
```

### 位置说明

```
tl: 左上角
tr: 右上角
bl: 左下角
br/se: 右下角
c: 居中
```

## 运行示例

```bash
cd skills/image_processor
python example.py
```
