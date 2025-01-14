from django.db import models

class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    contact_details = models.TextField()

class Plant_genus(models.Model):
    plant_genus_id = models.AutoField(primary_key=True)
    genus_name = models.CharField(max_length=50)
    genus_description = models.TextField()

class Plant(models.Model):
    CATEGORY_CHOICES = [
        ('Саджанці плодових дерев і чагарників', 'Саджанці плодових дерев і чагарників'),
        ('Саджанці декоративних чагарників і дерев', 'Саджанці декоративних чагарників і дерев'),
        ('Насіння і цибулини квітів', 'Насіння і цибулини квітів'),
        ('Насіння газонної трави', 'Насіння газонної трави'),
    ]
    plant_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    genus = models.ForeignKey(Plant_genus, on_delete=models.CASCADE, to_field='plant_genus_id') 
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, to_field='supplier_id')
    plant_name = models.CharField(max_length=100)
    plant_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    photo = models.ImageField(null=True, blank=True)  

    def __str__(self):
        return f"{self.plant_name} ({self.plant_id})"
