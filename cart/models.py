from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Cart(models.Model):
    # Basic fields (these already exist)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    
    # New fields - make them optional first
    user_session = models.CharField(max_length=40, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item_type = models.CharField(max_length=10, choices=[('food', 'Food'), ('drink', 'Drink')], blank=True, null=True)
    item_id = models.IntegerField(null=True, blank=True)  # Make it nullable first
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} (x{self.quantity})"