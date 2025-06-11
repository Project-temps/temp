<<<<<<< HEAD
from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
=======
# authentication/apps.py
from django.apps import AppConfig

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

    def ready(self):
        # لازم است سیگنال‌ها بارگذاری شوند
        import authentication.models  # این خط برای فراخوانی سیگنال‌ها کافی‌ست
>>>>>>> 7576c1d35bb7910344a6ac3a18c4a6d539cb55fd
