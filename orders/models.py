from django.db import models
from django.utils.text import slugify

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    short_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    # tambahkan field ini:
    is_featured = models.BooleanField(default=False, help_text="Centang jika produk ini tampil di section Produk Unggulan")

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or 'product'
            slug = base
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders', verbose_name="Produk")
    name = models.CharField(max_length=200, verbose_name="Nama Pemesan")
    email = models.EmailField(verbose_name="Email Pemesan")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Nomor Telepon")
    notes = models.TextField(blank=True, verbose_name="Catatan Tambahan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Tanggal Pesanan")

    class Meta:
        verbose_name = "Pesanan"
        verbose_name_plural = "Pesanan"

    def __str__(self):
        return f"Order #{self.id} - {self.product.name} oleh {self.name}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120, verbose_name="Nama Pengirim")
    email = models.EmailField(verbose_name="Email Pengirim")
    message = models.TextField(verbose_name="Pesan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Tanggal Dikirim")
    handled = models.BooleanField(default=False, verbose_name="Sudah Ditangani")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Pesan Kontak"
        verbose_name_plural = "Pesan Kontak"

    def __str__(self):
        return f"{self.name} — {self.email}"
