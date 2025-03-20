from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=30)

class Expense(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    price=models.FloatField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    created_at=models.DateTimeField(default=now)

class Balance(models.Model):
    balance=models.FloatField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)