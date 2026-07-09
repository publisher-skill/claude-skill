---
name: password_generator
description: 密码生成器 - 生成安全密码、易记密码、PIN码，检查密码强度
metadata:
  type: custom
---

# Password Generator Skill

密码生成器，生成安全密码、易记密码、PIN码，检查密码强度。

## 功能特性

- **安全密码** - 生成高随机度安全密码
- **易记密码** - 单词组合易记密码
- **PIN 码** - 纯数字 PIN 码
- **强度检查** - 检查密码强度
- **批量生成** - 一次生成多个密码

## 使用方法

### Python API

```python
from skills.password_generator import PasswordGenerator

gen = PasswordGenerator()

# 生成默认密码
password = gen.generate()

# 自定义密码
password = gen.generate(length=16, include_symbols=True)

# 生成 PIN 码
pin = gen.generate_pin(6)

# 生成易记密码
memorable = gen.generate_memorable(word_count=4)

# 检查强度
result = gen.check_strength(password)
print(result['strength_text'])
```

## API 参考

### PasswordGenerator 类

#### `generate(length=12, include_uppercase=True, include_lowercase=True, include_digits=True, include_symbols=True, symbols=None, require_all_types=True)`
生成密码

#### `generate_multiple(count, length=12, ...)`
生成多个密码

#### `generate_pin(length=6)`
生成 PIN 码

#### `generate_memorable(word_count=4, separator='-', capitalize=True)`
生成易记密码

#### `generate_passphrase(words=None, length=4, separator=' ', capitalize=False)`
生成密码短语

#### `check_strength(password)`
检查密码强度
