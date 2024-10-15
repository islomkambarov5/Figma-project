from django.apps import AppConfig


class QurilishAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qurilish_app'

    def ready(self):
        import qurilish_app.signals
