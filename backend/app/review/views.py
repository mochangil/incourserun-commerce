from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView
from .models import Review
from .serializers import ReviewSerializer
from .filters import ReviewFilter
from .paginations import ReviewPagination
from ..common.permissions import IsOwner, IsStaff


# Create your views here.
class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = ReviewFilter
    pagination_class = ReviewPagination