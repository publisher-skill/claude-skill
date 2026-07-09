"""
FFmpeg Processor Skill
视频/音频处理工具
"""

import os
import subprocess
import json
import tempfile
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Union, Callable


class FFmpegProcessor:
    """FFmpeg 处理器"""

    def __init__(self, ffmpeg_path: str = 'ffmpeg', ffprobe_path: str = 'ffprobe'):
        """初始化

        Args:
            ffmpeg_path: ffmpeg 可执行文件路径
            ffprobe_path: ffprobe 可执行文件路径
        """
        self.ffmpeg_path = ffmpeg_path
        self.ffprobe_path = ffprobe_path
        self.verbose = False

    def _run_command(self, cmd: List[str], capture_output: bool = True) -> Tuple[int, str, str]:
        """运行命令

        Args:
            cmd: 命令列表
            capture_output: 是否捕获输出

        Returns:
            (返回码, stdout, stderr)
        """
        if self.verbose:
            print(f"Running: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            return result.returncode, result.stdout, result.stderr
        except FileNotFoundError:
            raise FileNotFoundError(
                f"无法找到 {self.ffmpeg_path} 或 {self.ffprobe_path}。"
                f"请确保已安装 FFmpeg 并添加到 PATH 环境变量中。"
            )

    def check_ffmpeg(self) -> bool:
        """检查 FFmpeg 是否可用

        Returns:
            是否可用
        """
        try:
            code, _, _ = self._run_command([self.ffmpeg_path, '-version'])
            return code == 0
        except Exception:
            return False

    def get_file_info(self, filepath: str) -> Dict:
        """获取媒体文件信息

        Args:
            filepath: 文件路径

        Returns:
            文件信息字典
        """
        filepath = os.path.abspath(filepath)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件不存在: {filepath}")

        cmd = [
            self.ffprobe_path,
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            filepath
        ]

        code, stdout, stderr = self._run_command(cmd)
        if code != 0:
            raise Exception(f"获取文件信息失败: {stderr}")

        return json.loads(stdout)

    def get_video_info(self, filepath: str) -> Dict:
        """获取视频信息

        Args:
            filepath: 文件路径

        Returns:
            视频信息
        """
        info = self.get_file_info(filepath)
        video_stream = None
        audio_stream = None

        for stream in info.get('streams', []):
            if stream.get('codec_type') == 'video' and not video_stream:
                video_stream = stream
            elif stream.get('codec_type') == 'audio' and not audio_stream:
                audio_stream = stream

        format_info = info.get('format', {})

        return {
            'filepath': filepath,
            'format': format_info.get('format_name'),
            'duration': float(format_info.get('duration', 0)),
            'size_bytes': int(format_info.get('size', 0)),
            'bitrate': int(format_info.get('bit_rate', 0)),
            'video': video_stream,
            'audio': audio_stream,
            'video_codec': video_stream.get('codec_name') if video_stream else None,
            'video_resolution': (
                f"{video_stream.get('width')}x{video_stream.get('height')}"
                if video_stream else None
            ),
            'video_fps': eval(video_stream.get('avg_frame_rate', '0/1')) if video_stream else 0,
            'audio_codec': audio_stream.get('codec_name') if audio_stream else None,
        }

    def convert_format(self, input_path: str, output_path: str,
                      video_codec: Optional[str] = None,
                      audio_codec: Optional[str] = None,
                      video_bitrate: Optional[str] = None,
                      audio_bitrate: Optional[str] = None,
                      quality: Optional[int] = None,
                      overwrite: bool = True) -> str:
        """转换视频格式

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            video_codec: 视频编码器
            audio_codec: 音频编码器
            video_bitrate: 视频比特率（如 '1M', '2000k'）
            audio_bitrate: 音频比特率（如 '128k'）
            quality: 质量（0-31，0为最高）
            overwrite: 是否覆盖

        Returns:
            输出文件路径
        """
        input_path = os.path.abspath(input_path)
        output_path = os.path.abspath(output_path)

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"文件不存在: {input_path}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        cmd = [self.ffmpeg_path, '-i', input_path]

        if video_codec:
            cmd.extend(['-c:v', video_codec])
        if audio_codec:
            cmd.extend(['-c:a', audio_codec])
        if video_bitrate:
            cmd.extend(['-b:v', video_bitrate])
        if audio_bitrate:
            cmd.extend(['-b:a', audio_bitrate])
        if quality is not None:
            cmd.extend(['-q:v', str(quality)])

        if overwrite:
            cmd.append('-y')

        cmd.append(output_path)

        code, _, stderr = self._run_command(cmd)
        if code != 0:
            raise Exception(f"转换失败: {stderr}")

        return output_path

    def to_mp4(self, input_path: str, output_path: Optional[str] = None,
              codec: str = 'libx264', **kwargs) -> str:
        """转换为 MP4

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            codec: 视频编码器
            **kwargs: 其他参数

        Returns:
            输出文件路径
        """
        if output_path is None:
            base, _ = os.path.splitext(input_path)
            output_path = f"{base}.mp4"

        return self.convert_format(input_path, output_path, video_codec=codec, **kwargs)

    def to_webm(self, input_path: str, output_path: Optional[str] = None,
               codec: str = 'libvpx-vp9', **kwargs) -> str:
        """转换为 WebM

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            codec: 视频编码器
            **kwargs: 其他参数

        Returns:
            输出文件路径
        """
        if output_path is None:
            base, _ = os.path.splitext(input_path)
            output_path = f"{base}.webm"

        return self.convert_format(input_path, output_path, video_codec=codec, **kwargs)

    def to_avi(self, input_path: str, output_path: Optional[str] = None,
              codec: str = 'libxvid', **kwargs) -> str:
        """转换为 AVI

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            codec: 视频编码器
            **kwargs: 其他参数

        Returns:
            输出文件路径
        """
        if output_path is None:
            base, _ = os.path.splitext(input_path)
            output_path = f"{base}.avi"

        return self.convert_format(input_path, output_path, video_codec=codec, **kwargs)

    def to_mp3(self, input_path: str, output_path: Optional[str] = None,
              bitrate: str = '192k', quality: Optional[int] = None) -> str:
        """提取音频为 MP3

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            bitrate: 比特率
            quality: 质量（0-9）

        Returns:
            输出文件路径
        """
        if output_path is None:
            base, _ = os.path.splitext(input_path)
            output_path = f"{base}.mp3"

        input_path = os.path.abspath(input_path)
        output_path = os.path.abspath(output_path)

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"文件不存在: {input_path}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        cmd = [self.ffmpeg_path, '-i', input_path]

        if quality is not None:
            cmd.extend(['-q:a', str(quality)])
        else:
            cmd.extend(['-b:a', bitrate])

        cmd.extend(['-y', output_path])

        code, _, stderr = self._run_command(cmd)
        if code != 0:
            raise Exception(f"转换失败: {stderr}")

        return output_path

    def to_aac(self, input_path: str, output_path: Optional[str] = None,
              bitrate: str = '192k') -> str:
        """提取音频为 AAC

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            bitrate: 比特率

        Returns:
            输出文件路径
        """
        if output_path is None:
            base, _ = os.path.splitext(input_path)
            output_path = f"{base}.aac"

        return self.convert_format(input_path, output_path, audio_codec='aac',
                                  audio_bitrate=bitrate)

    def resize_video(self, input_path: str, output_path: str,
                    width: int, height: int,
                    keep_aspect_ratio: bool = True) -> str:
        """调整视频尺寸

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            width: 宽度
            height: 高度
            keep_aspect_ratio: 是否保持宽高比

        Returns:
            输出文件路径
        """
        input_path = os.path.abspath(input_path)
        output_path = os.path.abspath(output_path)

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"文件不存在: {input_path}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        if keep_aspect_ratio:
            scale = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2"
        else:
            scale = f"scale={width}:{height}"

        cmd = [
            self.ffmpeg_path,
            '-i', input_path,
            '-vf', scale,
            '-y', output_path
        ]

        code, _, stderr = self._run_command(cmd)
        if code != 0:
            raise Exception(f"调整尺寸失败: {stderr}")

        return output_path

    def trim_video(self, input_path: str, output_path: str,
                  start_time: str = '00:00:00',
                  duration: Optional[str] = None,
                  end_time: Optional[str] = None) -> str:
        """裁剪视频

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            start_time: 开始时间（格式: HH:MM:SS 或 秒数）
            duration: 持续时长（优先级高于 end_time）
            end_time: 结束时间

        Returns:
            输出文件路径
        """
        input_path = os.path.abspath(input_path)
        output_path = os.path.abspath(output_path)

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"文件不存在: {input_path}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        cmd = [self.ffmpeg_path, '-ss', start_time, '-i', input_path]

        if duration:
            cmd.extend(['-t', duration])
        elif end_time:
            cmd.extend(['-to', end_time])

        cmd.extend(['-c', 'copy', '-y', output_path])

        code, _, stderr = self._run_command(cmd)
        if code != 0:
            raise Exception(f"裁剪失败: {stderr}")

        return output_path

    def extract_frame(self, input_path: str, output_path: str,
                     time: str = '00:00:01') -> str:
        """提取视频帧

        Args:
            input_path: 输入文件路径
            output_path: 输出图片路径
            time: 时间点

        Returns:
            输出文件路径
        """
        input_path = os.path.abspath(input_path)
        output_path = os.path.abspath(output_path)

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"文件不存在: {input_path}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        cmd = [
            self.ffmpeg_path,
            '-ss', time,
            '-i', input_path,
            '-vframes', '1',
            '-y', output_path
        ]

        code, _, stderr = self._run_command(cmd)
        if code != 0:
            raise Exception(f"提取帧失败: {stderr}")

        return output_path

    def extract_all_frames(self, input_path: str, output_dir: str,
                          format: str = 'frame_%04d.jpg',
                          fps: Optional[float] = None) -> List[str]:
        """提取所有帧

        Args:
            input_path: 输入文件路径
            output_dir: 输出目录
            format: 文件名格式
            fps: 每秒提取帧数（None则提取所有帧）

        Returns:
            输出文件列表
        """
        input_path = os.path.abspath(input_path)
        output_dir = os.path.abspath(output_dir)

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"文件不存在: {input_path}")

        os.makedirs(output_dir, exist_ok=True)

        output_pattern = os.path.join(output_dir, format)

        cmd = [self.ffmpeg_path, '-i', input_path]

        if fps:
            cmd.extend(['-vf', f'fps={fps}'])

        cmd.extend(['-y', output_pattern])

        code, _, stderr = self._run_command(cmd)
        if code != 0:
            raise Exception(f"提取帧失败: {stderr}")

        frames = []
        for filename in os.listdir(output_dir):
            if filename.startswith(format.split('%')[0]):
                frames.append(os.path.join(output_dir, filename))
        frames.sort()
        return frames

    def video_to_gif(self, input_path: str, output_path: str,
                    fps: int = 10,
                    width: Optional[int] = None,
                    start_time: Optional[str] = None,
                    duration: Optional[str] = None) -> str:
        """视频转 GIF

        Args:
            input_path: 输入文件路径
            output_path: 输出 GIF 路径
            fps: 帧率
            width: 宽度（保持宽高比）
            start_time: 开始时间
            duration: 持续时长

        Returns:
            输出文件路径
        """
        input_path = os.path.abspath(input_path)
        output_path = os.path.abspath(output_path)

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"文件不存在: {input_path}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        filters = [f'fps={fps}']
        if width:
            filters.append(f'scale={width}:-1')
        filters.append('split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse')

        cmd = [self.ffmpeg_path]
        if start_time:
            cmd.extend(['-ss', start_time])
        cmd.extend(['-i', input_path])
        if duration:
            cmd.extend(['-t', duration])
        cmd.extend(['-vf', ','.join(filters), '-y', output_path])

        code, _, stderr = self._run_command(cmd)
        if code != 0:
            raise Exception(f"转换 GIF 失败: {stderr}")

        return output_path

    def create_video_from_images(self, image_dir: str, output_path: str,
                               pattern: str = 'frame_%04d.jpg',
                               fps: float = 24.0,
                               image_format: str = 'image2') -> str:
        """从图片创建视频

        Args:
            image_dir: 图片目录
            output_path: 输出视频路径
            pattern: 文件名模式
            fps: 帧率
            image_format: 图片格式

        Returns:
            输出文件路径
        """
        image_dir = os.path.abspath(image_dir)
        output_path = os.path.abspath(output_path)

        if not os.path.exists(image_dir):
            raise FileNotFoundError(f"目录不存在: {image_dir}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        input_pattern = os.path.join(image_dir, pattern)

        cmd = [
            self.ffmpeg_path,
            '-framerate', str(fps),
            '-f', image_format,
            '-i', input_pattern,
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-y', output_path
        ]

        code, _, stderr = self._run_command(cmd)
        if code != 0:
            raise Exception(f"创建视频失败: {stderr}")

        return output_path

    def add_watermark(self, input_path: str, output_path: str,
                     watermark_path: str,
                     position: str = 'se',
                     offset_x: int = 10,
                     offset_y: int = 10,
                     opacity: float = 1.0) -> str:
        """添加水印

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            watermark_path: 水印图片路径
            position: 位置 (tl, tr, bl, br, c 等)
            offset_x: X偏移
            offset_y: Y偏移
            opacity: 透明度 (0.0-1.0)

        Returns:
            输出文件路径
        """
        input_path = os.path.abspath(input_path)
        output_path = os.path.abspath(output_path)
        watermark_path = os.path.abspath(watermark_path)

        for p in [input_path, watermark_path]:
            if not os.path.exists(p):
                raise FileNotFoundError(f"文件不存在: {p}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        positions = {
            'tl': f'W+{offset_x}:H+{offset_y}',
            'tr': f'main_w-overlay_w-{offset_x}:H+{offset_y}',
            'bl': f'W+{offset_x}:main_h-overlay_h-{offset_y}',
            'br': f'main_w-overlay_w-{offset_x}:main_h-overlay_h-{offset_y}',
            'c': '(main_w-overlay_w)/2:(main_h-overlay_h)/2',
        }

        pos = positions.get(position.lower(), positions['br'])

        filter_str = f"[1:v]scale=iw*0.25:ih*0.25[wm];[wm]alpha={opacity}[wm2];[0:v][wm2]overlay={pos}"

        cmd = [
            self.ffmpeg_path,
            '-i', input_path,
            '-i', watermark_path,
            '-filter_complex', filter_str,
            '-c:a', 'copy',
            '-y', output_path
        ]

        code, _, stderr = self._run_command(cmd)
        if code != 0:
            raise Exception(f"添加水印失败: {stderr}")

        return output_path

    def add_subtitle(self, input_path: str, output_path: str,
                    subtitle_path: str) -> str:
        """添加字幕

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            subtitle_path: 字幕文件路径 (srt, ass, etc.)

        Returns:
            输出文件路径
        """
        input_path = os.path.abspath(input_path)
        output_path = os.path.abspath(output_path)
        subtitle_path = os.path.abspath(subtitle_path)

        for p in [input_path, subtitle_path]:
            if not os.path.exists(p):
                raise FileNotFoundError(f"文件不存在: {p}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        ext = os.path.splitext(output_path)[1].lower()

        if ext in ['.mp4', '.mkv']:
            cmd = [
                self.ffmpeg_path,
                '-i', input_path,
                '-i', subtitle_path,
                '-c', 'copy',
                '-c:s', 'mov_text',
                '-y', output_path
            ]
        else:
            cmd = [
                self.ffmpeg_path,
                '-i', input_path,
                '-vf', f'subtitles={subtitle_path}',
                '-y', output_path
            ]

        code, _, stderr = self._run_command(cmd)
        if code != 0:
            raise Exception(f"添加字幕失败: {stderr}")

        return output_path

    def merge_videos(self, file_list: List[str], output_path: str,
                    use_concat_demuxer: bool = True) -> str:
        """合并多个视频

        Args:
            file_list: 文件列表
            output_path: 输出文件路径
            use_concat_demuxer: 是否使用 concat demuxer

        Returns:
            输出文件路径
        """
        output_path = os.path.abspath(output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        if use_concat_demuxer:
            file_list = [os.path.abspath(f) for f in file_list]
            for f in file_list:
                if not os.path.exists(f):
                    raise FileNotFoundError(f"文件不存在: {f}")

            list_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
            try:
                for f in file_list:
                    list_file.write(f"file '{f}'\n")
                list_file.close()

                cmd = [
                    self.ffmpeg_path,
                    '-f', 'concat',
                    '-safe', '0',
                    '-i', list_file.name,
                    '-c', 'copy',
                    '-y', output_path
                ]

                code, _, stderr = self._run_command(cmd)
            finally:
                os.unlink(list_file.name)
        else:
            filter_str = f"concat=n={len(file_list)}:v=1:a=1"

            cmd = [self.ffmpeg_path]
            for f in file_list:
                cmd.extend(['-i', f])
            cmd.extend(['-filter_complex', filter_str, '-y', output_path])

            code, _, stderr = self._run_command(cmd)

        if code != 0:
            raise Exception(f"合并视频失败: {stderr}")

        return output_path

    def change_speed(self, input_path: str, output_path: str,
                    speed: float) -> str:
        """调整视频速度

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            speed: 速度倍数 (0.5=慢放2倍, 2.0=快放2倍)

        Returns:
            输出文件路径
        """
        input_path = os.path.abspath(input_path)
        output_path = os.path.abspath(output_path)

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"文件不存在: {input_path}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        filter_str = f"[0:v]setpts={1/speed}*PTS[v];[0:a]atempo={speed}[a]"

        cmd = [
            self.ffmpeg_path,
            '-i', input_path,
            '-filter_complex', filter_str,
            '-map', '[v]',
            '-map', '[a]',
            '-y', output_path
        ]

        code, _, stderr = self._run_command(cmd)
        if code != 0:
            raise Exception(f"调整速度失败: {stderr}")

        return output_path

    def rotate_video(self, input_path: str, output_path: str,
                    rotation: int = 90) -> str:
        """旋转视频

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            rotation: 旋转角度 (90, 180, 270)

        Returns:
            输出文件路径
        """
        input_path = os.path.abspath(input_path)
        output_path = os.path.abspath(output_path)

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"文件不存在: {input_path}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        transpose = {90: 1, 180: 2, 270: 2}
        rotations = {90: 'transpose=1,transpose=1', 180: 'transpose=2,transpose=2', 270: 'transpose=2,transpose=2'}

        if rotation == 90:
            filter_str = 'transpose=1'
        elif rotation == 180:
            filter_str = 'transpose=2,transpose=2'
        elif rotation == 270:
            filter_str = 'transpose=2'
        else:
            raise ValueError("旋转角度必须是 90, 180, 或 270")

        cmd = [
            self.ffmpeg_path,
            '-i', input_path,
            '-vf', filter_str,
            '-y', output_path
        ]

        code, _, stderr = self._run_command(cmd)
        if code != 0:
            raise Exception(f"旋转失败: {stderr}")

        return output_path

    def extract_audio(self, input_path: str, output_path: str,
                     codec: str = 'mp3',
                     bitrate: str = '192k') -> str:
        """提取音频

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            codec: 音频编码
            bitrate: 比特率

        Returns:
            输出文件路径
        """
        input_path = os.path.abspath(input_path)
        output_path = os.path.abspath(output_path)

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"文件不存在: {input_path}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        codecs = {
            'mp3': 'libmp3lame',
            'aac': 'aac',
            'wav': 'pcm_s16le',
            'flac': 'flac',
            'opus': 'libopus',
        }

        cmd = [
            self.ffmpeg_path,
            '-i', input_path,
            '-vn',
            '-c:a', codecs.get(codec, codec),
            '-b:a', bitrate,
            '-y', output_path
        ]

        code, _, stderr = self._run_command(cmd)
        if code != 0:
            raise Exception(f"提取音频失败: {stderr}")

        return output_path

    def get_ffmpeg_version(self) -> str:
        """获取 FFmpeg 版本

        Returns:
            版本信息
        """
        cmd = [self.ffmpeg_path, '-version']
        code, stdout, stderr = self._run_command(cmd)
        if code != 0:
            raise Exception(f"获取版本失败: {stderr}")
        return stdout.split('\n')[0]


__all__ = ["FFmpegProcessor"]
