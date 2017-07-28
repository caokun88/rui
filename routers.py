# /usr/bin/env python
# coding=utf8


APP_LIST = ['app1', 'app2']  # 对应app的名称
DATABASE_NAME_2 = 'demo'


# settings 中 加入  DATABASE_ROUTERS = ["routers.DatabaseAppsRouter"]


class DatabaseAppsRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label in APP_LIST:
            return 'chipmunk_v2'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label in APP_LIST:
            return 'chipmunk_v2'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label in APP_LIST and \
           obj2._meta.app_label in APP_LIST:
           return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label in APP_LIST or db == DATABASE_NAME_2:
            return False
        return None
