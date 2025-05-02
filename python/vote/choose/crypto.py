import os
from cryptography.fernet import Fernet

def get_fernet():
    # В веб-процессе MASTER_KEY не задан, при попытке расшифровать упадёт
    key = os.environ.get("MASTER_KEY")
    if not key:
        raise RuntimeError("No MASTER_KEY in env")
    return Fernet(key.encode())

def encrypt_privkey(raw_priv_pem: bytes) -> str:
    return get_fernet().encrypt(raw_priv_pem).decode()

def decrypt_privkey(token: str) -> bytes:
    return get_fernet().decrypt(token.encode())