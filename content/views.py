from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from content.models import Plant, Supplier, Plant_genus
from authentication.models import User
from orders.models import Order, OrderItem
from orders.models import CartItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.core.files.storage import default_storage
from django.db.models import Count, Sum, F


def main_page(request):
    plants = Plant.objects.all().order_by('-plant_id')
    countries = Supplier.objects.values_list('country', flat=True).distinct()  
    categories = Plant.objects.values_list('category', flat=True).distinct() 

    # Пошук за назвою рослини
    search_query = request.GET.get('search')
    if search_query:
        print("Search query:", search_query)  
        plants = plants.filter(plant_name__icontains=search_query)

    # Фільтрація за ціною
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        plants = plants.filter(price__gte=min_price)
    if max_price:
        plants = plants.filter(price__lte=max_price)

    # Фільтрація за країнами
    selected_countries = request.GET.getlist('country')
    if selected_countries:
        plants = plants.filter(supplier__country__in=selected_countries)

    # Фільтрація за категоріями
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        plants = plants.filter(category__in=selected_categories)

    paginator = Paginator(plants, 30)
    page = request.GET.get('p')
    try:
        plants = paginator.page(page)
    except PageNotAnInteger:
        plants = paginator.page(1)
    except EmptyPage:
        plants = paginator.page(paginator.num_pages)

    # Отримуємо елементи кошика для авторизованого користувача
    cart_items_dict = {}
    if request.user.is_authenticated:
        user_cart_items = CartItem.objects.filter(user=request.user).values_list('plant_id', 'items_quantity')
        cart_items_dict = {item[0]: item[1] for item in user_cart_items}

    # Передаємо дані у шаблон
    context = {
        'plants': plants,
        'countries': countries,
        'categories': categories,
        'selected_category': request.GET.get('category'),
        'cart_items': cart_items_dict,
    }
    
    return render(request, 'content/main_page.html', context)

def plant_detail(request, plant_id):
    # Отримуємо рослину за plant_id або повертаємо 404, якщо не знайдено
    plant = get_object_or_404(Plant, plant_id=plant_id)
    
    # Отримуємо постачальника та рід рослини з перевіркою на 404
    supplier = get_object_or_404(Supplier, supplier_id=plant.supplier_id)  
    genus = get_object_or_404(Plant_genus, plant_genus_id=plant.genus_id)  
    
    # Обробка форми (кнопки "Купити" та "До кошика")
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))  # Отримуємо кількість з форми
        action = request.POST.get('action')  # Отримуємо дію (купити або до кошика)

        # Перевірка, щоб кількість не перевищувала доступну
        if quantity > plant.quantity_in_stock:
            messages.error(request, "Недостатня кількість товару на складі.")
        else:
            if action == 'buy':
                # Логіка для покупки
                messages.success(request, f"Ви придбали {quantity} шт. {plant.plant_name}.")
                return redirect('main_page')
            elif action == 'add_to_cart':
                # Логіка для додавання до кошика
                messages.success(request, f"Додано {quantity} шт. {plant.plant_name} до кошика.")
                return redirect('main_page')

    cart_items_dict = {}
    if request.user.is_authenticated:
        user_cart_items = CartItem.objects.filter(user=request.user).values_list('plant_id', 'items_quantity')
        cart_items_dict = {item[0]: item[1] for item in user_cart_items}

    # Передаємо дані у шаблон
    context = {
        'plant': plant,
        'supplier': supplier,
        'genus': genus,
        'cart_items': cart_items_dict,
    }
    
    return render(request, 'content/plant_detail.html', context)

def autocomplete(request):
    query = request.GET.get('query', '')
    if query:
        plants = Plant.objects.filter(plant_name__icontains=query)[:10]  # Обмежуємо кількість результатів
        results = [{'plant_name': plant.plant_name} for plant in plants]
    else:
        results = []
    return JsonResponse(results, safe=False)

@user_passes_test(lambda u: u.is_staff)
def user_rights(request):
    if request.method == 'POST':
        users = User.objects.all()
        for user in users:
            checkbox_name = f"user_{user.user_id}"
            if user != request.user:
                if checkbox_name in request.POST:
                    user.is_staff = True
                else:
                    user.is_staff = False
                user.save()
        messages.success(request, 'Зміни успішно збережено!')
        return redirect('user_rights')

    users = User.objects.all()
    return render(request, 'content/admin_management.html', {'users': users})

@user_passes_test(lambda u: u.is_staff)
def update_plant(request, plant_id):
    plant = get_object_or_404(Plant, plant_id=plant_id)
    
    if request.method == 'POST':
        plant.category = request.POST.get('category')
        plant.genus_id = request.POST.get('genus')  
        plant.supplier_id = request.POST.get('supplier') 
        plant.plant_name = request.POST.get('plant_name')
        plant.plant_description = request.POST.get('plant_description')
        plant.price = request.POST.get('price')
        plant.quantity_in_stock = request.POST.get('quantity_in_stock')
        plant.weight = request.POST.get('weight')

        if request.POST.get('photo_is_deleted') == 'false':
            if 'photo' in request.FILES:
                photo = request.FILES['photo']
                extension = os.path.splitext(photo.name)[1] 
                photo_name = f"{plant.genus_id}_{plant.plant_id}{extension}"
                photo_path = os.path.join('plants', photo_name)
                
                if plant.photo:  
                    if default_storage.exists(f'plants/{plant.photo}'):
                        default_storage.delete(f'plants/{plant.photo}')
                default_storage.save(photo_path, photo)
                plant.photo = photo_name
        else:
            if plant.photo:  
                if default_storage.exists(f'plants/{plant.photo}'):
                    default_storage.delete(f'plants/{plant.photo}')
            plant.photo = None

        plant.save()
        return redirect('plant_detail', plant_id=plant_id)
    context = {
               'plant': plant,
               'genuses': Plant_genus.objects.all(),
               'suppliers': Supplier.objects.all(),
               }
    return render(request, 'content/edit_plant.html', context)

@user_passes_test(lambda u: u.is_staff)
def create_plant(request):
    if request.method == 'POST':
        plant = Plant()
        plant.category = request.POST.get('category')
        plant.genus_id = request.POST.get('genus')
        plant.supplier_id = request.POST.get('supplier')
        plant.plant_name = request.POST.get('plant_name')
        plant.plant_description = request.POST.get('plant_description')
        plant.price = request.POST.get('price')
        plant.quantity_in_stock = request.POST.get('quantity_in_stock')
        plant.weight = request.POST.get('weight')

        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            extension = os.path.splitext(photo.name)[1]
            photo_name = f"{plant.genus_id}_{plant.plant_id}{extension}"
            photo_path = os.path.join('plants', photo_name)
            default_storage.save(photo_path, photo)
            plant.photo = photo_name

        plant.save()
        return redirect('plant_detail', plant_id=plant.plant_id) 

    context = {
        'genuses': Plant_genus.objects.all(),
        'suppliers': Supplier.objects.all(),
        'categories': Plant.CATEGORY_CHOICES,
    }
    return render(request, 'content/create_plant.html', context)

@user_passes_test(lambda u: u.is_staff)
def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, plant_id=plant_id)
    if request.method == 'POST':
        if plant.photo:  
            photo_path = f'plants/{plant.photo}'
            if default_storage.exists(photo_path):
                default_storage.delete(photo_path)

        plant.delete()
        messages.success(request, f"Рослину '{plant.plant_name}' успішно видалено.")
        return redirect('main_page')

from .info_docx import generate_docx

def download_plant_docx(request, plant_id):
    plant = get_object_or_404(Plant, plant_id=plant_id)
    return generate_docx(plant)

@user_passes_test(lambda u: u.is_staff)
def statistics_view(request):
    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_revenue = round(Order.objects.filter(status__in=['delivered', 'shipped']).aggregate(Sum('discounted_total_price'))['discounted_total_price__sum'], 2) or 0
    canceled_orders = Order.objects.filter(status='canceled').count() 

    category_stats = (
        OrderItem.objects
        .values(category=F('plant__category'))  
        .annotate(total_sold=Sum('quantity'))  
        .order_by('-total_sold')  
    )

    supplier_ranking = (
    Supplier.objects
    .annotate(total_plants=Count('plant'))  
    .order_by('-total_plants')  
    )

    total_sold_items = sum(item['total_sold'] for item in category_stats)

    
    for category in category_stats:
        category['percentage'] = round((category['total_sold'] / total_sold_items) * 100, 2) if total_sold_items > 0 else 0

    context = {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'canceled_orders': canceled_orders,
        'category_stats': category_stats,
        'supplier_ranking': supplier_ranking,
    }

    return render(request, 'content/statistics.html', context)