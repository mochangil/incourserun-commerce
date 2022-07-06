from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Cart
from .serializers import CartSerializer
from .filters import CartFilter
from ..common.permissions import IsOwner


class CartListCreateView(ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    # filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CartFilter


class CartDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    # permission_classes = [IsOwner]
