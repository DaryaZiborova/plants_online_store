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
from django.contrib.auth import views as auth_views0 
from content import views 
from authentication import views as auth_views
from orders import views as ord_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='main_page'),  # Головна сторінка
    path('plant/<int:plant_id>/', views.plant_detail, name='plant_detail'),  # Сторінка рослин
    path('autocomplete/', views.autocomplete, name='autocomplete'), 
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_by_email, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),  
    path('add-to-cart/<int:plant_id>/<slug:q>', ord_views.add_to_cart, name='add_to_cart'),
    path('cart/', ord_views.cart_view, name='cart'),
    path('user/', auth_views.user_profile, name='user_profile'),  # Сторінка користувача
    path('user/edit/', auth_views.edit_profile, name='edit_profile'),
    path('ordering/', ord_views.ordering_page, name='ordering_page'),  # Сторінка оформлення замовлення
    path('place_order/', ord_views.place_order, name='place_order'),  # Обробка замовлення
    path('orders/', ord_views.orders_view, name='orders'),  # Сторінка "Мої замовлення"
    path('manage-user-rights', views.user_rights, name='user_rights'),
<<<<<<< HEAD
    path('plant/<int:plant_id>/edit', views.update_plant, name='update_plant'),
    path('plant/<int:plant_id>/delete', views.delete_plant, name='delete_plant'),
    path('create-new-plant/', views.create_plant, name='create_plant'),
]
=======
    path('plant/<int:plant_id>/edit', views.edit_plant, name='edit_plant'),
    path('admin-orders/', views.admin_orders, name='admin_orders'),
]
>>>>>>> 7b4768178a3a964adf2c408b7e5952bfd0d3e0f4
