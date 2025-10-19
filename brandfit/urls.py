# brandfit/urls.py (contoh)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from orders import views



urlpatterns = [
    path('admin/', admin.site.urls),           # admin harus di atas
    path('', include('orders.urls', namespace='orders')),          # routes app kamu
    path('contact/submit/', views.contact_submit, name='contact_submit'),
]

# hanya tambahkan static serve untuk development — batasi ke media/static path
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
