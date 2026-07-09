"""
Image Processor Skill
图片批量处理工具
"""

import os
from typing import List, Optional, Callable, Tuple


class ImageProcessor:
    """图片处理器"""

    def __init__(self):
        """初始化"""
        self._pillow_available = False
        self._check_dependencies()

    def _check_dependencies(self):
        """检查依赖"""
        try:
            from PIL import Image
            self._pillow_available = True
        except ImportError:
            self._pillow_available = False

    def _get_image(self, image_path: str):
        """获取图片对象"""
        from PIL import Image
        return Image.open(image_path)

    def resize_image(self, image_path: str, output_path: str,
                     width: int, height: int,
                     keep_ratio: bool = True) -> str:
        """调整图片尺寸

        Args:
            image_path: 输入图片路径
            output_path: 输出路径
            width: 宽度
            height: 高度
            keep_ratio: 是否保持宽高比

        Returns:
            输出文件路径
        """
        if not self._pillow_available:
            raise ImportError("请先安装: pip install Pillow")

        from PIL import Image

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        img = self._get_image(image_path)
        original_width, original_height = img.size

        if keep_ratio:
            ratio = min(width / original_width, height / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
        else:
            new_width = width
            new_height = height

        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        resized_img.save(output_path)

        return output_path

    def convert_format(self, image_path: str, output_path: str,
                       format: str = "JPEG", quality: int = 85) -> str:
        """转换图片格式

        Args:
            image_path: 输入图片路径
            output_path: 输出路径
            format: 输出格式（JPEG, PNG, WEBP, BMP, etc.）
            quality: 图片质量（0-100，仅部分格式支持）

        Returns:
            输出文件路径
        """
        if not self._pillow_available:
            raise ImportError("请先安装: pip install Pillow")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        img = self._get_image(image_path)

        if img.mode in ('RGBA', 'LA', 'P') and format in ('JPEG', 'WEBP'):
            background = img.convert('RGBA').resize(img.size)
            background.paste(img, mask=img.split()[3])
            img = background.convert('RGB')

        save_kwargs = {}
        if format in ('JPEG', 'WEBP'):
            save_kwargs['quality'] = quality

        img.save(output_path, format=format, **save_kwargs)

        return output_path

    def compress_image(self, image_path: str, output_path: str,
                       quality: int = 75) -> str:
        """压缩图片

        Args:
            image_path: 输入图片路径
            output_path: 输出路径
            quality: 压缩质量（0-100，越低越小）

        Returns:
            输出文件路径
        """
        if not self._pillow_available:
            raise ImportError("请先安装: pip install Pillow")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        img = self._get_image(image_path)

        img_format = img.format or 'JPEG'

        if img.mode in ('RGBA', 'LA', 'P') and img_format == 'JPEG':
            img = img.convert('RGB')

        if img_format in ('JPEG', 'WEBP'):
            img.save(output_path, img_format, quality=quality, optimize=True)
        else:
            img.save(output_path, optimize=True)

        return output_path

    def add_watermark(self, image_path: str, output_path: str,
                      watermark_path: str,
                      position: str = 'se',
                      opacity: float = 0.5) -> str:
        """添加水印

        Args:
            image_path: 输入图片路径
            output_path: 输出路径
            watermark_path: 水印图片路径
            position: 位置（tl, tr, bl, br, c）
            opacity: 透明度（0-1）

        Returns:
            输出文件路径
        """
        if not self._pillow_available:
            raise ImportError("请先安装: pip install Pillow")

        from PIL import Image

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        img = self._get_image(image_path).convert('RGBA')
        watermark = self._get_image(watermark_path).convert('RGBA')

        watermark_width, watermark_height = watermark.size
        img_width, img_height = img.size

        scale_factor = min(img_width / (watermark_width * 4), img_height / (watermark_height * 4), 1)
        new_width = int(watermark_width * scale_factor)
        new_height = int(watermark_height * scale_factor)

        if new_width > 0 and new_height > 0:
            watermark = watermark.resize((new_width, new_height), Image.Resampling.LANCZOS)

        if opacity < 1:
            watermark_alpha = watermark.split()[3]
            watermark_alpha = watermark_alpha.point(lambda x: int(x * opacity))
            watermark.putalpha(watermark_alpha)

        positions = {
            'tl': (0, 0),
            'tr': (img_width - new_width, 0),
            'bl': (0, img_height - new_height),
            'br': (img_width - new_width, img_height - new_height),
            'c': ((img_width - new_width) // 2, (img_height - new_height) // 2),
        }

        pos = positions.get(position, positions['br'])

        watermark_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        watermark_layer.paste(watermark, pos, watermark if watermark.mode == 'RGBA' else None)

        result = Image.alpha_composite(img, watermark_layer)
        result = result.convert('RGB')
        result.save(output_path, 'JPEG', quality=95)

        return output_path

    def batch_process(self, input_dir: str, output_dir: str,
                      process_func: Callable, file_ext: Optional[List[str]] = None,
                      **kwargs) -> Tuple[List[str], List[str]]:
        """批量处理图片

        Args:
            input_dir: 输入目录
            output_dir: 输出目录
            process_func: 处理函数
            file_ext: 文件扩展名列表（默认常用图片格式）
            **kwargs: 传递给处理函数的参数

        Returns:
            (成功列表, 失败列表)
        """
        if not self._pillow_available:
            raise ImportError("请先安装: pip install Pillow")

        if file_ext is None:
            file_ext = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']

        success_files = []
        failed_files = []

        os.makedirs(output_dir, exist_ok=True)

        for filename in os.listdir(input_dir):
            ext = os.path.splitext(filename)[1].lower()
            if ext in file_ext:
                try:
                    input_path = os.path.join(input_dir, filename)
                    output_path = os.path.join(output_dir, filename)

                    result = process_func(input_path, output_path, **kwargs)
                    success_files.append(result)
                except Exception as e:
                    failed_files.append((filename, str(e)))

        return success_files, failed_files

    def get_info(self, image_path: str) -> dict:
        """获取图片信息

        Args:
            image_path: 图片路径

        Returns:
            图片信息字典
        """
        if not self._pillow_available:
            raise ImportError("请先安装: pip install Pillow")

        img = self._get_image(image_path)
        width, height = img.size

        return {
            "width": width,
            "height": height,
            "format": img.format,
            "mode": img.mode,
            "size_bytes": os.path.getsize(image_path),
        }

    def rotate_image(self, image_path: str, output_path: str,
                     angle: int) -> str:
        """旋转图片

        Args:
            image_path: 输入图片路径
            output_path: 输出路径
            angle: 旋转角度（90, 180, 270, or 任意角度）

        Returns:
            输出文件路径
        """
        if not self._pillow_available:
            raise ImportError("请先安装: pip install Pillow")

        from PIL import Image

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        img = self._get_image(image_path)
        rotated_img = img.rotate(angle, expand=True, fillcolor='white')
        rotated_img.save(output_path, img.format or 'JPEG', quality=95)

        return output_path

    def is_available(self) -> bool:
        """检查是否可用"""
        return self._pillow_available


__all__ = ["ImageProcessor"]
