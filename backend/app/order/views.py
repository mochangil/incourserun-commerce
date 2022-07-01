from django.shortcuts import render
from django_filters import rest_framework as filters
from django.db.models import Exists, OuterRef, Prefetch
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Order, OrderProduct
from ..review.models import Review
from .serializers import OrderSerializer
from .filters import OrderFilter, OrderProductFilter

# Create your views here.
class OrderListCreateView(ListCreateAPIView):
    has_review_subquery = Review.objects.filter(order_product=OuterRef('id'))

    queryset = Order.objects.all().prefetch_related(
        Prefetch("order_products", queryset = OrderProduct.objects.annotate(has_review = Exists(has_review_subquery)))
    )
    serializer_class = OrderSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OrderFilter


class OrderDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer