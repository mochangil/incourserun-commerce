from django_filters import rest_framework as filters
from .models import Review, Photo, Reply

class ReviewFilter(filters.FilterSet):
    photo_count = filters.NumberFilter(field_name='photo_count', lookup_expr='gt', label="photo_count (greater than)")

    class Meta:
        model = Review
        fields = ['user', 'product']


class PhotoFilter(filters.FilterSet):
    class Meta:
        model = Photo
        fields = ['review']


class ReplyFilter(filters.FilterSet):
    class Meta:
        model = Reply
        fields = ['review']