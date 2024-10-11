from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.name)

class Category(models.Model):
    options = (
        ('breakfast', 'breakfast'),
        ('lunch', 'lunch'),
        ('dinner', 'dinner'),
        ('snacks', 'snacks'),
    )
    name = models.CharField(max_length=50, choices=options)
    
    def __str__(self):
        return self.name

class Fooditem(models.Model):
    name = models.CharField(max_length=200)
    category = models.ManyToManyField(Category)
    carbohydrate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fats = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    protein = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    calorie = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    
    def __str__(self):
        return str(self.name)

# models.py
MEAL_TYPE_CHOICES = [
    ('breakfast', 'Breakfast'),
    ('lunch', 'Lunch'),
    ('dinner', 'Dinner'),
    ('snacks', 'Snacks'),
]
class UserFooditem(models.Model):
    customer = models.ManyToManyField(Customer, blank=True)
    fooditem = models.ManyToManyField(Fooditem, blank=True)
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPE_CHOICES, default='breakfast')
    date_consumed = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer} - {self.fooditem} ({self.meal_type})"
