from django import forms
from .models import Order, ContactMessage

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'phone', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nama Anda', 'class': 'input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'input'}),
            'phone': forms.TextInput(attrs={'placeholder': 'No. Telp (opsional)', 'class': 'input'}),
            'notes': forms.Textarea(attrs={'placeholder': 'Tambahkan catatan pesanan...', 'rows':4, 'class': 'input'}),
        }



class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nama Anda', 'class': 'input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'input'}),
            'message': forms.Textarea(attrs={'placeholder': 'Tulis pesan Anda...', 'rows':4, 'class': 'input'}),
        }
