from django.apps import AppConfig
from django.db.models.signals import post_delete
from gdpr_assist.handlers import handle_post_delete


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        post_delete.disconnect(handle_post_delete)