from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginByEmailForm
from django.contrib.auth import authenticate, login, logout
from .models import User

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')

            user = form.save(commit=False)
            user.set_password(password)  # Хешування пароля
            user.save()

            user = authenticate(
                request,
                email=form.cleaned_data.get('email'),
                password=password
            )
            if user:
                login(request, user) 
                return redirect('main_page')
    else:
        form = RegisterForm()

    return render(request, 'authentication/registration.html', {'form': form})


def login_by_email(request):
    if request.method == 'POST':
        form = LoginByEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                form.add_error('email', 'Користувача з введеною електронною поштою не існує')
                return render(request, 'authentication/login.html', {'form': form})

            user = authenticate(request, username=user.username, password=password)
            if user:
                login(request, user)
                return redirect('main_page')
            else:
                form.add_error('password', 'Невірний пароль')
    else:
        form = LoginByEmailForm()

    return render(request, 'authentication/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('register')