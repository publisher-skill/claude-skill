# Claude Skills Collection

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub repo](https://img.shields.io/badge/GitHub-publisher--skill%2Fclaude--skill-green?logo=github)](https://github.com/publisher-skill/claude-skill)

A practical Python skill tool collection containing multiple independent functional modules, usable as Claude Code custom skills or standalone imports.

## Skill List

### 📄 Office Document (2+)

| Skill Name | Description | Directory |
|-----------|------|------|
| **PDF Tool** | PDF document processing tool (merge, split, encrypt, extract text, etc.) | [skills/pdf_tool/](./skills/pdf_tool/) |
| **Image Processor** | Batch image processing tool (compress, convert format, add watermark, etc.) | [skills/image_processor/](./skills/image_processor/) |

### 🔐 Remote Tools (1+)

| Skill Name | Description | Directory |
|-----------|------|------|
| **SFTP Tool** | SFTP/SSH remote file management tool (upload, download, list, rename, execute commands) | [skills/sftp_tool/](./skills/sftp_tool/) |

### 🎬 Video Processing (1+)

| Skill Name | Description | Directory |
|-----------|------|------|
| **FFmpeg Processor** | FFmpeg video/audio processing tool (format conversion, trim, merge, watermark, etc.) | [skills/ffmpeg_processor/](./skills/ffmpeg_processor/) |

### 📷 Image Processing (1+)

| Skill Name | Description | Directory |
|-----------|------|------|
| **Image Downloader** | Website image batch download tool (single image, HTML page, whole site crawl) | [skills/image_downloader/](./skills/image_downloader/) |

### 📁 File Processing (4)

| Skill Name | Description | Directory |
|-----------|------|------|
| **File Organizer** | Auto-organize files by type, date, extension | [skills/file_organizer/](./skills/file_organizer/) |
| **Batch Renamer** | Batch rename files (regex, sequence, prefix, etc.) | [skills/batch_renamer/](./skills/batch_renamer/) |
| **Directory Tree** | Generate directory tree, show file sizes | [skills/directory_tree/](./skills/directory_tree/) |
| **File Comparator** | Compare file/directory differences, find duplicates | [skills/file_comparator/](./skills/file_comparator/) |

### 📊 Data Processing (1+)

| Skill Name | Description | Directory |
|-----------|------|------|
| **Data Processor** | CSV/JSON read/write, convert, filter, merge | [skills/data_processor/](./skills/data_processor/) |

### 🔒 Dev Tools (1+)

| Skill Name | Description | Directory |
|-----------|------|------|
| **Password Generator** | Password generator (secure, memorable, PIN) | [skills/password_generator/](./skills/password_generator/) |

### 🌐 Web Tools (2)

| Skill Name | Description | Directory |
|-----------|------|------|
| **Web Crawler** | Web crawler based on requests and BeautifulSoup | [skills/web_crawler/](./skills/web_crawler/) |
| **PDF-Word Converter** | PDF and Word document conversion tool | [skills/pdf_word_converter/](./skills/pdf_word_converter/) |

## Quick Install (like npx)

### One-click Clone Install

```bash
git clone https://github.com/publisher-skill/claude-skill.git
cd claude-skill
pip install -r requirements.txt
```

### Direct from GitHub (with pipx)

If you have `pipx`, you can install and run directly:

```bash
# Install pipx (if needed)
python -m pip install --user pipx
python -m pipx ensurepath

# Use pipx install (when project is published to PyPI)
# pipx install claude-skills
```

### Use a Single Skill

Each skill can be used independently without installing the whole collection:

```bash
# Download only the skill you need (e.g., PDF Tool)
git clone --depth 1 https://github.com/publisher-skill/claude-skill.git temp-skills
cd temp-skills/skills/pdf_tool
pip install -r requirements.txt
```

## Regular Install

### Install All Skills

```bash
git clone https://github.com/publisher-skill/claude-skill.git
cd claude-skill
pip install -r requirements.txt
```

### Install a Single Skill

Each skill has its own `requirements.txt` for individual install:

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

# FFmpeg Processor (requires system FFmpeg installation)
cd skills/ffmpeg_processor
# See README.md for FFmpeg installation
```

### Development Mode Install

```bash
pip install -e ".[dev]"
```

## Quick Start

### Run the Comprehensive Example

```bash
python example.py
```

### PDF Tool Example

```python
from skills.pdf_tool import PDFTool

pdf = PDFTool()

# Merge multiple PDFs
pdf.merge_pdfs(['part1.pdf', 'part2.pdf'], 'complete.pdf')

# Split PDF
pdf.split_pdf('document.pdf', 'output_dir', start=0, end=4)

# Extract text
text = pdf.extract_text('document.pdf', 'output.txt')

# Encrypt PDF
pdf.encrypt_pdf('document.pdf', 'secure.pdf', 'mypassword')
```

### Image Processing Example

```python
from skills.image_processor import ImageProcessor

img = ImageProcessor()

# Compress image
img.compress_image('photo.jpg', 'compressed.jpg', quality=70)

# Resize image
img.resize_image('photo.jpg', 'small.jpg', 800, 600)

# Convert format
img.convert_format('image.png', 'image.jpg', format='JPEG', quality=85)

# Add watermark
img.add_watermark('photo.jpg', 'watermarked.jpg', 'logo.png')

# Batch compress
success, failed = img.batch_process('original/', 'compressed/', img.compress_image, quality=75)
```

### SFTP Remote Management Example

```python
from skills.sftp_tool import SFTPClient

with SFTPClient('example.com', 22, 'user', password='pass') as sftp:

    # Upload file
    sftp.upload_file('local.txt', 'remote.txt')

    # Download file
    sftp.download_file('remote.txt', 'local.txt')

    # List directory
    files = sftp.list_dir('/path')

    # Create directory
    sftp.mkdir('/new/path')

    # Delete file
    sftp.delete('/old/file.txt')

    # Execute command
    code, stdout, stderr = sftp.execute_command('ls -la')
```

### Image Download Example

```python
from skills.image_downloader import ImageDownloader

dl = ImageDownloader(delay=1.0)

# Download all images from webpage
downloaded = dl.download_from_url(
    'https://example.com/gallery',
    'images/gallery/',
    max_images=50
)

# Download single image
dl.download_image(
    'https://example.com/img.jpg',
    'images/img.jpg'
)

# Batch download URL list
urls = ['https://a.com/1.jpg', 'https://a.com/2.jpg']
dl.download_from_list(urls, 'images/')

# Whole site crawl
dl.crawl_and_download(
    'https://example.com',
    'images/site/',
    max_pages=20
)

# Get summary
summary = dl.get_summary()
print(f"Success: {summary['downloaded']}")
```

### FFmpeg Video Processing Example

```python
from skills.ffmpeg_processor import FFmpegProcessor

ff = FFmpegProcessor()

# Check if FFmpeg is available
if not ff.check_ffmpeg():
    print("Please install FFmpeg first!")
    exit(1)

# Format conversion
ff.to_mp4('input.avi', 'output.mp4')
ff.to_mp3('video.mp4', 'audio.mp3')

# Get video info
info = ff.get_video_info('video.mp4')
print(f"Resolution: {info['video_resolution']}")
print(f"Duration: {info['duration']} seconds")

# Trim video
ff.trim_video('input.mp4', 'output.mp4', 
              start_time='00:00:10', duration='00:00:30')

# Video to GIF
ff.video_to_gif('input.mp4', 'output.gif', fps=15)

# Add watermark
ff.add_watermark('input.mp4', 'output.mp4', 
                'logo.png', position='br')
```

### File Organizer Example

```python
from skills.file_organizer import FileOrganizer

organizer = FileOrganizer()

# Organize download folder by type
stats = organizer.organize_by_type('~/Downloads')

# Preview organization
stats = organizer.organize_by_type('~/Downloads', dry_run=True)
```

### Password Generator Example

```python
from skills.password_generator import PasswordGenerator

gen = PasswordGenerator()

# Generate secure password
password = gen.generate(length=16)

# Generate memorable password
memorable = gen.generate_memorable(word_count=4)

# Check strength
result = gen.check_strength(password)
print(f"Strength: {result['strength_text']}")
```

### Data Processing Example

```python
from skills.data_processor import DataProcessor

proc = DataProcessor()

# Read CSV
data = proc.read_csv('data.csv')

# Filter data
filtered = proc.filter_data(data, lambda x: int(x['age']) > 18)

# Format conversion
proc.csv_to_json('data.csv', 'data.json')
```

More examples available in each skill directory's `example.py` and `README.md`.

## Project Structure

```
claude-skill/
├── README.md                          # This file (Chinese)
├── README_EN.md                       # This file (English)
├── __init__.py                        # Package entry
├── pyproject.toml                     # Project config
├── requirements.txt                   # All dependencies
├── example.py                         # Comprehensive example
├── LICENSE                            # MIT License
├── CONTRIBUTING.md                    # Contribution guide
├── .gitignore                         # Git ignore file
├── skills/                            # Claude Code Skills
│   ├── __init__.py
│   │
│   ├── pdf_tool/                      # PDF Tool
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── pdf_tool.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── image_processor/               # Image Processor
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── image_processor.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── sftp_tool/                     # SFTP Tool
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── sftp_tool.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── image_downloader/              # Image Downloader
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── image_downloader.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── ffmpeg_processor/              # FFmpeg Video Processor
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── ffmpeg_processor.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── file_organizer/               # File Organizer
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── file_organizer.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── batch_renamer/                 # Batch Renamer
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── batch_renamer.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── directory_tree/                # Directory Tree Generator
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── directory_tree.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── file_comparator/               # File Comparator
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── file_comparator.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── data_processor/                # Data Processor
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── data_processor.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── password_generator/            # Password Generator
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── password_generator.py
│   │   ├── example.py
│   │   └── requirements.txt
│   │
│   ├── web_crawler/                  # Web Crawler
│   │   ├── __init__.py
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── web_crawler.py
│   │   ├── example.py
│   │   └ requirements.txt
│   │
│   └── pdf_word_converter/           # PDF-Word Converter
│       ├── __init__.py
│       ├── SKILL.md
│       ├── README.md
│       ├── pdf_word_converter.py
│       ├── converter.py
│       ├── example.py
│       └── requirements.txt
│
└── tests/                            # Test directory
    ├── __init__.py
    ├── test_web_crawler.py
    └── test_pdf_word_converter.py
```

## Run Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_web_crawler.py -v

# Show coverage
pytest --cov=skills tests/
```

## Add New Skills

Want to contribute a new skill? See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guide.

Quick steps:

1. Create a new subdirectory in `skills/`
2. Create required files (`__init__.py`, main module, `SKILL.md`, `README.md`, `example.py`, `requirements.txt`)
3. Add new skill to `skills/__init__.py`
4. Update root `README.md` and `README_EN.md` with new skill info
5. Submit Pull Request

## License

MIT License - see [LICENSE](./LICENSE) file for details.

## Links

- GitHub repo: https://github.com/publisher-skill/claude-skill
- Issues: https://github.com/publisher-skill/claude-skill/issues
