from django.shortcuts import render
from django.db.models import Subquery, OuterRef, Avg, Count
from django.db.models.functions import Coalesce
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView
from .models import Review, Photo
from .serializers import ReviewSerializer
from .filters import ReviewFilter
from .paginations import ReviewPagination
from ..common.permissions import IsOwner, IsStaff


# Create your views here.
class ReviewListCreateView(ListCreateAPIView):
    photo_count_subquery = Photo.objects.filter(review=OuterRef('id')).values('review').annotate(cnt=Count('id')).values('cnt')
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = ReviewFilter
    pagination_class = ReviewPagination