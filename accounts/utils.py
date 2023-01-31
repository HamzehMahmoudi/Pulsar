import binascii
import os

def generate_key():
    from accounts.models import AppToken
    key = binascii.hexlify(os.urandom(20)).decode()
    if AppToken.objects.filter(key=key).exists():
        key = generate_key()
    return key