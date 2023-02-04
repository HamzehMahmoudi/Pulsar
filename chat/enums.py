from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

class ChatTypes(TextChoices):
    GROUPE = 'groupe', _("Groupe")
    PV = 'private_chat', _("Private Chat")
