from django import forms
from orders.models import Order

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Отримуємо поточний статус замовлення
        current_status = self.instance.status if self.instance else None
        
        # Якщо статус не "В обробці", прибираємо цей варіант з вибору
        if current_status != 'in_progress':
            self.fields['status'].choices = [
                choice for choice in self.fields['status'].choices 
                if choice[0] != 'in_progress'
            ]