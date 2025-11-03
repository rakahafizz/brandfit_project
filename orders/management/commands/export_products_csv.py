import csv, os
from django.core.management.base import BaseCommand
from django.conf import settings
from orders.models import Product

class Command(BaseCommand):
    help = 'Export products to CSV (media paths included).'

    def add_arguments(self, parser):
        parser.add_argument('--out', default='products_export.csv')

    def handle(self, *args, **opts):
        out = opts['out']
        path = os.path.join(settings.BASE_DIR, out)
        with open(path, 'w', newline='', encoding='utf-8') as fh:
            writer = csv.writer(fh)
            writer.writerow(['id','name','slug','price','is_featured','image'])
            for p in Product.objects.all():
                writer.writerow([p.pk, p.name, p.slug, p.price or '', p.is_featured, getattr(p.image, 'url', '')])
        self.stdout.write(self.style.SUCCESS(f'Exported to {path}'))
