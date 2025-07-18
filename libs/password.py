import base64
import binascii
import hashlib
import re

"""
这个正则表达式要求密码满足以下条件：
    1. 至少包含一个字母（大小写均可）。
    2. 至少包含一个数字。
    3. 长度至少为 8 个字符。
    4. 可以包含其他任意字符（如特殊符号 !@#$% 等，因为 . 是通用的）
"""
password_pattern = r"^(?=.*[a-zA-Z])(?=.*\d).{8,}$"


def valid_password(password):
    # Define a regex pattern for password rules
    pattern = password_pattern
    # Check if the password matches the pattern
    if re.match(pattern, password) is not None:
        return password

    raise ValueError("Not a valid password.")


def hash_password(password_str, salt_byte):
    dk = hashlib.pbkdf2_hmac("sha256", password_str.encode("utf-8"), salt_byte, 10000)
    return binascii.hexlify(dk)


def compare_password(password_str, password_hashed_base64, salt_base64):
    # compare password for login
    return hash_password(password_str, base64.b64decode(salt_base64)) == base64.b64decode(password_hashed_base64)
