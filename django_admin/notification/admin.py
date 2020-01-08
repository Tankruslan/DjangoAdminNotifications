from django.contrib import admin
from .models import NewNotification


class NewNotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'actor',
                    'level', 'action_object', 'unread', 'public')


# admin.site.unregister(Notification)
admin.site.register(NewNotification, NewNotificationAdmin)