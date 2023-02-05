from django.test import TestCase
from chat.utils import get_from_base64, generate_chat_key, encrypt_message, decrypt_message

# Create your tests here.

class TestEncryption(TestCase):
    def test_encrypt_data(self):
        message = b"test message"
        key = b"\x00" * 32
        encrypted_message = encrypt_message(message, key)
        self.assertNotEqual(encrypted_message, message)
    def test_decrypt_data(self):
        message = b"test message"
        key = b"\x00" * 32
        encrypted_message = encrypt_message(message, key)
        decrypted_message = decrypt_message(encrypted_message, key)
        self.assertEqual(decrypted_message, message)
    