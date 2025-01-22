from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CartItem, Order, OrderItem
from content.models import Plant

# Додавання товару до кошика
def add_to_cart(request, plant_id, q):
    if not request.user.is_authenticated:
        messages.warning(request, 'Будь ласка, увійдіть в аккаунт, щоб додати товар до кошика.')
        return redirect(request.META.get('HTTP_REFERER')) 

    q = int(q)
    plant = get_object_or_404(Plant, plant_id=plant_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        plant=plant,
        defaults={"items_quantity": q},
    )

    if q > 0:
        if cart_item.items_quantity > plant.quantity_in_stock:
            cart_item.items_quantity = plant.quantity_in_stock
            return redirect(request.META.get('HTTP_REFERER'))
        
        if cart_item.items_quantity == plant.quantity_in_stock:
            return redirect(request.META.get('HTTP_REFERER'))
    if q == 0:
        cart_item.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    
    if not created:
        cart_item.items_quantity += q
        if cart_item.items_quantity < 1:  
            cart_item.delete()
        else:
            cart_item.save()

    return redirect(request.META.get('HTTP_REFERER'))

# Перегляд кошика
def cart_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Будь ласка, увійдіть в аккаунт, щоб переглянути кошик.')
        referer = request.META.get('HTTP_REFERER') or '/'  
        return redirect(referer)

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
        messages.warning(request, 'Будь ласка, увійдіть в аккаунт, щоб купити.')
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
        if not cart_items:
            messages.warning(request, 'Ваш кошик порожній!')
            return redirect('cart')  # Перенаправлення на кошик, якщо він порожній
        total = sum(item.items_quantity * item.plant.price for item in cart_items)

    return render(request, 'orders/ordering_page.html', {
        'total': total,
        'cart_items': cart_items,
        'buy_now': buy_now,
    })

# Підтвердження замовлення
def place_order(request):
    if request.method == 'POST':
        # Отримуємо дані з форми
        order_city = request.POST.get('order_city')
        order_street = request.POST.get('order_street')
        order_house = request.POST.get('order_house')
        order_flat = request.POST.get('order_flat')
        payment_method = request.POST.get('payment_method')

        # Перевіряємо, чи це "Купити зараз"
        buy_now = request.POST.get('buy_now') == 'true'

        if buy_now:
            # Якщо це "Купити зараз", отримуємо товар з параметрів запиту
            plant_id = request.POST.get('plant_id')
            plant = get_object_or_404(Plant, plant_id=plant_id)

            # Створюємо нове замовлення
            order = Order.objects.create(
                user=request.user,
                order_city=order_city,
                order_street=order_street,
                order_house=order_house,
                order_flat=order_flat,
                total_price=plant.price,
                payment_method=payment_method
            )

            # Додаємо товар до замовлення
            OrderItem.objects.create(
                order=order,
                plant=plant,
                quantity=1,
                price=plant.price
            )

            # Зменшуємо кількість товару на складі
            plant.quantity_in_stock -= 1
            plant.save()

            messages.success(request, 'Замовлення успішно оформлено!')
            return redirect('orders')  # Перенаправлення на сторінку замовлень

        else:
            # Якщо це звичайне оформлення замовлення з кошика
            cart_items = CartItem.objects.filter(user=request.user)
            if not cart_items:
                messages.warning(request, 'Ваш кошик порожній!')
                return redirect('cart')

            # Розраховуємо загальну суму замовлення
            total_price = sum(item.items_quantity * item.plant.price for item in cart_items)

            # Створюємо нове замовлення
            order = Order.objects.create(
                user=request.user,
                order_city=order_city,
                order_street=order_street,
                order_house=order_house,
                order_flat=order_flat,
                total_price=total_price,
                payment_method=payment_method
            )

            # Додаємо товари до замовлення
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    plant=cart_item.plant,
                    quantity=cart_item.items_quantity,
                    price=cart_item.plant.price * cart_item.items_quantity
                )

                # Зменшуємо кількість товару на складі
                cart_item.plant.quantity_in_stock -= cart_item.items_quantity
                cart_item.plant.save()

            # Очищаємо кошик після оформлення замовлення
            cart_items.delete()

            messages.success(request, 'Замовлення успішно оформлено!')
            return redirect('orders')

    # Якщо метод не POST, перенаправляємо на кошик
    return redirect('cart')

# Перегляд замовлень
@login_required
def orders_view(request):
    # Отримуємо всі замовлення поточного користувача
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'orders/orders.html', {'orders': orders})