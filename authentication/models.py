from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

# Create your models here.

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    house = models.CharField(max_length=255, null=True, blank=True)
    flat = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'surname']

    def __str__(self):
        return self.email