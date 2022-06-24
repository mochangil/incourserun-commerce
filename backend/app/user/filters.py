from django_filters import rest_framework as filters
from .models import User, Cart

class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ['email']

class CartFilter(filters.FilterSet):
    class Meta:
        model = Cart
        fields = ['user', 'product']