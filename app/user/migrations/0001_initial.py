# Generated by Django 5.0.6 on 2024-09-24 21:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.ImageField(default='defaults/user.png', upload_to='')),
                ('question_helper', models.TextField(blank=True, default='Ask me anything !', max_length=200, null=True)),
                ('allow_anonymous_questions', models.BooleanField(default=True)),
                ('blocked', models.ManyToManyField(blank=True, related_name='blocked_users', to=settings.AUTH_USER_MODEL)),
                ('following', models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('silenced', models.ManyToManyField(blank=True, related_name='silenced_users', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
