from django.db import models
from user.models import User

class ProfileManager(models.Manager):
    def get(self, user):
        requested_user = User.objects.get(username = user)

        return super().get(user=requested_user) 