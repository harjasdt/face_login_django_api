# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    faceid=models.CharField(max_length=500000)

    # Add custom fields here, if needed

    def __str__(self):
        return self.username