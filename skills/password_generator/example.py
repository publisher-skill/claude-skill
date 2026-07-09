"""
Password Generator Skill 使用示例
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from skills.password_generator import PasswordGenerator


def example_basic_password():
    """基础密码生成示例"""
    print("="*60)
    print("示例1: 基础密码生成")
    print("="*60)

    gen = PasswordGenerator()

    print("\n默认密码 (12位，包含所有字符类型):")
    for _ in range(3):
        password = gen.generate()
        strength = gen.check_strength(password)
        print(f"  {password:20} ({strength['strength_text']})")


def example_custom_password():
    """自定义密码示例"""
    print("\n" + "="*60)
    print("示例2: 自定义密码")
    print("="*60)

    gen = PasswordGenerator()

    print("\n16位密码:")
    password = gen.generate(length=16)
    strength = gen.check_strength(password)
    print(f"  {password} ({strength['strength_text']})")

    print("\n不含特殊字符:")
    password = gen.generate(length=12, include_symbols=False)
    strength = gen.check_strength(password)
    print(f"  {password} ({strength['strength_text']})")

    print("\n仅小写字母和数字:")
    password = gen.generate(length=12, include_uppercase=False, include_symbols=False)
    strength = gen.check_strength(password)
    print(f"  {password} ({strength['strength_text']})")


def example_pin_code():
    """PIN 码示例"""
    print("\n" + "="*60)
    print("示例3: PIN 码")
    print("="*60)

    gen = PasswordGenerator()

    print("\n6位 PIN 码:")
    for _ in range(3):
        pin = gen.generate_pin(6)
        print(f"  {pin}")

    print("\n4位 PIN 码:")
    for _ in range(3):
        pin = gen.generate_pin(4)
        print(f"  {pin}")


def example_memorable_password():
    """易记密码示例"""
    print("\n" + "="*60)
    print("示例4: 易记密码")
    print("="*60)

    gen = PasswordGenerator()

    print("\n4单词易记密码:")
    for _ in range(3):
        password = gen.generate_memorable(word_count=4, separator='-')
        strength = gen.check_strength(password)
        print(f"  {password:30} ({strength['strength_text']})")

    print("\n5单词易记密码:")
    for _ in range(3):
        password = gen.generate_memorable(word_count=5, separator='_', capitalize=True)
        strength = gen.check_strength(password)
        print(f"  {password:40} ({strength['strength_text']})")


def example_passphrase():
    """密码短语示例"""
    print("\n" + "="*60)
    print("示例5: 密码短语")
    print("="*60)

    gen = PasswordGenerator()

    print("\n密码短语:")
    for _ in range(3):
        password = gen.generate_passphrase(length=4, separator=' ')
        strength = gen.check_strength(password)
        print(f"  \"{password}\"")


def example_multiple_passwords():
    """批量生成示例"""
    print("\n" + "="*60)
    print("示例6: 批量生成密码")
    print("="*60)

    gen = PasswordGenerator()

    print("\n批量生成5个14位密码:")
    passwords = gen.generate_multiple(5, length=14)
    for i, password in enumerate(passwords, 1):
        strength = gen.check_strength(password)
        print(f"  {i}. {password:20} ({strength['strength_text']})")


def example_strength_check():
    """强度检查示例"""
    print("\n" + "="*60)
    print("示例7: 密码强度检查")
    print("="*60)

    gen = PasswordGenerator()

    test_passwords = [
        '123456',
        'password',
        'Password123',
        'P@ssw0rd!2024',
        'Blue-Rain-Sunset-42',
    ]

    for password in test_passwords:
        result = gen.check_strength(password)
        print(f"\n  密码: {password}")
        print(f"  长度: {result['length']}")
        print(f"  评分: {result['score']}/{result['max_score']}")
        print(f"  强度: {result['strength_text']}")
        print(f"  大写: {'✓' if result['has_upper'] else '✗'}")
        print(f"  小写: {'✓' if result['has_lower'] else '✗'}")
        print(f"  数字: {'✓' if result['has_digits'] else '✗'}")
        print(f"  符号: {'✓' if result['has_symbols'] else '✗'}")
        if result['feedback']:
            print(f"  建议: {', '.join(result['feedback'])}")


if __name__ == "__main__":
    example_basic_password()
    example_custom_password()
    example_pin_code()
    example_memorable_password()
    example_passphrase()
    example_multiple_passwords()
    example_strength_check()
