# Claude Skills Collection

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub repo](https://img.shields.io/badge/GitHub-publisher--skill%2Fclaude--skill-green?logo=github)](https://github.com/publisher-skill/claude-skill)

这是一个实用的 Python 技能工具集合，包含多个独立的功能模块，可以作为 Claude Code 的自定义 skills 使用，也可以单独导入使用。

## Skill 列表

### 📄 办公文档类 (2个+)

| Skill 名称 | 描述 | 目录 |
|-----------|------|------|
| **PDF Tool** | PDF 文档处理工具（合并、拆分、加密、提取文本等） | [skills/pdf_tool/](./skills/pdf_tool/) |
| **Image Processor** | 图片批量处理工具（压缩、格式转换、加水印等） | [skills/image_processor/](./skills/image_processor/) |

### 🔐 远程工具类 (1个+)

| Skill 名称 | 描述 | 目录 |
|-----------|------|------|
| **SFTP Tool** | SFTP/SSH 远程文件管理工具（上传下载、列表、重命名、执行命令） | [skills/sftp_tool/](./skills/sftp_tool/) |

### 🎬 视频处理类 (1个+)

| Skill 名称 | 描述 | 目录 |
|-----------|------|------|
| **FFmpeg Processor** | FFmpeg 视频/音频处理工具（格式转换、裁剪、合并、水印等） | [skills/ffmpeg_processor/](./skills/ffmpeg_processor/) |

### 📷 图片处理类 (1个+)

| Skill 名称 | 描述 | 目录 |
|-----------|------|------|
| **Image Downloader** | 网站图片批量下载工具（单张图片、HTML页面、全站爬取） | [skills/image_downloader/](./skills/image_downloader/) |

### 📁 文件处理类 (4个)

| Skill 名称 | 描述 | 目录 |
|-----------|------|------|
| **File Organizer** | 按类型、日期、扩展名自动整理文件 | [skills/file_organizer/](./skills/file_organizer/) |
| **Batch Renamer** | 批量重命名文件（正则、序号、前缀等） | [skills/batch_renamer/](./skills/batch_renamer/) |
| **Directory Tree** | 生成目录树，显示文件大小 | [skills/directory_tree/](./skills/directory_tree/) |
| **File Comparator** | 对比文件/目录差异，查找重复文件 | [skills/file_comparator/](./skills/file_comparator/) |

### 📊 数据处理类 (1个+)

| Skill 名称 | 描述 | 目录 |
|-----------|------|------|
| **Data Processor** | CSV/JSON 读写、转换、过滤、合并 | [skills/data_processor/](./skills/data_processor/) |

### 🔒 开发工具类 (1个+)

| Skill 名称 | 描述 | 目录 |
|-----------|------|------|
| **Password Generator** | 密码生成器（安全密码、易记密码、PIN码） | [skills/password_generator/](./skills/password_generator/) |

### 🌐 网络工具类 (2个)

| Skill 名称 | 描述 | 目录 |
|-----------|------|------|
| **Web Crawler** | 基于 requests 和 BeautifulSoup 的网页爬虫工具 | [skills/web_crawler/](./skills/web_crawler/) |
| **PDF-Word Converter** | PDF 与 Word 文档相互转换工具 | [skills/pdf_word_converter/](./skills/pdf_word_converter/) |

## 快速安装（类似 npx 的便捷方式）

### 一键克隆安装

```bash
git clone https://github.com/publisher-skill/claude-skill.git
cd claude-skill
pip install -r requirements.txt
```

### 直接从 GitHub 安装（使用 pipx）

如果你有 `pipx`，可以直接安装并运行：

```bash
# 安装 pipx（如果还没有）
python -m pip install --user pipx
python -m pipx ensurepath

# 使用 pipx 安装（当项目发布到 PyPI 时可用）
# pipx install claude-skills
```

### 使用单个 Skill

每个 skill 可以单独使用，无需安装整个集合：

```bash
# 只下载你需要的 skill（例如 PDF 工具）
git clone --depth 1 https://github.com/publisher-skill/claude-skill.git temp-skills
cd temp-skills/skills/pdf_tool
pip install -r requirements.txt
```

## 常规安装方式

### 安装所有 skills

```bash
git clone https://github.com/publisher-skill/claude-skill.git
cd claude-skill
pip install -r requirements.txt
```

### 单独安装某个 skill

每个 skill 都有自己的 `requirements.txt`，可以单独安装：

```bash
# Web Crawler
cd skills/web_crawler
pip install -r requirements.txt

# PDF Tool
cd skills/pdf_tool
pip install -r requirements.txt

# Image Processor
cd skills/image_processor
pip install -r requirements.txt

# SFTP Tool
cd skills/sftp_tool
pip install -r requirements.txt

# FFmpeg Processor (需要系统安装 FFmpeg)
cd skills/ffmpeg_processor
# 详见 README.md 安装 FFmpeg
```

### 开发模式安装

```bash
pip install -e ".[dev]"
```

## 快速开始

### 运行综合示例

```bash
python example.py
```

### PDF 工具示例

```python
from skills.pdf_tool import PDFTool

pdf = PDFTool()

# 合并多个 PDF
pdf.merge_pdfs(['part1.pdf', 'part2.pdf'], 'complete.pdf')

# 拆分 PDF
pdf.split_pdf('document.pdf', 'output_dir', start=0, end=4)

# 提取文本
text = pdf.extract_text('document.pdf', 'output.txt')

# 加密 PDF
pdf.encrypt_pdf('document.pdf', 'secure.pdf', 'mypassword')
```

### 图片处理示例

```python
from skills.image_processor import ImageProcessor

img = ImageProcessor()

# 压缩图片
img.compress_image('photo.jpg', 'compressed.jpg', quality=70)

# 调整尺寸
img.resize_image('photo.jpg', 'small.jpg', 800, 600)

# 转换格式
img.convert_format('image.png', 'image.jpg', format='JPEG', quality=85)

# 添加水印
img.add_watermark('photo.jpg', 'watermarked.jpg', 'logo.png')

# 批量压缩
success, failed = img.batch_process('original/', 'compressed/', img.compress_image, quality=75)
```

### SFTP 远程管理示例

```python
from skills.sftp_tool import SFTPClient

with SFTPClient('example.com', 22, 'user', password='pass') as sftp:

    # 上传文件
    sftp.upload_file('local.txt', 'remote.txt')

    # 下载文件
    sftp.download_file('remote.txt', 'local.txt')

    # 列出目录
    files = sftp.list_dir('/path')

    # 创建目录
    sftp.mkdir('/new/path')

    # 删除文件
    sftp.delete('/old/file.txt')

    # 执行命令
    code, stdout, stderr = sftp.execute_command('ls -la')
```

### 图片下载示例

```python
from skills.image_downloader import ImageDownloader

dl = ImageDownloader(delay=1.0)

# 从网页下载所有图片
downloaded = dl.download_from_url(
    'https://example.com/gallery',
    'images/gallery/',
    max_images=50
)

# 下载单张图片
dl.download_image(
    'https://example.com/img.jpg',
    'images/img.jpg'
)

# 批量下载 URL 列表
urls = ['https://a.com/1.jpg', 'https://a.com/2.jpg']
dl.download_from_list(urls, 'images/')

# 全站爬取
dl.crawl_and_download(
    'https://example.com',
    'images/site/',
    max_pages=20
)

# 查看摘要
summary = dl.get_summary()
print(f"成功: {summary['downloaded']}")
```

### FFmpeg 视频处理示例

```python
from skills.ffmpeg_processor import FFmpegProcessor

ff = FFmpegProcessor()

# 检查 FFmpeg 是否可用
if not ff.check_ffmpeg():
    print("请先安装 FFmpeg！")
    exit(1)

# 格式转换
ff.to_mp4('input.avi', 'output.mp4')
ff.to_mp3('video.mp4', 'audio.mp3')

# 获取视频信息
info = ff.get_video_info('video.mp4')
print(f"分辨率: {info['video_resolution']}")
print(f"时长: {info['duration']}秒")

# 裁剪视频
ff.trim_video('input.mp4', 'output.mp4', 
              start_time='00:00:10', duration='00:00:30')

# 视频转 GIF
ff.video_to_gif('input.mp4', 'output.gif', fps=15)

# 添加水印
ff.add_watermark('input.mp4', 'output.mp4', 
                'logo.png', position='br')
```

### 文件整理示例

```python
from skills.file_organizer import FileOrganizer

organizer = FileOrganizer()

# 按类型整理下载文件夹
stats = organizer.organize_by_type('~/Downloads')

# 预览整理结果
stats = organizer.organize_by_type('~/Downloads', dry_run=True)
```

### 密码生成示例

```python
from skills.password_generator import PasswordGenerator

gen = PasswordGenerator()

# 生成安全密码
password = gen.generate(length=16)

# 生成易记密码
memorable = gen.generate_memorable(word_count=4)

# 检查强度
result = gen.check_strength(password)
print(f"强度: {result['strength_text']}")
```

### 数据处理示例

```python
from skills.data_processor import DataProcessor

proc = DataProcessor()

# 读取 CSV
data = proc.read_csv('data.csv')

# 过滤数据
filtered = proc.filter_data(data, lambda x: int(x['age']) > 18)

# 格式转换
proc.csv_to_json('data.csv', 'data.json')
```

更多示例请参考各个 skill 目录下的 `example.py` 和 `README.md`。

## 项目结构

```
claude-skill/
├── README.md                          # 本文件
├── __init__.py                        # 包入口
├── pyproject.toml                     # 项目配置
├── requirements.txt                   # 所有依赖
├── example.py                         # 综合示例
├── LICENSE                            # MIT 许可证
├── CONTRIBUTING.md                    # 贡献指南
├── .gitignore                         # Git 忽略文件
├── skills/                            # Claude Code Skills
│   ├── __init__.py
│   │
│   ├── pdf_tool/                      # PDF 工具
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── pdf_tool.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── image_processor/               # 图片处理器
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── image_processor.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── sftp_tool/                     # SFTP 工具
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── sftp_tool.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── image_downloader/               # 图片下载器
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── image_downloader.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── ffmpeg_processor/              # FFmpeg 视频处理
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── ffmpeg_processor.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── file_organizer/               # 文件整理器
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── file_organizer.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── batch_renamer/                 # 批量重命名器
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── batch_renamer.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── directory_tree/                # 目录树生成器
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── directory_tree.py
│   │   ├── example.py
│   │   └ requirements.txt
│   │
│   ├── file_comparator/               # 文件对比工具
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── file_comparator.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── data_processor/                # 数据处理器
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── data_processor.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── password_generator/            # 密码生成器
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── password_generator.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── web_crawler/                  # 网页爬虫
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── web_crawler.py
│   │   ├── example.py
│   │   └ requirements.txt
│   │
│   └── pdf_word_converter/           # PDF-Word 转换
│       ├── __init__.py
│       ├── SKILL.md
│       ├── README.md
│       ├── pdf_word_converter.py
│       ├── converter.py
│       ├── example.py
│       └── requirements.txt
│
└── tests/                            # 测试目录
    ├── __init__.py
    ├── test_web_crawler.py
    └── test_pdf_word_converter.py
```

## 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_web_crawler.py -v

# 显示覆盖率
pytest --cov=skills tests/
```

## 添加新 Skill

想要贡献新的 skill？请查看 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解详细指南。

简要步骤：

1. 在 `skills/` 目录下创建新的子目录
2. 创建必要的文件（`__init__.py`, 主模块, `SKILL.md`, `README.md`, `example.py`, `requirements.txt`）
3. 在 `skills/__init__.py` 中添加新 skill
4. 更新根目录 `README.md` 添加新 skill 说明
5. 提交 Pull Request

## License

MIT License - 详见 [LICENSE](./LICENSE) 文件

## 链接

- GitHub 仓库: https://github.com/publisher-skill/claude-skill
- 问题反馈: https://github.com/publisher-skill/claude-skill/issues
