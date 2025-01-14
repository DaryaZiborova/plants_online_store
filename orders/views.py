from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import CartItem
from content.models import Plant

# Create your views here.

@login_required
def add_to_cart(request, plant_id, q):
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