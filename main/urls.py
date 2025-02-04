
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views0 
from content import views 
from authentication import views as auth_views
from orders import views as ord_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='main_page'),  
    path('plant/<int:plant_id>/', views.plant_detail, name='plant_detail'),  
    path('autocomplete/', views.autocomplete, name='autocomplete'), 
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_by_email, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),  
    path('add-to-cart/<int:plant_id>/<slug:q>', ord_views.add_to_cart, name='add_to_cart'),
    path('cart/', ord_views.cart_view, name='cart'),
    path('user/', auth_views.user_profile, name='user_profile'),  
    path('user/edit/', auth_views.edit_profile, name='edit_profile'),
    path('ordering/', ord_views.ordering_page, name='ordering_page'),  
    path('place_order/', ord_views.place_order, name='place_order'),  
    path('orders/', ord_views.orders_view, name='orders'), 
    path('manage-user-rights', views.user_rights, name='user_rights'),
    path('plant/<int:plant_id>/edit', views.update_plant, name='update_plant'),
    path('plant/<int:plant_id>/delete', views.delete_plant, name='delete_plant'),
    path('create-new-plant/', views.create_plant, name='create_plant'),
    path('plant/<int:plant_id>/edit', views.update_plant, name='edit_plant'),
    path('admin-orders/', ord_views.admin_orders, name='admin_orders'),
    path('download_receipt/<int:order_id>/', ord_views.download_receipt, name='download_receipt'),
    path('download-plant/<int:plant_id>/', views.download_plant_docx, name='download_plant_docx'),
    path('statistics/', views.statistics_view, name='statistics_page'),
]
