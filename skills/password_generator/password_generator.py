"""
Password Generator Skill
密码生成器
"""

import random
import string
import secrets
from typing import List, Dict, Optional


class PasswordGenerator:
    """密码生成器"""

    def __init__(self):
        """初始化"""
        self.lower = string.ascii_lowercase
        self.upper = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        self.symbols_safe = '!@#$%^&*'

    def generate(self, length: int = 12,
                include_uppercase: bool = True,
                include_lowercase: bool = True,
                include_digits: bool = True,
                include_symbols: bool = True,
                symbols: Optional[str] = None,
                require_all_types: bool = True) -> str:
        """生成密码

        Args:
            length: 密码长度
            include_uppercase: 是否包含大写字母
            include_lowercase: 是否包含小写字母
            include_digits: 是否包含数字
            include_symbols: 是否包含特殊字符
            symbols: 自定义特殊字符
            require_all_types: 是否要求包含所有选中类型

        Returns:
            密码字符串
        """
        if length < 4:
            raise ValueError("密码长度至少为 4")

        chars = ''
        required = []

        if include_lowercase:
            chars += self.lower
            required.append(secrets.choice(self.lower))

        if include_uppercase:
            chars += self.upper
            required.append(secrets.choice(self.upper))

        if include_digits:
            chars += self.digits
            required.append(secrets.choice(self.digits))

        if include_symbols:
            symbol_set = symbols if symbols is not None else self.symbols
            chars += symbol_set
            required.append(secrets.choice(symbol_set))

        if not chars:
            raise ValueError("至少需要选择一种字符类型")

        # 生成剩余字符
        remaining_length = length - len(required)
        remaining = [secrets.choice(chars) for _ in range(remaining_length)]

        # 组合并打乱
        password_chars = required + remaining
        random.shuffle(password_chars)

        password = ''.join(password_chars)

        # 如果要求包含所有类型，验证一下
        if require_all_types and len(required) > 0:
            # 确保每种类型都至少有一个
            has_all = True
            if include_lowercase and not any(c in self.lower for c in password):
                has_all = False
            if include_uppercase and not any(c in self.upper for c in password):
                has_all = False
            if include_digits and not any(c in self.digits for c in password):
                has_all = False
            if include_symbols:
                symbol_set = symbols if symbols is not None else self.symbols
                if not any(c in symbol_set for c in password):
                    has_all = False

            if not has_all:
                # 重试
                return self.generate(length, include_uppercase, include_lowercase,
                                   include_digits, include_symbols, symbols, require_all_types)

        return password

    def generate_multiple(self, count: int, length: int = 12,
                        include_uppercase: bool = True,
                        include_lowercase: bool = True,
                        include_digits: bool = True,
                        include_symbols: bool = True) -> List[str]:
        """生成多个密码

        Args:
            count: 数量
            length: 密码长度
            include_uppercase: 是否包含大写字母
            include_lowercase: 是否包含小写字母
            include_digits: 是否包含数字
            include_symbols: 是否包含特殊字符

        Returns:
            密码列表
        """
        passwords = []
        for _ in range(count):
            password = self.generate(length, include_uppercase, include_lowercase,
                                   include_digits, include_symbols)
            passwords.append(password)
        return passwords

    def generate_pin(self, length: int = 6) -> str:
        """生成 PIN 码（纯数字）

        Args:
            length: PIN 长度

        Returns:
            PIN 字符串
        """
        return self.generate(length, include_uppercase=False, include_lowercase=False,
                            include_digits=True, include_symbols=False)

    def generate_memorable(self, word_count: int = 4,
                         separator: str = '-',
                         capitalize: bool = True) -> str:
        """生成易记密码（单词组合）

        Args:
            word_count: 单词数量
            separator: 分隔符
            capitalize: 是否首字母大写

        Returns:
            易记密码
        """
        # 常用单词列表
        words = [
            'apple', 'beach', 'cloud', 'dance', 'eagle', 'flame', 'grape', 'house',
            'image', 'juice', 'kingdom', 'lemon', 'music', 'nature', 'ocean', 'piano',
            'queen', 'river', 'sunset', 'tree', 'universe', 'valley', 'window', 'yellow',
            'zebra', 'book', 'dream', 'forest', 'garden', 'harbor', 'island', 'jewel',
            'knife', 'light', 'mountain', 'night', 'orange', 'peace', 'quest', 'rainbow',
            'stone', 'torch', 'unity', 'violet', 'whale', 'yacht', 'zero', 'amber',
            'blue', 'coral', 'diamond', 'emerald', 'forest', 'gold', 'heart', 'ivy',
            'jade', 'kite', 'lake', 'moon', 'nova', 'opal', 'pearl', 'quartz', 'ruby'
        ]

        selected_words = []
        for _ in range(word_count):
            word = secrets.choice(words)
            if capitalize:
                word = word.capitalize()
            selected_words.append(word)

        # 添加随机数字
        number = secrets.randbelow(100)

        return separator.join(selected_words) + separator + str(number)

    def check_strength(self, password: str) -> Dict[str, any]:
        """检查密码强度

        Args:
            password: 密码

        Returns:
            强度评分
        """
        score = 0
        feedback = []

        # 长度检查
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1

        # 字符多样性检查
        has_lower = any(c in self.lower for c in password)
        has_upper = any(c in self.upper for c in password)
        has_digits = any(c in self.digits for c in password)
        has_symbols = any(c in self.symbols for c in password)

        if has_lower:
            score += 1
        else:
            feedback.append('建议添加小写字母')

        if has_upper:
            score += 1
        else:
            feedback.append('建议添加大写字母')

        if has_digits:
            score += 1
        else:
            feedback.append('建议添加数字')

        if has_symbols:
            score += 1
        else:
            feedback.append('建议添加特殊字符')

        # 确定强度等级
        if score <= 2:
            strength = 'weak'
            strength_text = '弱'
        elif score <= 4:
            strength = 'medium'
            strength_text = '中等'
        elif score <= 6:
            strength = 'strong'
            strength_text = '强'
        else:
            strength = 'very_strong'
            strength_text = '非常强'

        return {
            'score': score,
            'max_score': 7,
            'strength': strength,
            'strength_text': strength_text,
            'length': len(password),
            'has_lower': has_lower,
            'has_upper': has_upper,
            'has_digits': has_digits,
            'has_symbols': has_symbols,
            'feedback': feedback,
        }

    def generate_passphrase(self, words: Optional[List[str]] = None,
                         length: int = 4,
                         separator: str = ' ',
                         capitalize: bool = False) -> str:
        """生成密码短语

        Args:
            words: 单词列表（可选）
            length: 单词数量
            separator: 分隔符
            capitalize: 是否首字母大写

        Returns:
            密码短语
        """
        if words is None:
            words = [
                'correct', 'horse', 'battery', 'staple', 'apple', 'orange', 'grape',
                'happy', 'sleep', 'tree', 'forest', 'river', 'mountain', 'ocean'
            ]

        selected = [secrets.choice(words) for _ in range(length)]

        if capitalize:
            selected = [word.capitalize() for word in selected]

        return separator.join(selected)


__all__ = ["PasswordGenerator"]
