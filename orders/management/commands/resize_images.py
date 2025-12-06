import os
from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image

class Command(BaseCommand):
    help = 'Resize product images in MEDIA_ROOT/products/ to max width and create thumbnails.'

    def add_arguments(self, parser):
        parser.add_argument('--max-width', type=int, default=1200)
        parser.add_argument('--thumb-width', type=int, default=400)
        parser.add_argument('--dry-run', action='store_true')

    def handle(self, *args, **options):
        media_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        if not os.path.isdir(media_dir):
            self.stdout.write(self.style.WARNING('No products directory found in media.'))
            return

        for root, _, files in os.walk(media_dir):
            for f in files:
                if not f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    continue
                path = os.path.join(root, f)
                try:
                    img = Image.open(path)     
                    w, h = img.size
                    if w > options['max_width']:
                        newh = int(h * options['max_width'] / w)
                        if not options['dry_run']:
                            img = img.resize((options['max_width'], newh), Image.LANCZOS)
                            img.save(path, optimize=True, quality=85)
                        self.stdout.write(f"Resized {path} -> {options['max_width']}x{newh}")
                    # thumbnail
                    thumb_path = os.path.join(root, 'thumb_' + f)
                    if not os.path.exists(thumb_path):
                        tw = options['thumb_width']
                        th = int(h * tw / w)
                        if not options['dry_run']:
                            thumb = img.copy()
                            thumb.thumbnail((tw, th), Image.LANCZOS)
                            thumb.save(thumb_path, optimize=True, quality=80)
                        self.stdout.write(f"Thumb created {thumb_path}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing {path}: {e}"))

