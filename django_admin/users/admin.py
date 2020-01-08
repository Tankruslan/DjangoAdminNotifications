from django.contrib import admin
from loguru import logger
from .models import Profile
from notifications.models import Notification
from notifications.admin import NotificationAdmin


class ProfileAdmin(admin.ModelAdmin):

    @staticmethod
    def is_member(user, group_name):
        return user.groups.filter(name=group_name).exists()

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if self.is_member(request.user, 'Managers'):
            self.readonly_fields = ('token',)
        return super(ProfileAdmin, self).change_view(request, object_id,
                                                     form_url, extra_context)


admin.site.register(Profile, ProfileAdmin)


class NewNotificationAdmin(NotificationAdmin):
    list_display = ('recipient', 'actor',
                    'level', 'action_object', 'unread', 'public')


admin.site.unregister(Notification)
admin.site.register(Notification, NewNotificationAdmin)
