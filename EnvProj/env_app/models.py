from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class EcoProduct(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    is_eco_friendly = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class EcoTip(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='eco_tips/', null=True, blank=True)  # Now optional

    def __str__(self):
        return self.title


class UserUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page_visited = models.CharField(max_length=200)
    visit_date = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.page_visited}"


class SustainabilityCalculator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    electricity_usage = models.FloatField()
    water_usage = models.FloatField()
    waste_production = models.FloatField()
    transportation_miles = models.FloatField()
    carbon_footprint = models.FloatField()
    calculated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.calculated_at}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('EcoProduct', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    order_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Order #{self.order_id} by {self.user.username}"

# User Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"