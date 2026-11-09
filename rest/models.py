from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(Category, related_name='menu_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    
class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Prepararing', 'Preparing'),
        ('Ready', 'Ready'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} (order #{self.order.id})"