from django_filters import rest_framework as filters

from .models import Order, OrderProduct


class OrderFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = ['user']


class OrderProductFilter(filters.FilterSet):
    class Meta:
        model = OrderProduct
        fields = ['order']
