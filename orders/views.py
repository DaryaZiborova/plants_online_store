from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CartItem, Order, OrderItem, Promocode
from content.models import Plant
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
from .documents import generate_pdf_receipt
from django.http import JsonResponse
from django.utils import timezone

# Додавання товару до кошика
def add_to_cart(request, plant_id, q):
    if not request.user.is_authenticated:
        messages.warning(request, 'Будь ласка, увійдіть в аккаунт, щоб додати товар до кошика')
        return redirect(request.META.get('HTTP_REFERER')) 

    q = int(q)
    plant = get_object_or_404(Plant, plant_id=plant_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        plant=plant,
        defaults={"items_quantity": q},
    )

    if not created:
        if q == 0:
            cart_item.delete()
            return redirect(request.META.get('HTTP_REFERER'))
        
        if cart_item.items_quantity > plant.quantity_in_stock:
            if plant.quantity_in_stock == 0:
                cart_item.delete()
            else:
                cart_item.items_quantity = plant.quantity_in_stock
            return redirect(request.META.get('HTTP_REFERER'))
    
        cart_item.items_quantity += q
        if cart_item.items_quantity < 1:  
            cart_item.delete()
        else:
            cart_item.save()
    
    return redirect(request.META.get('HTTP_REFERER'))

# Перегляд кошика
@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    user_cart = [
        {
            "plant": cart_item.plant,
            "quantity": cart_item.items_quantity,
            "total_price": cart_item.items_quantity * cart_item.plant.price
        }
        for cart_item in cart_items
    ]
    total = sum(item["total_price"] for item in user_cart)

    return render(request, 'orders/cart.html', {"cart": user_cart, "total": total})

# Сторінка оформлення замовлення
def ordering_page(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Будь ласка, увійдіть в аккаунт, щоб купити товар')
        referer = request.META.get('HTTP_REFERER') or '/'  
        return redirect(referer)
    plant_id = request.GET.get('plant_id')
    buy_now = request.GET.get('buy_now') == 'true'  # Перевіряємо, чи це "Купити зараз"

    if buy_now and plant_id:
        # Якщо це "Купити зараз", створюємо тимчасовий кошик з одним товаром
        plant = get_object_or_404(Plant, plant_id=plant_id)
        if plant.quantity_in_stock < 1:
            return redirect('main_page')  # Перенаправлення на головну сторінку

        cart_items = [{
            "plant": plant,
            "items_quantity": 1,
            "total_price": plant.price
        }]
        total = plant.price
    else:
        # Якщо це звичайне оформлення замовлення з кошика
        cart_items = CartItem.objects.filter(user=request.user)
        total = sum(item.items_quantity * item.plant.price for item in cart_items)

    return render(request, 'orders/ordering_page.html', {
        'total': total,
        'cart_items': cart_items,
        'buy_now': buy_now,
    })

def download_receipt(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return generate_pdf_receipt(order)

# Підтвердження замовлення
@login_required
def place_order(request):
    if request.method == 'POST':
        # Отримуємо дані з форми
        order_city = request.POST.get('order_city')
        order_street = request.POST.get('order_street')
        order_house = request.POST.get('order_house')
        order_flat = request.POST.get('order_flat')
        payment_method = request.POST.get('payment_method')
        promocode = request.POST.get('promocode')

        PROMOCODES = {promo.promocode: promo.discount_value for promo in Promocode.objects.all()}
        if promocode in PROMOCODES:
            discount = PROMOCODES.get(promocode, 0)
        else:
            promocode = None
            discount = 0
        # Створюємо нове замовлення
        order = Order.objects.create(
            user=request.user,
            order_city=order_city,
            order_street=order_street,
            order_house=order_house,
            order_flat=order_flat,
            payment_method=payment_method,
            promocode=promocode,
            discount=discount,
        )
        # Перевіряємо, чи це "Купити зараз"
        buy_now = request.POST.get('buy_now') == 'true'

        # Якщо це "Купити зараз", отримуємо товар з параметрів запиту
        if buy_now:
            plant_id = request.POST.get('plant_id')
            plant = get_object_or_404(Plant, plant_id=plant_id)

            # Додаємо товар до замовлення
            OrderItem.objects.create(
                order=order,
                plant=plant,
                quantity=1,
                price=plant.price
            )
            order.total_price = plant.price

        # Якщо це звичайне оформлення замовлення з кошика
        else:
            cart_items = CartItem.objects.filter(user=request.user)
            order.total_price = sum(item.items_quantity * item.plant.price for item in cart_items)
            # Додаємо товари до замовлення
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    plant=cart_item.plant,
                    quantity=cart_item.items_quantity,
                    price=cart_item.plant.price * cart_item.items_quantity
                )
            # Очищаємо кошик після оформлення замовлення
            cart_items.delete()
            
        if discount == 0:
            order.discounted_total_price = order.total_price
        else:
            order.discounted_total_price = round(order.total_price * (100-order.discount) / 100, 2)
        order.save()
        messages.success(request, 'Замовлення успішно оформлено!')

        return JsonResponse({"download_url": f"/download_receipt/{order.order_id}/", "redirect_url": "/orders/"})

# Перегляд замовлень
@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'orders/orders.html', {'orders': orders})

@user_passes_test(lambda u: u.is_staff)
def admin_orders(request):
    orders = Order.objects.all().order_by('-order_date', 'user__email')
    orders_by_users = {}

    if request.method == 'POST':
        try:
            order = get_object_or_404(Order, order_id=request.POST.get('order_id'))
            if 'delivery_date' in request.POST:
                delivery_date = request.POST.get('delivery_date')
                delivery_date_parsed = datetime.strptime(delivery_date, "%Y-%m-%d")
                order.delivery_date = delivery_date_parsed
                order.save()
                messages.success(request, "Очікувану дату доставки успiшно встановлено!")
            
            if 'status' in request.POST:
                new_status = request.POST.get('status')
                if new_status == 'shipped':
                    for item in order.items.all():
                        plant = item.plant
                        if plant.quantity_in_stock < item.quantity:
                            messages.error(request, f"Недостатня кількість товару '{plant.plant_name}' на складі.")
                            return redirect('admin_orders')
                        plant.quantity_in_stock -= item.quantity
                        plant.save()
                elif new_status == 'delivered':
                    order.delivery_date = timezone.now()
                elif new_status == 'canceled':
                    order.delivery_date = None  # Очистка даты доставки
                    messages.success(request, "Замовлення скасовано.")
                order.status = new_status
                order.save()
                messages.success(request, "Статус замовлення успішно змінено.")

        except Exception as e:
            messages.error(request, f"Помилка: {str(e)}")
            return redirect('admin_orders')

    # Групуємо замовлення за email користувача
    for order in orders:
        email = order.user.email
        if email not in orders_by_users:
            orders_by_users[email] = []
        orders_by_users[email].append(order)

    # Передаємо дані в шаблон
    context = {
        'orders_by_users': orders_by_users,
    }
    return render(request, 'orders/admin_orders.html', context)

@user_passes_test(lambda u: u.is_staff)
def promocode_management(request):
    if request.method == 'POST':
        promocode = request.POST.get('promocode').strip()
        discount_value = request.POST.get('discount_value')
        if Promocode.objects.filter(promocode=promocode).exists():
            messages.error(request, "Додати не вийшло. Цей промокод вже існує.")
        else:
            Promocode.objects.create(promocode=promocode, discount_value=discount_value)

    promocodes = Promocode.objects.all()
    return render(request, 'orders/promocode_management.html', {"promocodes": promocodes})

@user_passes_test(lambda u: u.is_staff)
def delete_promocode(request):
    id = request.POST.get('promocode_id')
    promo = get_object_or_404(Promocode, pk=id)
    promo.delete()
    return redirect('promocode_management') 