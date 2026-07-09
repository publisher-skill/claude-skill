# Password Generator Skill

密码生成器，生成安全密码、易记密码、PIN码，检查密码强度。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

```python
from skills.password_generator import PasswordGenerator

gen = PasswordGenerator()

# 生成默认密码
password = gen.generate()

# 自定义密码
password = gen.generate(length=16, include_symbols=True)

# 检查强度
result = gen.check_strength(password)
print(f"强度: {result['strength_text']}")
```

## 运行示例

```bash
cd skills/password_generator
python example.py
```
