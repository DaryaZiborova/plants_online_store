from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from content.models import Plant, Supplier, Plant_genus

def main_page(request):
    plants = Plant.objects.all()  # Получаем все растения из базы данных
    countries = Supplier.objects.values_list('country', flat=True).distinct()  # Получаем все уникальные страны
    categories = Plant.objects.values_list('category', flat=True).distinct()  # Получаем все уникальные категории

    # Поиск по названию растения
    search_query = request.GET.get('search')
    if search_query:
        print("Search query:", search_query)  # Отладка
        plants = plants.filter(plant_name__icontains=search_query)

    # Фильтрация по цене
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        plants = plants.filter(price__gte=min_price)
    if max_price:
        plants = plants.filter(price__lte=max_price)

    # Фильтрация по странам
    selected_countries = request.GET.getlist('country')
    if selected_countries:
        plants = plants.filter(supplier__country__in=selected_countries)

    # Фильтрация по категориям
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        plants = plants.filter(category__in=selected_categories)

    # Передаем данные в шаблон
    context = {
        'plants': plants,
        'countries': countries,
        'categories': categories,
        'selected_category': request.GET.get('category'),
    }
    
    return render(request, 'content/main_page.html', context)

def plant_detail(request, plant_id):
    # Получаем растение по plant_id или возвращаем 404, если не найдено
    plant = get_object_or_404(Plant, plant_id=plant_id)
    
    # Получаем поставщика и род растения с проверкой на 404
    supplier = get_object_or_404(Supplier, supplier_id=plant.supplier_id)  # Исправлено на supplier_id
    genus = get_object_or_404(Plant_genus, plant_genus_id=plant.genus_id)  # Исправлено на plant_genus_id
    
    # Обработка формы (кнопки "Купити" и "До кошика")
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))  # Получаем количество из формы
        action = request.POST.get('action')  # Получаем действие (купити или до кошика)

        # Проверка, чтобы количество не превышало доступное
        if quantity > plant.quantity_in_stock:
            messages.error(request, "Недостатня кількість товару на складі.")
        else:
            if action == 'buy':
                # Логика для покупки
                messages.success(request, f"Ви придбали {quantity} шт. {plant.plant_name}.")
                return redirect('main_page')
            elif action == 'add_to_cart':
                # Логика для добавления в корзину
                messages.success(request, f"Додано {quantity} шт. {plant.plant_name} до кошика.")
                return redirect('main_page')

    # Передаем данные в шаблон
    context = {
        'plant': plant,
        'supplier': supplier,
        'genus': genus,
    }
    
    return render(request, 'content/plant_detail.html', context)

def autocomplete(request):
    query = request.GET.get('query', '')
    if query:
        plants = Plant.objects.filter(plant_name__icontains=query)[:10]  # Ограничиваем количество результатов
        results = [{'plant_name': plant.plant_name} for plant in plants]
    else:
        results = []
    return JsonResponse(results, safe=False)