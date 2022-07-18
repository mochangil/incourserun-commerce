from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Cart
from django.contrib.auth import get_user_model


class CartSerializer(serializers.ModelSerializer):
    User = get_user_model()

    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    def create(self, validated_data):
        validated_data['user']=self.context['request'].user
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