from django import forms
from django.contrib.auth.models import User
from .models import Order

class CheckoutForm(forms.ModelForm):
    payment_method = forms.ChoiceField(
        choices=Order.PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'payment-radio'}),
        initial='COD'
    )

    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address', 'city', 'state', 'postal_code', 'payment_method', 'notes']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john@example.com', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 234 567 890', 'required': True}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123 Main St, Apt 4B', 'required': True}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'New York', 'required': True}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NY', 'required': True}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10001', 'required': True}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Special delivery instructions (optional)', 'rows': 2}),
        }


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Choose a password', 'required': True})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat your password', 'required': True})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address', 'required': True}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data
