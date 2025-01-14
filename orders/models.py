from django.db import models
from authentication.models import User
from content.models import Plant

# Create your models here.
    
class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='user_id')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, to_field='plant_id')
    items_quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.items_quantity} {self.plant.plant_name} ({self.user.email}"