from notifications.models import Notification


class NewNotification(Notification):
    def __unicode__(self):
        super(NewNotification, self).__unicode__()
        ctx = {
            'actor': self.actor,
            'verb': self.verb,
            'action_object': self.action_object.object_repr,
            'target': self.target.object_repr,
            'timesince': self.timesince()
        }
        if self.target:
            if self.action_object:
                return u'%(actor)s %(verb)s %(action_object)s on %(target)s %(timesince)s ago' % ctx
            return u'%(actor)s %(verb)s %(target)s %(timesince)s ago' % ctx
        if self.action_object:
            return u'%(actor)s %(verb)s %(action_object)s %(timesince)s ago' % ctx
        return u'%(actor)s %(verb)s %(timesince)s ago' % ctx
