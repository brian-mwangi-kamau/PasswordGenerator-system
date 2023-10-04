from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta():
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class PasswordGeneratorForm(forms.Form):
    length = forms.IntegerField(
        label="Password Length",
        min_value=8,
        max_value=100,
        initial=12,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    use_lowercase = forms.BooleanField(
        label="Include lowercase letters",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    use_uppercase = forms.BooleanField(
        label="Include uppercase letters",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    use_special_chars = forms.BooleanField(
        label="Include special characters (!@#$%^&*()_-+=<>?/)",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    site = forms.CharField(
        label="Site Name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
