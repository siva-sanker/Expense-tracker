from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=30)

class Expense(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    price=models.FloatField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

class Balance(models.Model):
    balance=models.FloatField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)