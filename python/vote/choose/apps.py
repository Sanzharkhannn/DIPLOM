from django.apps import AppConfig


class ChooseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'choose'

    def ready(self):
        # При импорте приложения подключаем наши сигналы
        import choose.signals