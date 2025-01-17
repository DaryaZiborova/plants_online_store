"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views 
from content import views 
from authentication import views as auth_views
from orders import views as ord_views
from authentication.views import edit_profile  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='main_page'),  # Головна сторінка
    path('plant/<int:plant_id>/', views.plant_detail, name='plant_detail'),  # Сторінка рослин
    path('autocomplete/', views.autocomplete, name='autocomplete'), 
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_by_email, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),  # Перенаправлення на головну сторінку
    path('add-to-cart/<int:plant_id>/<slug:q>', ord_views.add_to_cart, name='add_to_cart'),
    path('cart/', ord_views.cart_view, name='cart'),
    path('user/', auth_views.user_profile, name='user_profile'),  # Сторінка користувача
    path('user/edit/', auth_views.edit_profile, name='edit_profile'),
]