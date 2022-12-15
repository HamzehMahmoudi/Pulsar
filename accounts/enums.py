from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class UserType(IntegerChoices):
    NORMAL_USER = 1, _("normal user")
    COMPANY_ADMIN = 2, _("company admin")
    
