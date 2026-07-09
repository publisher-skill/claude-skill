# FFmpeg Processor Skill

FFmpeg 视频/音频处理工具，提供丰富的媒体处理功能。

## 前置要求

需要安装 FFmpeg：

### Windows
1. 从 https://ffmpeg.org/download.html 下载
2. 解压到 `C:\ffmpeg`
3. 将 `C:\ffmpeg\bin` 添加到系统 PATH

### macOS
```bash
brew install ffmpeg
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install ffmpeg
```

验证安装：
```bash
ffmpeg -version
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

```python
from skills.ffmpeg_processor import FFmpegProcessor

ff = FFmpegProcessor()

# 检查 FFmpeg
if not ff.check_ffmpeg():
    print("FFmpeg 未安装！")
    exit(1)

# 格式转换
ff.to_mp4('input.avi', 'output.mp4')
ff.to_mp3('video.mp4', 'audio.mp3')

# 获取信息
info = ff.get_video_info('video.mp4')
print(f"分辨率: {info['video_resolution']}")
print(f"时长: {info['duration']}秒")
```

## 更多示例

### 裁剪视频
```python
# 从第10秒开始，裁剪30秒
ff.trim_video('input.mp4', 'output.mp4', 
              start_time='00:00:10', duration='00:00:30')

# 或者指定结束时间
ff.trim_video('input.mp4', 'output.mp4',
              start_time='00:00:10', end_time='00:00:40')
```

### 调整尺寸
```python
# 调整为 1080p
ff.resize_video('input.mp4', 'output.mp4', 1920, 1080)

# 调整宽度，保持宽高比
ff.resize_video('input.mp4', 'output.mp4', 1280, -1)
```

### 视频转 GIF
```python
ff.video_to_gif('input.mp4', 'output.gif', 
                fps=10, width=500)
```

### 添加水印
```python
# 右下角水印
ff.add_watermark('input.mp4', 'output.mp4', 
                'logo.png', position='br',
                offset_x=20, offset_y=20)

# 支持的位置: tl, tr, bl, br, c (左上角、右上角、左下角、右下角、中心)
```

### 合并视频
```python
videos = ['part1.mp4', 'part2.mp4', 'part3.mp4']
ff.merge_videos(videos, 'merged.mp4')
```

### 提取帧
```python
# 提取所有帧（每帧一张）
frames = ff.extract_all_frames('video.mp4', 'frames/')

# 每秒提取一帧
frames = ff.extract_all_frames('video.mp4', 'frames/', fps=1)
```

### 调整播放速度
```python
# 2倍速
ff.change_speed('input.mp4', 'fast.mp4', 2.0)

# 0.5倍速（慢放）
ff.change_speed('input.mp4', 'slow.mp4', 0.5)
```

## 运行示例

```bash
cd skills/ffmpeg_processor
python example.py
```
