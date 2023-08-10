# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    image=models.CharField(max_length=500000,default="test")
    avalcash=models.IntegerField(default=100000)
    investedcash=models.IntegerField(default=0)
    profit=models.IntegerField(default=0)

    # Add custom fields here, if needed

    def __str__(self):
        return self.username
    
class STOCK(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    stockcode=models.CharField(max_length=100)
    stockname=models.CharField(max_length=200)
    ltp=models.IntegerField(default=1)
    quant=models.IntegerField(default=0)