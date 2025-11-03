from django import forms
from .models import Order, ContactMessage
from django.core.validators import RegexValidator
phone_validator = RegexValidator(r'^[0-9+\-\s()]{6,30}$', 'Nomor telepon tidak valid.')

class OrderForm(forms.ModelForm):
    phone = forms.CharField(required=False, validators=[phone_validator])
    
    class Meta:
        model = Order
        fields = ['name', 'email', 'phone', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nama Anda', 'class': 'input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'input'}),
            'phone': forms.TextInput(attrs={'placeholder': 'No. Telp (opsional)', 'class': 'input'}),
            'notes': forms.Textarea(attrs={'placeholder': 'Tambahkan catatan pesanan...', 'rows':4, 'class': 'input'}),
        }
    def clean_name(self):
        name = self.cleaned_data.get('name','').strip()
        if len(name) < 2:
            raise forms.ValidationError("Nama terlalu pendek.")
        return name


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nama Anda', 'class': 'input', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'input', 'required': True}),
            'message': forms.Textarea(attrs={'placeholder': 'Tulis pesan Anda...', 'rows':4, 'class': 'input', 'required': True}),
        }