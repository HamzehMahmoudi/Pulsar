from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from accounts.manager import CustomUserManager
from django.utils import timezone
from accounts.enums import UserType
from pulsar.models import BaseModel
# import binascii
# import os
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    user_type = models.IntegerField(choices=UserType.choices, default=UserType.NORMAL_USER, null=True, blank=True)
    email = models.EmailField(_("email"), max_length=254, unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        db_table = 'auth_user'


class Project(BaseModel):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=50)
    
    
    
class ProjectUser(BaseModel):
    project = models.ForeignKey("accounts.Project", on_delete=models.CASCADE, related_name='users')
    is_online = models.BooleanField(default=False)


# class AppToken(models.Model):
#     name = models.CharField(max_length=256, null=True, blank=True)
#     key = models.CharField(max_length=256, primary_key=True)
#     project = models.ForeignKey('accounts.Project', on_delete=models.CASCADE, db_index=True)
#     created = models.DateTimeField(auto_now_add=True)
#     expire_on = models.DateTimeField(blank=True, null=True,)

#     class Meta:
#         verbose_name = _("Token")
#         verbose_name_plural = _("Tokens")

#     def save(self, *args, **kwargs):
#         if not self.key:
#             self.key = self.generate_key()
#         s = super().save()
#         return s

#     def generate_key(self):
#         return binascii.hexlify(os.urandom(20)).decode()

#     def __str__(self):
#         return self.name
