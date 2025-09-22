import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from argon2 import PasswordHasher

class Encryption:
    @staticmethod
    def key_maker(password: bytes, salt: bytes) -> Fernet:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return Fernet(key)

    @staticmethod
    def encrypt(key: Fernet, data: str) -> str:
        if not data:
            return None
        return key.encrypt(data.encode()).decode()

    @staticmethod
    def decrypt(key: Fernet, data: str) -> str:
        if not data:
            return None
        try:
            return key.decrypt(data.encode()).decode()
        except Exception:
            return None
    @staticmethod
    def hashing(password:str):
        ph = PasswordHasher()
        return ph.hash(password)
    
    @staticmethod
    def authorized(hash:str, password:str|bytes):
        try:
            ph = PasswordHasher()
            return ph.verify(hash=hash, password=password)
        except:
            return False
