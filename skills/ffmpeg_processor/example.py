"""
FFmpeg Processor Skill 使用示例
"""

import os
import sys
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from skills.ffmpeg_processor import FFmpegProcessor


def create_test_video(output_path: str):
    """创建测试视频（使用 FFmpeg 生成简单视频）

    注意：这需要 FFmpeg 可用
    """
    import subprocess

    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', 'color=c=red:s=320x240:r=10',
        '-t', '5',
        '-f', 'lavfi',
        '-i', 'sine=frequency=440:duration=5',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-y', output_path
    ]

    subprocess.run(cmd, capture_output=True)


def example_check_ffmpeg():
    """检查 FFmpeg"""
    print("="*60)
    print("示例1: 检查 FFmpeg")
    print("="*60)

    ff = FFmpegProcessor()

    print(f"\nFFmpeg 可用: {ff.check_ffmpeg()}")

    if ff.check_ffmpeg():
        version = ff.get_ffmpeg_version()
        print(f"\nFFmpeg 版本: {version}")


def example_format_conversion():
    """格式转换示例"""
    print("\n" + "="*60)
    print("示例2: 格式转换")
    print("="*60)

    ff = FFmpegProcessor()

    if not ff.check_ffmpeg():
        print("FFmpeg 不可用，跳过此示例")
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        input_video = os.path.join(temp_dir, 'test.mp4')
        print(f"\n创建测试视频: {input_video}")
        create_test_video(input_video)

        if not os.path.exists(input_video):
            print("测试视频创建失败，可能 FFmpeg 不可用")
            return

        output_webm = os.path.join(temp_dir, 'test.webm')
        output_mp3 = os.path.join(temp_dir, 'test.mp3')

        print(f"\n转换为 WebM: {output_webm}")
        try:
            ff.to_webm(input_video, output_webm)
            print("✓ 成功")
        except Exception as e:
            print(f"✗ 失败: {e}")

        print(f"\n转换为 MP3: {output_mp3}")
        try:
            ff.to_mp3(input_video, output_mp3)
            print("✓ 成功")
        except Exception as e:
            print(f"✗ 失败: {e}")


def example_get_info():
    """获取视频信息示例"""
    print("\n" + "="*60)
    print("示例3: 获取视频信息")
    print("="*60)

    ff = FFmpegProcessor()

    if not ff.check_ffmpeg():
        print("FFmpeg 不可用，跳过此示例")
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        input_video = os.path.join(temp_dir, 'test.mp4')
        create_test_video(input_video)

        if not os.path.exists(input_video):
            print("测试视频创建失败")
            return

        print(f"\n获取视频信息: {input_video}")
        try:
            info = ff.get_video_info(input_video)
            print(f"\n格式: {info['format']}")
            print(f"时长: {info['duration']:.2f}秒")
            print(f"分辨率: {info['video_resolution']}")
            print(f"视频编码: {info['video_codec']}")
            if info.get('audio_codec'):
                print(f"音频编码: {info['audio_codec']}")
        except Exception as e:
            print(f"✗ 失败: {e}")


def example_video_editing():
    """视频编辑示例"""
    print("\n" + "="*60)
    print("示例4: 视频编辑")
    print("="*60)

    ff = FFmpegProcessor()

    if not ff.check_ffmpeg():
        print("FFmpeg 不可用，跳过此示例")
        return

    print("\n可用功能:")
    print("  - trim_video: 裁剪视频")
    print("  - resize_video: 调整尺寸")
    print("  - rotate_video: 旋转视频")
    print("  - change_speed: 调整速度")


def example_extract_frames():
    """提取帧示例"""
    print("\n" + "="*60)
    print("示例5: 提取视频帧")
    print("="*60)

    print("\n可用功能:")
    print("  - extract_frame: 提取单帧")
    print("  - extract_all_frames: 提取所有帧")


def example_video_to_gif():
    """视频转 GIF 示例"""
    print("\n" + "="*60)
    print("示例6: 视频转 GIF")
    print("="*60)

    print("\n使用方法:")
    print("  ff.video_to_gif('input.mp4', 'output.gif', fps=10, width=500)")


def example_watermark():
    """水印示例"""
    print("\n" + "="*60)
    print("示例7: 添加水印")
    print("="*60)

    print("\n可用位置:")
    print("  tl - 左上角")
    print("  tr - 右上角")
    print("  bl - 左下角")
    print("  br - 右下角")
    print("  c - 中心")


def example_merge_videos():
    """合并视频示例"""
    print("\n" + "="*60)
    print("示例8: 合并视频")
    print("="*60)

    print("\n使用方法:")
    print("  videos = ['part1.mp4', 'part2.mp4']")
    print("  ff.merge_videos(videos, 'merged.mp4')")


def example_audio_extraction():
    """音频提取示例"""
    print("\n" + "="*60)
    print("示例9: 提取音频")
    print("="*60)

    print("\n支持格式:")
    print("  - mp3 - MP3")
    print("  - aac - AAC")
    print("  - wav - WAV")
    print("  - flac - FLAC")


def example_subtitle():
    """字幕示例"""
    print("\n" + "="*60)
    print("示例10: 添加字幕")
    print("="*60)

    print("\n使用方法:")
    print("  ff.add_subtitle('video.mp4', 'output.mp4', 'subtitle.srt')")


def example_image_to_video():
    """图片转视频示例"""
    print("\n" + "="*60)
    print("示例11: 图片合成视频")
    print("="*60)

    print("\n使用方法:")
    print("  ff.create_video_from_images('images/', 'output.mp4',")
    print("                            pattern='frame_%04d.jpg', fps=24)")


def quick_reference():
    """快速参考"""
    print("\n" + "="*60)
    print("快速参考")
    print("="*60)

    print("""
常用功能速查:

1. 格式转换
   ff.to_mp4('input.avi', 'output.mp4')
   ff.to_mp3('video.mp4', 'audio.mp3')

2. 裁剪视频
   ff.trim_video('input.mp4', 'out.mp4', '00:00:10', duration='00:00:30')

3. 调整尺寸
   ff.resize_video('input.mp4', 'out.mp4', 1920, 1080)

4. 视频转 GIF
   ff.video_to_gif('input.mp4', 'out.gif', fps=15, width=640)

5. 添加水印
   ff.add_watermark('input.mp4', 'out.mp4', 'logo.png', position='br')

6. 合并视频
   ff.merge_videos(['1.mp4', '2.mp4'], 'merged.mp4')

7. 提取音频
   ff.extract_audio('video.mp4', 'audio.mp3', codec='mp3', bitrate='192k')

8. 提取帧
   frames = ff.extract_all_frames('video.mp4', 'frames/', fps=1)

9. 调整速度
   ff.change_speed('input.mp4', 'fast.mp4', 2.0)

10. 获取信息
    info = ff.get_video_info('video.mp4')
    print(info['video_resolution'])
""")


if __name__ == "__main__":
    example_check_ffmpeg()
    example_format_conversion()
    example_get_info()
    example_video_editing()
    example_extract_frames()
    example_video_to_gif()
    example_watermark()
    example_merge_videos()
    example_audio_extraction()
    example_subtitle()
    example_image_to_video()
    quick_reference()
