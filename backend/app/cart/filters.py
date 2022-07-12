from django_filters import rest_framework as filters
from .models import Cart


class CartFilter(filters.FilterSet):
    class Meta:
        model = Cart
        fields = ['user', 'product']