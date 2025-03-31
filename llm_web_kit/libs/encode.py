import hashlib


def sha256_hash(data: str) -> str:
    """计算字符串的 SHA-256 哈希值."""
    # 创建 SHA-256 对象
    sha256 = hashlib.sha256()
    # 更新数据（需编码为字节）
    sha256.update(data.encode('utf-8'))
    # 返回十六进制哈希值
    return sha256.hexdigest()
