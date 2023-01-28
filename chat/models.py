from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from chat.enums import ChatTypes
from pulsar.models import BaseModel
# Create your models here.


class Message(BaseModel):
    user = models.ForeignKey("accounts.ProjectUser", verbose_name=_("user"), on_delete=models.CASCADE, related_name="messages")
    text = models.TextField(_("text"), null=True, blank=True)
    chat = models.ForeignKey("chat.Chat", verbose_name=_("chat"), on_delete=models.CASCADE, related_name="messages")
    message_file = models.FileField(_("file"), upload_to='messages/', max_length=100)
    replied_on = models.ForeignKey('chat.Message', on_delete=models.SET_NULL, related_name="replies", null=True, blank=True)

    def message_tojson(self, host=None):
        file_url = self.message_file.url if self.message_file else None
        if host is not None and file_url is not None:
            file_url = host + file_url
            
        return {
            'id': self.id,
            'user': self.user.identifier,
            'text': self.text,
            'replied_on': self.replied_on.id if self.replied_on else None,
            'message_file': file_url,
            'created': self.created.isoformat()
        }


class Chat(BaseModel):
    members = models.ManyToManyField("accounts.ProjectUser", verbose_name=_("members"), related_name='chats')
    chat_type = models.CharField(_("chat type"), max_length=20, choices=ChatTypes.choices, default=ChatTypes.PV)
    project =  models.ForeignKey("accounts.Project", verbose_name=_("project"), on_delete=models.CASCADE, related_name="chats")
    name = models.CharField(max_length=256 ,null=True, blank=True, default=None)

    def messages_to_json(self, num=10, host=None):
        res = []
        for msg in self.messages.all()[:num].iterator():
            file_url = self.message_file.url if self.message_file else None
            if file_url is not None:
                try:
                    file_url = host + file_url
                except:
                    continue
            j = msg.message_tojson(host=host)
            res.append(j)
        return res
