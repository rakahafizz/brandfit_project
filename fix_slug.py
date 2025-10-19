import os
import django
from django.utils.text import slugify

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brandfit_project.settings")
django.setup()

from orders.models import Product

# Loop semua product
for p in Product.objects.all():
    base_slug = p.slug or slugify(p.name)
    slug = base_slug
    counter = 1
    # Pastikan slug unik
    while Product.objects.filter(slug=slug).exclude(id=p.id).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    p.slug = slug
    p.save()

print("Semua slug sudah unik dan tidak NULL.")
