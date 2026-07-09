"""
Image Processor Skill 使用示例
"""

import os
import sys
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from skills.image_processor import ImageProcessor


def create_test_image(output_path):
    """创建测试图片"""
    try:
        from PIL import Image, ImageDraw, ImageFont

        img = Image.new('RGB', (800, 600), color='lightblue')
        draw = ImageDraw.Draw(img)

        draw.rectangle([100, 100, 700, 500], outline='white', width=3)
        draw.text((200, 250), '测试图片', fill='white')

        img.save(output_path, 'JPEG', quality=95)
        print(f"创建测试图片: {output_path}")
        return True
    except Exception as e:
        print(f"无法创建测试图片: {e}")
        return False


def example_basic_use():
    """基本使用示例"""
    print("="*60)
    print("示例 1: 图片工具基本使用")
    print("="*60)

    img = ImageProcessor()

    # 检查是否可用
    if not img.is_available():
        print("\n❌ 图片工具不可用")
        print("请运行: pip install Pillow")
        return

    print("\n✅ 图片工具已就绪")

    with tempfile.TemporaryDirectory() as temp_dir:
        test_image = os.path.join(temp_dir, "test.jpg")
        if not create_test_image(test_image):
            print("跳过示例演示")
            return

        print("\n" + "="*60)
        print("可用功能:")
        print("="*60)
        print("1. resize_image    - 调整尺寸")
        print("2. rotate_image    - 旋转图片")
        print("3. convert_format  - 转换格式")
        print("4. compress_image  - 压缩图片")
        print("5. add_watermark   - 添加水印")
        print("6. get_info        - 获取信息")
        print("7. batch_process   - 批量处理")


def example_resize():
    """调整尺寸示例"""
    print("\n" + "="*60)
    print("示例 2: 调整图片尺寸")
    print("="*60)

    print("""
使用方法:
    # 调整到 800x600（保持比例）
    img.resize_image('input.jpg', 'output.jpg', 800, 600)

    # 调整宽度为 1024（高度自动计算）
    img.resize_image('input.jpg', 'output.jpg', 1024, 768)
    """)


def example_compress():
    """压缩示例"""
    print("\n" + "="*60)
    print("示例 3: 压缩图片")
    print("="*60)

    print("""
使用方法:
    # 70% 质量
    img.compress_image('photo.jpg', 'compressed.jpg', quality=70)

    # 更小，50% 质量
    img.compress_image('photo.jpg', 'small.jpg', quality=50)

    # 高质量，90%
    img.compress_image('photo.jpg', 'hq.jpg', quality=90)
    """)


def example_watermark():
    """水印示例"""
    print("\n" + "="*60)
    print("示例 4: 添加水印")
    print("="*60)

    print("""
使用方法:
    # 右下角水印
    img.add_watermark('photo.jpg', 'out.jpg', 'logo.png', position='se')

    # 居中水印
    img.add_watermark('photo.jpg', 'out.jpg', 'logo.png', position='c')

    # 透明度调整
    img.add_watermark('photo.jpg', 'out.jpg', 'logo.png', opacity=0.3)
    """)


def quick_reference():
    """快速参考"""
    print("\n" + "="*60)
    print("图片工具速查")
    print("="*60)
    print("""
日常办公最常用:

1. 批量压缩会议照片
    img.batch_process('raw/', 'compressed/', img.compress_image, quality=70)

2. 图片转成 PDF 准备的大小
    img.resize_image('photo.jpg', 'pdf_photo.jpg', 1920, 1080)

3. 给产品图片加水印
    img.add_watermark('product.jpg', 'watermarked.jpg', 'logo.png', position='br', opacity=0.4)

4. PNG 转 JPG
    img.convert_format('image.png', 'image.jpg', format='JPEG', quality=85)

5. 旋转手机拍的竖屏照片
    img.rotate_image('portrait.jpg', 'landscape.jpg', 90)
    """)


if __name__ == "__main__":
    example_basic_use()
    example_resize()
    example_compress()
    example_watermark()
    quick_reference()
