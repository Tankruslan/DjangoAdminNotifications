import requests
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from notifications.signals import notify
from notifications.models import Notification


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    class Meta:
        app_label = 'users'

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    token = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        app_label = 'users'

    def __str__(self):
        return self.user.user.username


@receiver(post_save, sender=LogEntry)
def write_logs_to_notifications(sender, instance, **kwargs):
    log = LogEntry.objects.first()
    if log:
        user_id = log.user_id
        user = User.objects.get(id=user_id)
        recipients = User.objects.filter(groups__name='SuperAdmin').exclude(id=user.id)
        action_flag = log.action_flag
        if action_flag == 1:
            action = 'added'
        elif action_flag == 2:
            action = 'changed'
        elif action_flag == 3:
            action = 'deleted'
        notify.send(sender=user, recipient=recipients, verb=action,
                    action_object=instance)

        notification = Notification.objects.first()
        data = {
            'id': notification.id,
            'actor': notification.actor.username.capitalize(),
            'verb': notification.verb,
            'action_object': notification.action_object.object_repr,
        }
        # Use 'localhost' if you are out of docker, or 'socket_server' if you are in docker
        requests.post('http://socket_server:8002/get-messages', data=data)


post_save.connect(write_logs_to_notifications, sender=LogEntry)
