from django.db.models import Exists, OuterRef
from django.db.models import Prefetch
from django_filters import rest_framework as filters
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from .filters import OrderFilter
from .models import Order, OrderProduct
from .permissions import OrderProductPermission, OrderWebhookPermission
from .serializers import OrderSerializer, OrderProductSerializer, CancelSerializer, OrderPaymentSerializer
from ..common.permissions import IsOwner
from ..review.models import Review

has_review_subquery = Review.objects.filter(order_product=OuterRef('id'))


class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all().prefetch_related(
        Prefetch("order_products", queryset=OrderProduct.objects.annotate(has_review=Exists(has_review_subquery)))
    )
    serializer_class = OrderSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OrderFilter


class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all().prefetch_related(
        Prefetch("order_products", queryset=OrderProduct.objects.annotate(has_review=Exists(has_review_subquery)))
    )
    serializer_class = OrderSerializer
    permission_classes = [IsOwner]


class OrderProductDetailView(RetrieveAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer
    permission_classes = [OrderProductPermission]


class CancelCreateView(CreateAPIView):
    serializer_class = CancelSerializer


class OrderPaymentView(CreateAPIView):
    serializer_class = OrderPaymentSerializer
    permission_classes = [OrderWebhookPermission]
