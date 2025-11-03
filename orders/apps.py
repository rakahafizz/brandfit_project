# orders/apps.py
from django.apps import AppConfig

class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    def ready(self):
        # import signals so they get registered when app is ready
        try:
            import orders.signals  # noqa: F401
        except Exception as e:
            # avoid breaking startup if signals fail; log error
            import sys
            print(f"Failed to import orders.signals: {e}", file=sys.stderr)
