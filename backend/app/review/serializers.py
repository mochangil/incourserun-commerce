from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Review, Photo, Reply


class PhotoSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['review'].photos.count() >= 3:
            raise ValidationError({'photoCount': '리뷰 하나에 사진은 3개까지만 등록 가능합니다.'})
        return attrs

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
    photo_count = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        order = attrs['order_product'].order
        if order.user != self.context['request'].user:
            raise ValidationError({'user': '주문자와 작성자가 일치하지 않습니다.'})
        if order.shipping_status != "배송완료":
            raise ValidationError({'shippingStatus': '배송 완료된 상품만 작성 가능합니다.'})
        return attrs    

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
            'photos',
            'reply',
            'photo_count'
        )