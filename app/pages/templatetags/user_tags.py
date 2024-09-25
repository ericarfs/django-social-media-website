from django import template
from notifications.models import Notification
from pages.models import Question

register = template.Library()

def get_notifications_count(user):
    return user.notifications.unread().count()

def get_questions_count(user):
    return len(Question.questions.get_queryset(user = user)) 

register.simple_tag(get_notifications_count) 
register.simple_tag(get_questions_count) 