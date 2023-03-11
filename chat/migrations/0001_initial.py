# Generated by Django 4.1.3 on 2023-02-25 15:13

import chat.utils
from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('chat_type', models.CharField(choices=[('groupe', 'Groupe'), ('private_chat', 'Private Chat')], default='private_chat', max_length=20, verbose_name='chat type')),
                ('name', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('key', models.CharField(blank=True, default=chat.utils.generate_chat_key, max_length=32, null=True)),
                ('members', models.ManyToManyField(related_name='chats', to='accounts.projectuser', verbose_name='members')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='accounts.project', verbose_name='project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('text', django_cryptography.fields.encrypt(models.TextField(blank=True, null=True, verbose_name='text'))),
                ('message_file', models.FileField(upload_to='messages/', verbose_name='file')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.chat', verbose_name='chat')),
                ('replied_on', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='replies', to='chat.message')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='accounts.projectuser', verbose_name='user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
