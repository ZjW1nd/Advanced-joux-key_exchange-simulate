from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class Signature:
    def __init__(self):
        self.private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())  # 生成随机私钥
        self.public_key = self.private_key.public_key()  # 计算公钥

    def sign(self, message):
        """生成签名"""
        signature = self.private_key.sign(
            message,
            ec.ECDSA(hashes.SHA256())
        )
        return signature

    def verify(self, message, signature):
        """验证签名"""
        try:
            self.public_key.verify(
                signature,
                message,
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except Exception as e:
            return False