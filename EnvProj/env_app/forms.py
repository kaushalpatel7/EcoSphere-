from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserUpload, SustainabilityCalculator
from .models import EcoTip, Profile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserUploadForm(forms.ModelForm):
    class Meta:
        model = UserUpload
        fields = ['title', 'description', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class SustainabilityCalculatorForm(forms.ModelForm):
    class Meta:
        model = SustainabilityCalculator
        fields = ['electricity_usage', 'water_usage', 'waste_production', 'transportation_miles']
        widgets = {
            'electricity_usage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly kWh usage'}),
            'water_usage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly gallons'}),
            'waste_production': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly pounds'}),
            'transportation_miles': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly miles'}),
        }


from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'value': 1}),
        }

# Form for EcoTip creation (with image required)
class EcoTipForm(forms.ModelForm):
    class Meta:
        model = EcoTip
        fields = ['title', 'content', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# Form for Profile photo upload
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
