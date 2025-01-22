from django.shortcuts import render, redirect
from django.contrib import messages  # Додано для повідомлень
from .forms import RegisterForm, LoginByEmailForm
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.decorators import login_required

# Реєстрація користувача
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
                messages.success(request, 'Ви успішно зареєструвалися та увійшли в систему.')  # Повідомлення про успішну реєстрацію
                return redirect('main_page')
    else:
        form = RegisterForm()

    return render(request, 'authentication/registration.html', {'form': form})

# Вхід в систему через email
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

            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Ви успішно увійшли в систему.')  # Повідомлення про успішний вхід
                return redirect('main_page')
            else:
                form.add_error('password', 'Невірний пароль')
    else:
        form = LoginByEmailForm()

    return render(request, 'authentication/login.html', {'form': form})

# Вихід з системи
def logout_view(request):
    logout(request)
    return redirect('main_page')  # Перенаправлення на головну сторінку

# Сторінка користувача

@login_required
def user_profile(request):
    user = request.user  # Отримуємо поточного авторизованого користувача
    return render(request, 'authentication/user_profile.html', {'user': user})

@login_required
def edit_profile(request):
    user = request.user  # Отримуємо поточного користувача

    if request.method == 'POST':
        # Оновлення даних користувача
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.city = request.POST.get('city')
        user.street = request.POST.get('street')
        user.house = request.POST.get('house')
        user.flat = request.POST.get('flat')
        user.phone_number = request.POST.get('phone_number')
        user.age = None if request.POST.get('age') == '' else request.POST.get('age')
        user.save()  # Зберігаємо зміни

        messages.success(request, 'Профіль успішно оновлено.')
        return redirect('user_profile')

    return render(request, 'authentication/edit_profile.html', {'user': user})