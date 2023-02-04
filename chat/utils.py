from django.core.files.base import ContentFile
import base64
import binascii
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def get_from_base64(file_data, filename=None):
    # Decode the base64 encoded image
    base = base64.b64decode(file_data)
    file_data = ContentFile(base, name=filename)
    # Create a new Image object
    return file_data


def generate_chat_key():
    from chat.models import Chat
    key = os.urandom(16)
    key = key.hex()
    try:
        if Chat.objects.filter(key=key).exists():
            key = generate_chat_key()
    except:
        return key
    return key

def encrypt_message(message, key):
    from Crypto.Util.Padding import pad
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES256(key), mode=modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    message = pad(message, 16)
    encrypted_message = encryptor.update(message) + encryptor.finalize()
    enc = iv + encrypted_message
    return enc.hex()

def decrypt_message(encrypted_message, key):
    from Crypto.Util.Padding import unpad
    encrypted_message = bytes.fromhex(encrypted_message)
    iv = encrypted_message[:16]
    encrypted_message = encrypted_message[16:]
    cipher = Cipher(algorithms.AES256(key), mode=modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
    decrypted_message = unpad(decrypted_message, 16)
    return decrypted_message