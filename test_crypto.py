from app.core.crypto import encrypt, decrypt

original = "1234567890"

encrypted = encrypt(original)
decrypted = decrypt(encrypted)

print("Original:", original)
print("Encrypted:", encrypted)
print("Decrypted:", decrypted)