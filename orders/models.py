from django.db import models
from authentication.models import User
from content.models import Plant
from django.utils import timezone 
from datetime import datetime, timedelta

# Create your models here.
    
class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='user_id')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, to_field='plant_id')
    items_quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.items_quantity} {self.plant.plant_name} ({self.user.email}"
    
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='user_id')  # Зв'язок з користувачем
    order_city = models.CharField(max_length=100)  # Місто доставки
    order_street = models.CharField(max_length=100)  # Вулиця доставки
    order_house = models.CharField(max_length=10)  # Будинок доставки
    order_flat = models.CharField(max_length=10)  # Квартира доставки
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Загальна сума замовлення
    discounted_total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_method = models.CharField(max_length=50)  # Спосіб оплати
    promocode = models.CharField(max_length=100, null=True, blank=True)
    discount = models.IntegerField(default=0)
    order_date = models.DateTimeField(default=timezone.now)  # Дата замовлення
    delivery_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    STATUS_CHOICES = [
        ('in_progress', 'В обробці'),
        ('shipped', 'Відправлено'),
        ('delivered', 'Доставлено'),
        ('canceled', 'Скасовано')
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='in_progress'  # За замовчуванням "В обробці"
    )

    def set_delivery_date(self, date):
        if date > self.order_date + timedelta(days=1):
            self.delivery_date = date
        else:
            raise ValueError("Delivery date must be at least one day after the order date.")
    
    def __str__(self):
        return f"Order #{self.order_id} by {self.user.email}"


class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')  # Зв'язок з замовленням
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, to_field='plant_id')  # Зв'язок з товаром
    quantity = models.IntegerField()  # Кількість товару
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Ціна товару на момент замовлення

    def __str__(self):
        return f"{self.quantity} x {self.plant.plant_name} (Order #{self.order.order_id})"
    
class Promocode(models.Model):
    promocode_id = models.AutoField(primary_key=True)
    promocode = models.CharField(max_length=100)
    discount_value = models.IntegerField() 

    def __str__(self):
        return self.promocode