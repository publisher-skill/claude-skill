# File Organizer Skill

文件整理器，可以按类型、日期、扩展名自动整理文件夹中的文件。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

```python
from skills.file_organizer import FileOrganizer

organizer = FileOrganizer()

# 按类型整理下载文件夹
stats = organizer.organize_by_type('~/Downloads')
print(stats)

# 预览整理结果（不实际移动）
stats = organizer.organize_by_type('~/Downloads', dry_run=True)

# 获取操作摘要
summary = organizer.get_summary()
print(f"移动了 {summary['moved']} 个文件")
```

## 支持的文件类型

- 图片 - jpg, jpeg, png, gif, bmp, webp, svg, ico
- 文档 - pdf, doc, docx, txt, rtf, odt, xls, xlsx, ppt, pptx
- 视频 - mp4, avi, mov, wmv, mkv, flv, webm
- 音频 - mp3, wav, flac, aac, ogg, wma, m4a
- 压缩包 - zip, rar, 7z, tar, gz, bz2
- 代码 - py, js, html, css, java, cpp, c, h, go, rs, ts, json, yaml, yml, xml
- 可执行 - exe, msi, dmg, app, deb, rpm

## 运行示例

```bash
cd skills/file_organizer
python example.py
```
