from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    THEME = (
        ('Light', 'Light'),
        ('Dark', 'Dark')
    )

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    theme = models.CharField(max_length=200, null=True, default='Dark', choices=THEME)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Sandal', 'Sandal'),
        ('Close-Toed Shoe', 'Close-Toed Shoe'),
    )

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='static/images/')

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('In Production', 'In Production'),
        ('Shipping', 'Shipping'),
        ('Delivered', 'Delivered'),
    )

    SIZE = (
        ('5.5', '5.5'),
        ('6', '6'),
        ('6.5', '6.5'),
        ('7', '7'),
        ('7.5', '7.5'),
        ('8', '8'),
        ('8.5', '8.5'),
        ('9', '9'),
        ('9.5', '9.5'),
        ('10', '10'),
        ('10.5', '10.5'),
        ('11', '11'),
        ('11.5', '11.5'),
        ('12', '12'),
        ('12.5', '12.5'),
        ('13', '13'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    size = models.CharField(max_length=200, null=True, choices=SIZE)
    notes = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return self.product.name


