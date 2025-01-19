from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Додано для повідомлень
from django.contrib.auth.decorators import login_required
from .models import CartItem
from content.models import Plant
from .models import Order, OrderItem  # Додано імпорт моделі Order
from .models import CartItem

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
        return redirect('login')  # Перенаправлення на сторінку входу

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

def ordering_page(request):
    # Отримуємо товари з кошика користувача
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.warning(request, 'Ваш кошик порожній!')
        return redirect('cart')  # Перенаправлення на кошик, якщо він порожній

    # Розраховуємо загальну суму замовлення
    total = sum(item.items_quantity * item.plant.price for item in cart_items)

    return render(request, 'orders/ordering_page.html', {'total': total})

def place_order(request):
    if request.method == 'POST':
        # Отримуємо дані з форми
        order_city = request.POST.get('order_city')
        order_street = request.POST.get('order_street')
        order_house = request.POST.get('order_house')
        order_flat = request.POST.get('order_flat')
        payment_method = request.POST.get('payment_method')

        # Отримуємо товари з кошика користувача
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
                price=cart_item.plant.price
            )

        # Очищаємо кошик після оформлення замовлення
        cart_items.delete()

        # Перенаправляємо на сторінку успішного оформлення
        return redirect('orders')

    # Якщо метод не POST, перенаправляємо на кошик
    return redirect('cart')

def orders_view(request):
    # Отримуємо всі замовлення поточного користувача
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'orders/orders.html', {'orders': orders})