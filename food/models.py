from django.db import models

# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.name