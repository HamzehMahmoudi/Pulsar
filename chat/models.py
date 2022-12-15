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

    def message_tojson(self):
        return {
            'id': self.id,
            'user': self.user.id,
            'text': self.text,
            'replied_on': self.replied_on.id if self.replied_on else None,
            'created': self.created.isoformat()
        }


class Chat(BaseModel):
    members = models.ManyToManyField("accounts.ProjectUser", verbose_name=_("members"))
    chat_type = models.CharField(_("chat type"), max_length=20, choices=ChatTypes.choices, default=ChatTypes.PV)
    project =  models.ForeignKey("accounts.Project", verbose_name=_("project"), on_delete=models.CASCADE, related_name="chats")

    def messages_to_json(self, num=10):
        res = []
        for msg in self.messages.all()[:num].iterator():
            j = msg.message_tojson()
            res.append(j)
        return res
