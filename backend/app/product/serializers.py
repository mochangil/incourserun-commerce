from rest_framework import serializers
from .models import Product, Hashtag


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only = True)
    review_count = serializers.IntegerField(read_only = True)
    hashtags = HashtagSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


