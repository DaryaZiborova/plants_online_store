from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from content.models import Plant, Supplier, Plant_genus
from orders.models import CartItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def main_page(request):
    plants = Plant.objects.all()  
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
        'username': request.user.username if request.user.is_authenticated else None,  # Додаємо username до контексту
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

    # Передаємо дані у шаблон
    context = {
        'plant': plant,
        'supplier': supplier,
        'genus': genus,
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