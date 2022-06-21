from django.shortcuts import render
from django.db.models import Subquery, OuterRef, Avg, Count
from django.db.models.functions import Coalesce
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Product, Hashtag
from ..review.models import Review
from .serializers import ProductSerializer, HashtagSerializer

# Create your views here.
class ProductListCreateView(ListCreateAPIView):
    avg_rating_subquery = Review.objects.filter(product=OuterRef('id')).values('product').annotate(avg=Avg('rating')).values('avg')
    review_count_subquery = Review.objects.filter(product=OuterRef('id')).values('product').annotate(cnt=Count('id')).values('cnt')

    queryset = Product.objects.annotate(
        avg_rating = Coalesce(Subquery(avg_rating_subquery), 0.0),
        review_count = Coalesce(Subquery(review_count_subquery), 0)
    )
    serializer_class = ProductSerializer


class ProductDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    avg_rating_subquery = Review.objects.filter(product=OuterRef('id')).values('product').annotate(avg=Avg('rating')).values('avg')
    review_count_subquery = Review.objects.filter(product=OuterRef('id')).values('product').annotate(cnt=Count('id')).values('cnt')

    queryset = Product.objects.annotate(
        avg_rating = Coalesce(Subquery(avg_rating_subquery), 0.0),
        review_count = Coalesce(Subquery(review_count_subquery), 0)
    )
    serializer_class = ProductSerializer


class HashtagListCreateView(ListCreateAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer


class HashtagDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer