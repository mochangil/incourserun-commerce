from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        cart, created = Cart.objects.get_or_create(user=validated_data['user'], product=validated_data['product'])
        quantity = validated_data.get('quantity')
        if quantity is not None:
            if created: 
                cart.quantity = quantity
            else:
                cart.quantity += quantity
        cart.save()
        return cart

    class Meta:
        model = Cart
        fields = (
            'id',
            'user',
            'product',
            'quantity'
        )