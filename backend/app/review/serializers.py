from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction
from .models import Review, Photo, Reply


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'img']


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id', 'content', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    reply = ReplySerializer(read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)
    photo_count = serializers.IntegerField(read_only=True)    

    class Meta:
        model = Review
        fields = (
            'id',
            'user',
            'product',
            'order_product',
            'rating',
            'content',
            'created_at',
            'reply',
            'photos',
            'photo_count'
        )

    def validate(self, attrs):
        # if attrs['user'] != self.context['request'].user:
        #     raise ValidationError({'user': '요청인과 작성자가 일치하지 않습니다.'})
        if attrs['user'] != attrs['order_product'].order.user:
            raise ValidationError({'user': '주문자와 작성자가 일치하지 않습니다.'})
        if attrs['order_product'].shipping_status != "배송완료":
            raise ValidationError({'shippingStatus': '배송 완료된 상품만 작성 가능합니다.'})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        # 리뷰 저장
        validated_data['product'] = validated_data['order_product'].product
        review = Review.objects.create(**validated_data)

        # 리뷰 이미지 저장
        if 'imgs' in self.context['request'].FILES:
            imgs = self.context['request'].FILES.pop('imgs')
            if len(imgs) > 3:
                raise ValidationError({'imgs': '리뷰 이미지는 최대 3장까지만 등록 가능합니다.'})
            for img in imgs:
                Photo.objects.create(review=review, img=img)

        return review