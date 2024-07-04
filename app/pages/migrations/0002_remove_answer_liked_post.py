# Generated by Django 5.0.6 on 2024-06-26 13:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='liked',
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('answer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pages.answer')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.profile')),
                ('liked', models.ManyToManyField(blank=True, default=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
