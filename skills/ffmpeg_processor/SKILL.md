---
name: ffmpeg_processor
description: FFmpeg 视频/音频处理工具 - 格式转换、裁剪、合并、水印、字幕、GIF转换等
metadata:
  type: custom
---

# FFmpeg Processor Skill

FFmpeg 视频/音频处理工具，提供丰富的媒体处理功能。

## 功能特性

### 🎥 格式转换
- MP4 / WebM / AVI / MOV / MKV 互转
- 视频转 GIF
- 视频转 MP3 / AAC / WAV / FLAC

### ✂️ 视频编辑
- 裁剪视频
- 调整尺寸
- 调整速度
- 旋转视频
- 提取视频帧

### 📦 视频处理
- 合并多个视频
- 添加水印
- 添加字幕
- 图片合成视频

### 📊 媒体信息
- 获取视频信息
- 获取音频信息
- 获取格式信息

## 使用方法

### Python API

```python
from skills.ffmpeg_processor import FFmpegProcessor

ff = FFmpegProcessor()

# 检查 FFmpeg 是否可用
print(f"FFmpeg 可用: {ff.check_ffmpeg()}")

# 格式转换
ff.to_mp4('input.avi', 'output.mp4')
ff.to_mp3('input.mp4', 'output.mp3')

# 获取媒体信息
info = ff.get_video_info('video.mp4')
print(f"分辨率: {info['video_resolution']}")
print(f"时长: {info['duration']}秒")

# 裁剪视频
ff.trim_video('input.mp4', 'output.mp4', 
              start_time='00:00:10', 
              duration='00:00:30')

# 调整尺寸
ff.resize_video('input.mp4', 'output.mp4', 1280, 720)

# 视频转 GIF
ff.video_to_gif('input.mp4', 'output.gif', fps=15)

# 添加水印
ff.add_watermark('input.mp4', 'output.mp4', 
                'logo.png', position='br')

# 提取帧
frames = ff.extract_all_frames('video.mp4', 'frames/', fps=1)
```

## API 参考

### FFmpegProcessor 类

#### 初始化
```python
FFmpegProcessor(ffmpeg_path='ffmpeg', ffprobe_path='ffprobe')
```

#### 检查与信息
- `check_ffmpeg()` - 检查 FFmpeg 是否可用
- `get_file_info(filepath)` - 获取文件详细信息
- `get_video_info(filepath)` - 获取视频信息
- `get_ffmpeg_version()` - 获取 FFmpeg 版本

#### 格式转换
- `convert_format(input, output, video_codec, audio_codec, ...)` - 通用格式转换
- `to_mp4(input, output, codec)` - 转换为 MP4
- `to_webm(input, output, codec)` - 转换为 WebM
- `to_avi(input, output, codec)` - 转换为 AVI
- `to_mp3(input, output, bitrate)` - 转换为 MP3
- `to_aac(input, output, bitrate)` - 转换为 AAC

#### 视频编辑
- `resize_video(input, output, width, height, keep_aspect_ratio)` - 调整尺寸
- `trim_video(input, output, start_time, duration, end_time)` - 裁剪视频
- `extract_frame(input, output, time)` - 提取单帧
- `extract_all_frames(input, output_dir, format, fps)` - 提取所有帧
- `change_speed(input, output, speed)` - 调整速度
- `rotate_video(input, output, rotation)` - 旋转视频

#### 视频处理
- `video_to_gif(input, output, fps, width)` - 视频转 GIF
- `create_video_from_images(image_dir, output, pattern, fps)` - 从图片创建视频
- `add_watermark(input, output, watermark, position, opacity)` - 添加水印
- `add_subtitle(input, output, subtitle_path)` - 添加字幕
- `merge_videos(file_list, output, use_concat_demuxer)` - 合并视频

#### 音频处理
- `extract_audio(input, output, codec, bitrate)` - 提取音频
