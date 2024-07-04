from .models import Answer, Post
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender = Answer)
def post_save_create_post(sender, instance, created, **kwargs):
    if created:
        Post.objects.create(answer=instance, author = instance.answer_author())