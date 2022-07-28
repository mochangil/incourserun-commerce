from django_filters import rest_framework as filters

from .models import Review


class ReviewFilter(filters.FilterSet):
    has_photo = filters.BooleanFilter(field_name='has_photo', label="Has Photo")

    class Meta:
        model = Review
        fields = ['user', 'product', 'has_photo', 'is_honest']
