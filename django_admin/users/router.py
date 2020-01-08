class Router:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'users':
            return 'users'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'users':
            return 'users'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'default' and app_label != 'users':
            return True
        return False
