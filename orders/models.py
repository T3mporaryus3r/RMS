# orders/models.py
from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    items = models.TextField()
    total_amount = models.FloatField()
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
