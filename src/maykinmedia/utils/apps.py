from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = "maykinmedia.utils"

    def ready(self):
        from . import checks  # noqa
