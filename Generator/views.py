from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import random
from .models import MyPassword
from django.db.models.signals import post_save
from django.dispatch import receiver
import string
from .forms import PasswordGeneratorForm
from cryptography.fernet import Fernet


# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password!')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})



def encrypt_password(password, key):
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password



def generate_random_password(request, preferences):
    length = preferences['length']
    use_lowercase = preferences['use_lowercase']
    use_uppercase = preferences['use_uppercase']
    use_special_chars = preferences['use_special_chars']

    lowercase_chars = string.ascii_lowercase if use_lowercase else ''
    uppercase_chars = string.ascii_uppercase if use_uppercase else ''
    special_chars = "!@#$%^&*()_-+=<>?/" if use_special_chars else ''

    all_chars = lowercase_chars + uppercase_chars + string.digits + special_chars

    if not (use_lowercase or use_uppercase or use_special_chars):
        raise ValueError("At least one character type must be selected!")

    key = Fernet.generate_key()
    f = Fernet(key)
    
    password = ''.join(random.choice(all_chars) for _ in range(length))

    encrypted_password = f.encrypt(password.encode())

    return encrypted_password, key



def generate_password(request):
    if request.method == 'POST':
        form = PasswordGeneratorForm(request.POST)
        if form.is_valid():
            generated_password, key = generate_random_password(request, form.cleaned_data)

            if request.user.is_active:
                my_password = MyPassword(
                    user = request.user,
                    site = form.cleaned_data['site'],
                    my_password = generated_password,
                    encryption_key=key.decode() ,
                )
                my_password.save()
            return redirect('home')
        
    else:
        form = PasswordGeneratorForm()
    
    return render(request, 'password_generation.html', {'form': form})


def home(request): 
    user = request.user
    my_passwords = MyPassword.objects.filter(user=user)

    for password in my_passwords:
        f = Fernet(password.encryption_key)
        password.my_password = f.decrypt(password.my_password.encode()).decode()

    context = {
        'user': user,
        'my_passwords': my_passwords,
    }
    
    return render(request, 'homepage.html', context)