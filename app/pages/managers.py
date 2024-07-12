from django.db import models
from user.models import User, Profile

class QuestionManager(models.Manager):
    def get_queryset(self, user):
        requested_user = User.objects.get(username = user)
        profile = Profile.objects.get(user=requested_user)

        questions = super().get_queryset().filter(sent_to = profile, is_answered=False).order_by('-created_at')

        blocked_users = profile.get_blocked_users()

        questions_list = [question for question in questions if question.sent_by.user not in blocked_users]

        return questions_list
