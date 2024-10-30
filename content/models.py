from django.db import models

class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    contact_details = models.TextField()

class Plant_genus(models.Model):
    plant_genus_id = models.AutoField(primary_key=True)
    genus_description = models.TextField()

class Plant(models.Model):
    CATEGORY_CHOICES = [
        ('Саженцы плодовитых деревьев и кустарников', 'Саженцы плодовитых деревьев и кустарников'),
        ('Саженцы декоративных кустарников и деревьев', 'Саженцы декоративных кустарников и деревьев'),
        ('Семена и луковицы цветов', 'Семена и луковицы цветов'),
        ('Семена газонной травы', 'Семена газонной травы'),
    ]
    plant_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    genus_id = models.ForeignKey(Plant_genus, on_delete=models.CASCADE) 
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    plant_name = models.CharField(max_length=100)
    plant_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField()
    photo = models.BinaryField(null=True, blank=True)  

    def __str__(self):
        return f"{self.plant_name} ({self.category_id})"
