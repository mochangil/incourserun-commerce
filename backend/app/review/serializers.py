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
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)
    reply = ReplySerializer(read_only=True)
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
            'photos',
            'reply',
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

    def create(self, validated_data):
        validated_data['product'] = validated_data['order_product'].product
        return Review.objects.create(**validated_data)