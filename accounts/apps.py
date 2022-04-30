from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = "Accounts/Users"

    def ready(self):
        import accounts.signals
