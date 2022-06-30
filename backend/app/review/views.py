from django.shortcuts import render
from django.db.models import Subquery, OuterRef, Avg, Count
from django.db.models.functions import Coalesce
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Review, Photo, Reply
from .serializers import ReviewSerializer, PhotoSerializer, ReplySerializer
from .filters import ReviewFilter, PhotoFilter, ReplyFilter
from .paginations import ReviewPagination
from .permissions import ReviewPermission


# Create your views here.
class ReviewListCreateView(ListCreateAPIView):
    photo_count_subquery = Photo.objects.filter(review=OuterRef('id')).values('review').annotate(cnt=Count('id')).values('cnt')
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = ReviewFilter
    pagination_class = ReviewPagination


class ReviewDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [ReviewPermission]


class PhotoListCreateView(ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PhotoFilter


class PhotoDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class ReplyListCreateView(ListCreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ReplyFilter


class ReplyDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer