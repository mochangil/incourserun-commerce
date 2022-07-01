from rest_framework import serializers
from .models import Order, OrderProduct
from ..product.serializers import ProductSerializer
from ..review.serializers import ReviewSerializer


class OrderProductSerializer(serializers.ModelSerializer):
    has_review = serializers.BooleanField(read_only=True)

    class Meta:
        model = OrderProduct
        fields = ('product', 'quantity', 'has_review')


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True)

    def create(self, validated_data):
        order_products = validated_data.pop('order_products')
        order = Order.objects.create(**validated_data)
        for order_product in order_products:
            OrderProduct.objects.create(order=order, **order_product)
        return order

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'created_at',
            'shipping_name',
            'shipping_phone',
            'shipping_zipcode',
            'shipping_address',
            'shipping_address_detail',
            'shipping_request',
            'shipping_status',
            'pay_method',
            'pay_date',
            'pay_status',
            'total_amount',
            'delivery_fee',
            'is_cancelled',
            'order_products'
        )


