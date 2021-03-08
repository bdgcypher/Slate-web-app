import django_filters
from django_filters import *
from .models import *

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = '__all__'


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['image']

