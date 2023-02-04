from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from accounts.manager import CustomUserManager
from django.utils import timezone
from accounts.enums import UserType
from pulsar.models import BaseModel
from accounts.utils import generate_key
from django.db.models import constraints
from chat.enums import ChatTypes
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
    class Meta:
        constraints = [
            constraints.UniqueConstraint(fields=['user', 'name'], name='unique_project'), 
        ]    


class ProjectUser(BaseModel):
    project = models.ForeignKey("accounts.Project", on_delete=models.CASCADE, related_name='users')
    identifier = models.CharField(max_length=255, verbose_name=_('identifier'))
    is_online = models.BooleanField(default=False)

    class Meta:
        constraints = [
            constraints.UniqueConstraint(fields=['project', 'identifier'], name='unique_project_user'),
        ]
    def get_chats(self):
        return self.chats.all()

    def get_pv_chats(self):
        return self.chats.filter(chat_type=ChatTypes.PV)

    def get_group_chats(self):
        return self.chats.filter(chat_type=ChatTypes.GROUP)

def get_user_pv(self, user_id):
    from chat.models import Chat
    try:
        user = ProjectUser.objects.get(id=user_id)
        chat, created = Chat.objects.get_or_create(project=self.project, chat_type=ChatTypes.PV, project_user=user)
        if created:
            chat.members.add(self, user)
        return chat
    except ProjectUser.DoesNotExist:
        return None


class AppToken(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    key = models.CharField(max_length=256, default=generate_key, blank=True, null=True, unique=True)
    project = models.ForeignKey('accounts.Project', on_delete=models.CASCADE, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    expire_on = models.DateTimeField(blank=True, null=True,)


    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def is_valid(self):
        now = timezone.now()
        return self.expire_on >= now


    def __str__(self):
        return self.name
