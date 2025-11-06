from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "account"
    label = "app_account"

    def ready(self):
        import account.signals

        return super().ready()
