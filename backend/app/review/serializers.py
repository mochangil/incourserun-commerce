from rest_framework import serializers
from .models import Review, Photo, Reply


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)
    reply = ReplySerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            'id',
            'user',
            'product',
            'rating',
            'content',
            'created',
            'photos',
            'reply'
        )
