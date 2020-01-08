from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from notifications.models import Notification


@login_required
def mark_block_as_read(request):
    user = request.user
    notifications = user.notifications.unread()[:10]
    [notification.mark_as_read() for notification in notifications]
    new_notifications = user.notifications.unread()[:10]
    json_notifications = [{'id': new_notify.id,
                           'actor': new_notify.actor.username.capitalize(),
                           'verb': new_notify.verb,
                           'action_object': new_notify.action_object.object_repr}
                          for new_notify in new_notifications]
    return JsonResponse({
        'new_notifications': json_notifications,
    })


@login_required
def mark_one_as_read(request):
    notification_id = request.GET.get('notification_id')
    notification = get_object_or_404(
        Notification, recipient=request.user, id=notification_id)
    notification.mark_as_read()

    if request.user.notifications.unread().count() < 10:
        return JsonResponse({
            'new_notification': 0
        })
    else:
        unread_notifications_slice = request.user.notifications.unread()[:9]
        min_notify_id = min([notify.id for notify in unread_notifications_slice])
        new_notification = request.user.notifications.unread().\
            filter(id__lt=min_notify_id).first()
        notification_id = new_notification.id
        actor = new_notification.actor.username.capitalize()
        verb = new_notification.verb.lower()
        action_object = new_notification.action_object.object_repr
        return JsonResponse({
            'new_notification': {'id': notification_id,
                                 'actor': actor,
                                 'verb': verb,
                                 'action_object': action_object,
                                 },
        })
