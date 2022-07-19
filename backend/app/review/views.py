from django.db.models import OuterRef, Exists
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView

from .filters import ReviewFilter
from .models import Review, Photo
from .serializers import ReviewSerializer


# Create your views here.
class ReviewListCreateView(ListCreateAPIView):
    photo_subquery = Photo.objects.filter(review=OuterRef('id')).values('review')
    queryset = Review.objects.annotate(has_photo=Exists(photo_subquery))
    serializer_class = ReviewSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = ReviewFilter
