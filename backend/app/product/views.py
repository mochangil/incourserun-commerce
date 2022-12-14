from django.shortcuts import render
from django.db.models import Subquery, OuterRef, Avg, Count
from django.db.models.functions import Coalesce
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from .models import Product, Hashtag
from ..review.models import Review
from .serializers import ProductSerializer, HashtagSerializer
from .filters import ProductFilter

# Create your views here.
class ProductListView(ListAPIView):
    avg_rating_subquery = Review.objects.filter(product=OuterRef('id')).values('product').annotate(avg=Avg('rating')).values('avg')
    review_count_subquery = Review.objects.filter(product=OuterRef('id')).values('product').annotate(cnt=Count('id')).values('cnt')
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter

    queryset = Product.objects.annotate(
        avg_rating = Coalesce(Subquery(avg_rating_subquery), 0.0),
        review_count = Coalesce(Subquery(review_count_subquery), 0)
    )
    serializer_class = ProductSerializer


class ProductDetailView(RetrieveAPIView):
    avg_rating_subquery = Review.objects.filter(product=OuterRef('id')).values('product').annotate(avg=Avg('rating')).values('avg')
    review_count_subquery = Review.objects.filter(product=OuterRef('id')).values('product').annotate(cnt=Count('id')).values('cnt')

    queryset = Product.objects.annotate(
        avg_rating = Coalesce(Subquery(avg_rating_subquery), 0.0),
        review_count = Coalesce(Subquery(review_count_subquery), 0)
    )
    serializer_class = ProductSerializer