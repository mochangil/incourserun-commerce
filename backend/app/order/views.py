from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Order, OrderProduct
from .serializers import OrderSerializer, OrderProductSerializer
from .filters import OrderFilter, OrderProductFilter

# Create your views here.
class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OrderFilter


class OrderDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderProductListCreateView(ListCreateAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OrderProductFilter


class OrderProductDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer