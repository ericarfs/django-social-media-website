# Generated by Django 5.0.6 on 2024-07-11 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_alter_answer_body_alter_question_body'),
        ('user', '0003_profile_question_helper_profile_silenced'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='liked',
            field=models.ManyToManyField(blank=True, default=None, related_name='post_likes', to='user.profile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='shared',
            field=models.ManyToManyField(blank=True, default=None, related_name='post_shares', to='user.profile'),
        ),
    ]
