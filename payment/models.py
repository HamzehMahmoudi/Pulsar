from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.
class Transaction(models.Model):
    tracking_code = models.CharField(verbose_name=_('tracking code'), max_length=20, default='', blank=True)
    project = models.ForeignKey(to='accounts.Project' ,verbose_name=_('project'), null=True, blank=True, on_delete=models.SET_NULL)
    is_paid = models.BooleanField(default=False)
    created = models.DateTimeField(_("created"), default=timezone.now)