from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer, ProductReview, ContactUs


class CustomerRegistrationForm(UserCreationForm):
    """Form for new user registration."""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter Username'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter Email'
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter Password'
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerLoginForm(AuthenticationForm):
    """Form for user login."""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter Password'
    }))


class CustomerProfileForm(forms.ModelForm):
    """Form for customer shipping/address profile."""
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'mobile', 'zipcode', 'state']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.NumberInput(attrs={'class': 'form-control'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
        }


class ProductReviewForm(forms.ModelForm):
    """Form for submitting a product review."""
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
        widgets = {
            'review': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3, 'placeholder': 'Write your review...'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 1, 'max': 5
            }),
        }


class ContactUsForm(forms.ModelForm):
    """Form for customer contact/inquiry submissions."""
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4, 'placeholder': 'Your Message'
            }),
        }
