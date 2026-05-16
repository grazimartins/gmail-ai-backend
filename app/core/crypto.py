from cryptography.fernet import Fernet
from app.core.config import SECRET_KEY


fernet = Fernet(SECRET_KEY)


def encrypt(text: str) -> str:
    return fernet.encrypt(text.encode()).decode()


def decrypt(text: str) -> str:
    return fernet.decrypt(text.encode()).decode()