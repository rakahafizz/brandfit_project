# orders/signals.py
import os
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.management import call_command
from django.conf import settings

from .models import Product

FIXTURES_DIR = os.path.join(settings.BASE_DIR, 'fixtures')
FIXTURES_PATH = os.path.join(FIXTURES_DIR, 'products.json')

def dump_products_fixture():
    """
    Dump all Product instances to fixtures/products.json
    Uses the management command `dumpdata` for correct serialization.
    """
    # ensure fixtures dir exists
    os.makedirs(FIXTURES_DIR, exist_ok=True)

    # call_command returns None, but writes to stdout; we redirect using StringIO
    # simpler approach: call dumpdata and write to file via call_command's stdout capture
    from io import StringIO
    out = StringIO()
    try:
        # Replace 'orders.Product' with '<app_label>.Product' if your app label differs
        call_command('dumpdata', 'orders.Product', indent=2, stdout=out)
        data = out.getvalue()
        # write to file atomically
        tmp_path = FIXTURES_PATH + '.tmp'
        with open(tmp_path, 'w', encoding='utf-8') as f:
            f.write(data)
        os.replace(tmp_path, FIXTURES_PATH)
    except Exception as e:
        # don't raise in signal; log to stderr so it doesn't break normal flow
        import sys
        print(f"[dump_products_fixture] failed: {e}", file=sys.stderr)
    finally:
        out.close()

@receiver(post_save, sender=Product)
def product_saved(sender, instance, **kwargs):
    dump_products_fixture()

@receiver(post_delete, sender=Product)
def product_deleted(sender, instance, **kwargs):
    dump_products_fixture()
