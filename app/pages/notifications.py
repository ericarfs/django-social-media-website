from notifications.models import Notification


def get_notifications_user(user):
    return Notification.objects.filter(recipient = user)

def notifications_count(user):
    return get_notifications_user(user).count()