from django.contrib import admin
from .models import Product, ContactMessage
from django.utils.html import format_html

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'name', 'price', 'is_featured')
    list_editable = ('is_featured',)
    search_fields = ('name', 'short_description')
    list_filter = ('price', 'is_featured')

    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:80px; height:50px; object-fit:cover; border-radius:6px;">',
                obj.image.url
            )
        return '-'
    thumb.short_description = 'Gambar'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'handled')
    list_filter = ('handled', 'created_at')
    search_fields = ('name', 'email', 'message')
    actions = ['mark_handled']

    def mark_handled(self, request, queryset):
        queryset.update(handled=True)
        self.message_user(request, f"{queryset.count()} pesan ditandai sebagai handled.")
    mark_handled.short_description = "Tandai pesan sebagai handled"
