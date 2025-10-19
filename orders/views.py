from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from urllib.parse import quote_plus

from .models import Product, Order, ContactMessage
from .forms import OrderForm, ContactForm


def home(request):
    """
    Halaman utama: tampilkan featured_products dan semua products.
    Pastikan model Product punya field is_featured (BooleanField).
    """
    featured_products = Product.objects.filter(is_featured=True)
    products = Product.objects.all()
    return render(request, 'orders/index.html', {
        'featured_products': featured_products,
        'products': products
    })


def product_detail(request, slug):
    """
    Halaman detail produk berdasarkan slug.
    Jika POST, simpan order lalu redirect ke WhatsApp dengan pesan terisi.
    """
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()

            # WA redirect (ganti nomor dengan nomor-mu, tanpa '+')
            wa_number = '6283890458528'  # <-- ganti nomor di sini
            message = (
                f"Halo, saya ingin memesan *{product.name}*.\n\n"
                f"Nama: {order.name}\n"
                f"Email: {order.email}\n"
                f"No HP: {order.phone}\n"
                f"Catatan: {order.notes or '-'}\n\n"
                f"Order ID: {order.pk}"
            )
            wa_url = f"https://wa.me/{wa_number}?text={quote_plus(message)}"

            messages.success(request, "Order tersimpan. Anda akan diarahkan ke WhatsApp untuk konfirmasi.")
            return redirect(wa_url)
        else:
            messages.error(request, "Form tidak valid. Cek kembali isian.")
    else:
        form = OrderForm()

    return render(request, 'orders/product_detail.html', {
        'product': product,
        'form': form
    })


def product_detail_by_pk(request, pk):
    """
    Backward compatibility: bila ada akses via /product/11/,
    redirect ke canonical slug URL.
    """
    product = get_object_or_404(Product, pk=pk)
    return redirect('product_detail', slug=product.slug)


def order_create(request, slug):
    """
    Endpoint alternatif: /product/<slug>/order/
    Perilaku: simpan order lalu redirect ke WA (sama seperti product_detail).
    Jika kamu tidak butuh view terpisah, kamu bisa menghapusnya.
    """
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()

            wa_number = '6283890458528'  # <-- ganti nomor di sini
            message = (
                f"Halo, saya ingin memesan *{product.name}*.\n\n"
                f"Nama: {order.name}\n"
                f"Email: {order.email}\n"
                f"No HP: {order.phone}\n"
                f"Catatan: {order.notes or '-'}\n\n"
                f"Order ID: {order.pk}"
            )
            wa_url = f"https://wa.me/{wa_number}?text={quote_plus(message)}"

            messages.success(request, "Order tersimpan. Anda akan diarahkan ke WhatsApp untuk konfirmasi.")
            return redirect(wa_url)
        else:
            messages.error(request, "Form tidak valid. Cek kembali isian.")
    else:
        form = OrderForm()

    return render(request, 'orders/order_form.html', {
        'product': product,
        'form': form
    })


def order_create_by_pk(request, pk):
    """
    Jika ada endpoint legacy /product/id/<pk>/order/, redirect ke slug-based product page.
    """
    product = get_object_or_404(Product, pk=pk)
    return redirect('product_detail', slug=product.slug)


def order_success(request):
    """
    Halaman sukses opsional (tidak digunakan saat redirect ke WA).
    """
    return render(request, 'orders/order_success.html')


def contact_submit(request):
    """
    Tangani form contact. Simpan ContactMessage via ContactForm.
    Redirect kembali ke home#contact agar user tetap berada di bagian contact.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Jika form adalah ModelForm yang menyimpan ContactMessage, cukup form.save()
            form.save()
            messages.success(request, "Terima kasih — pesan Anda telah diterima.")
        else:
            messages.error(request, "Form tidak valid. Pastikan semua field terisi dengan benar.")
        return redirect(f"{reverse('orders:index')}#contact")
    return redirect('orders:index')