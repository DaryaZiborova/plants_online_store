from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True, blank=True, default="")
    first_name = models.CharField(max_length=255, null=True, blank=True, default="")
    last_name = models.CharField(max_length=255, null=True, blank=True, default="")
    age = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=255, null=False, default="", blank=False)
    street = models.CharField(max_length=255, null=False, default="", blank=False)
    house = models.CharField(max_length=255, null=False, default="", blank=False)
    flat = models.IntegerField(null=False, default="", blank=False)
    username = None
    is_superuser = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'city', 'street', 'house', 'flat']

    def __str__(self):
        return self.email