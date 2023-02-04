# Generated by Django 4.1.3 on 2023-02-04 18:46

import chat.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_chat_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='key',
            field=models.CharField(blank=True, default=chat.utils.generate_chat_key, max_length=32, null=True),
        ),
    ]
