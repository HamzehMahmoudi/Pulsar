from django.core.files.base import ContentFile
import base64
import binascii
import os

def get_from_base64(file_data, filename=None):
    # Decode the base64 encoded image
    base = base64.b64decode(file_data)
    file_data = ContentFile(base, name=filename)
    # Create a new Image object
    return file_data


def generate_chat_key():
    from chat.models import Chat
    key = binascii.hexlify(os.urandom(20)).decode()
    try:
        if Chat.objects.filter(key=key).exists():
            key = generate_chat_key()
    except:
        return key[:21]
    return key[:21]
