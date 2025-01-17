from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django import forms
from django.core.exceptions import ValidationError
from .models import User

class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторіть пароль...'}),
        label='Повторіть пароль'
    )
    
    class Meta:
        model = User
        fields = ['email', 'username', 'name', 'surname', 'phone_number', 'age', 'city', 'street', 'house', 'flat', 'password']
        labels = {
            'email': 'Електронна пошта',
            'username': "Ім'я користувача",
            'name': "Ім'я",
            'surname': 'Прізвище',
            'phone_number': 'Номер телефону',
            'age': 'Вік',
            'city': 'Місто',
            'street': 'Вулиця',
            'house': 'Будинок',
            'flat': 'Поверх',
            'password': 'Пароль',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введіть електронну пошту...'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Введіть ім'я користувача..."}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Введіть своє ім'я..."}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть своє прізвище...'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть номер телефону...'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введіть свій вік...'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть місто...'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть вулицю...'}),
            'house': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть будинок...'}),
            'flat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть поверх...'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте пароль...'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Користувач із такою електронною поштою вже існує.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            self.add_error('password', 'Паролі не співпадають. Будь ласка, спробуйте ще раз.')
        
        return cleaned_data

class LoginByEmailForm(forms.Form):
    email = forms.EmailField(
        label='Електронна пошта',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введіть електронну пошту...'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть ваш пароль...'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Користувача з введеною електронною поштою не існує.")
        return email