from rest_framework import serializers

from .models import Product, Hashtag


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "category",
            "capacity",
            "price",
            "description",
            "thumbnail_img",
            "product_img",
            "detail_img",
            "hashtags",
            "avg_rating",
            "review_count",
            "created_at"
        )
