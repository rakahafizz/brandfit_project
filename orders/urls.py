from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.home, name='index'),  # index.html
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('product/<int:pk>/', views.product_detail_by_pk, name='product_detail_pk'),
    path('product/<slug:slug>/order/', views.order_create, name='order_create'),
    path('product/id/<int:pk>/order/', views.order_create_by_pk, name='order_create_pk'),
    path('order/success/', views.order_success, name='order_success'),
]
