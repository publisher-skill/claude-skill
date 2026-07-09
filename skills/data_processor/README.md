# Data Processor Skill

数据处理器，CSV/JSON 读写、转换、过滤、合并等。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

```python
from skills.data_processor import DataProcessor

proc = DataProcessor()

# 读取 CSV
data = proc.read_csv('data.csv')

# 过滤数据
filtered = proc.filter_data(data, lambda x: int(x['age']) > 18)

# 写入文件
proc.write_csv(filtered, 'output.csv')

# 格式转换
proc.csv_to_json('data.csv', 'data.json')
```

## 运行示例

```bash
cd skills/data_processor
python example.py
```
