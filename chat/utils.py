from django.core.files.base import ContentFile
import base64
def get_from_base64(file_data, filename=None):
    # Decode the base64 encoded image
    base = base64.b64decode(file_data)
    file_data = ContentFile(base, name=filename)
    # Create a new Image object
    return file_data