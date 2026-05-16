from cryptography.fernet import Fernet

SECRET_KEY = Fernet.generate_key()
fernet = Fernet(SECRET_KEY)


def encrypt(text: str) -> str:
    return fernet.encrypt(text.encode()).decode()


def decrypt(text: str) -> str:
    return fernet.decrypt(text.encode()).decode()