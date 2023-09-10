from django.apps import AppConfig
from .utils import set_popular_zipcode_to_cache


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        set_popular_zipcode_to_cache()
