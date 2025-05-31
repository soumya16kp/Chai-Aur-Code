from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Accounts'

class AccountsConfig(AppConfig):
    name = 'Accounts'

    def ready(self):
        import Accounts.signals