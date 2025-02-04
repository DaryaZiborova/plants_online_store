from django.contrib import admin


from .models import Plant, Plant_genus, Supplier

admin.site.register(Plant)
admin.site.register(Plant_genus)
admin.site.register(Supplier)