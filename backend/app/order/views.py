from django.http import HttpResponseRedirect
from django.forms import ValidationError
from django.shortcuts import render
from django_filters import rest_framework as filters
from django.db.models import Exists, OuterRef, Prefetch
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, CreateAPIView
from .models import Order, OrderProduct
from ..review.models import Review
from .serializers import OrderSerializer, OrderProductSerializer, CancelSerializer, OrderPaymentSerializer
from .filters import OrderFilter, OrderProductFilter
from ..common.permissions import IsStaff, IsOwner
from .permissions import OrderProductPermission
from django.shortcuts import redirect
from django.db.models import Prefetch
from django.conf import settings
from django.urls import reverse
import requests


has_review_subquery = Review.objects.filter(order_product=OuterRef('id'))

class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all().prefetch_related(
        Prefetch("order_products", queryset = OrderProduct.objects.annotate(has_review = Exists(has_review_subquery)))
    )
    serializer_class = OrderSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OrderFilter
    # permission_classes = [IsStaff]


class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all().prefetch_related(
        Prefetch("order_products", queryset = OrderProduct.objects.annotate(has_review = Exists(has_review_subquery)))
    )
    serializer_class = OrderSerializer
    # permission_classes = [IsOwner]


class OrderProductDetailView(RetrieveAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer
    # permission_classes = [OrderProductPermission]


class CancelCreateView(CreateAPIView):
    serializer_class = CancelSerializer

class OrderPaymentView(CreateAPIView):
    serializer_class = OrderPaymentSerializer

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print("Your ip = ",ip)
    if ip == '127.0.0.1' or ip == '52.78.100.19' or ip == '52.78.48.223':
        return HttpResponseRedirect(reverse('order:order-pay'))
    else:
        raise ValidationError("Unauthorized request ip")