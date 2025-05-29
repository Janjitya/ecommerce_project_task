from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} - {self.price}"
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    product_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','product')

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity} - {self.user.username}"
    
    def total_price(self):
        return self.product_price * self.quantity
    
    def save(self, *args, **kwargs):
        if self.product:
            self.product_price = self.product.price
        
        super().save(*args, **kwargs)
