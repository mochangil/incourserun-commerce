import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from app.user.models import User, Social, SocialKindChoices, Cart
from app.order.serializers import OrderSerializer
from app.review.serializers import ReviewSerializer
from app.product.serializers import ProductSerializer


class UserSocialLoginSerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True)
    state = serializers.CharField(write_only=True)
    redirect_uri = serializers.URLField(write_only=True)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    is_register = serializers.BooleanField(read_only=True)

    def validate(self, attrs):
        if attrs['state'] not in SocialKindChoices:
            raise ValidationError({'kind': '지원하지 않는 소셜 타입입니다.'})

        attrs['social_user_data'] = self.get_social_user_data(attrs['code'], attrs['state'])
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        social_user_id = validated_data['social_user_data']['id']
        kakao_account = validated_data['social_user_data']['kakao_account']
        state = validated_data['state']
        user, created = User.objects.get_or_create(email=f'{social_user_id}@{state}.social', defaults={
            'password': make_password(None)
        })

        if created:
            # user 데이터 추가
            user.username = kakao_account['email']
            user.nickname = kakao_account['profile']['nickname']
            user.profile = kakao_account['profile']['profile_image_url']
            if kakao_account['has_gender']:
                user.gender = kakao_account['gender']
            if kakao_account['has_age_range']:
                age = kakao_account['age_range']
                if age == '1~9':
                    pass
                elif age == '10~14' or age == '15~19':
                    user.age = 'teen'
                elif age == '20~29':
                    user.age = 'twenty'
                elif age == '30~39':
                    user.age = 'thirty'
                elif age == '40~49':
                    user.age = 'forty'
                else:
                    user.age = 'fifty'
            user.save()
            Social.objects.create(user=user, kind=state)

        refresh = RefreshToken.for_user(user)

        return {
            'access': refresh.access_token,
            'refresh': refresh,
            'is_register': user.is_register,
        }

    def get_social_user_data(self, code, state):
        redirect_uri = settings.KAKAO_REDIRECT_URL
        social_user_data = getattr(self, f'get_{state}_user_data')(code, redirect_uri)
        return social_user_data

    def get_kakao_user_data(self, code, redirect_uri):
        url = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.KAKAO_CLIENT_ID,
            'redirect_uri': redirect_uri,
            'code': code,
            'client_secret': settings.KAKAO_CLIENT_SECRET,
        }
        response = requests.post(url=url, data=data)
        if not response.ok:
            raise ValidationError('KAKAO GET TOKEN API ERROR')
        data = response.json()

        url = 'https://kapi.kakao.com/v2/user/me'
        headers = {
            'Authorization': f'Bearer {data["access_token"]}'
        }
        response = requests.get(url=url, headers=headers)
        if not response.ok:
            raise ValidationError('KAKAO ME API ERROR')
        data = response.json()
        return data

    def get_naver_user_data(self, code, redirect_uri):
        pass


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = (
            'id',
            'user',
            'product',
            'amount'
        )


class UserSerializer(serializers.ModelSerializer):
    is_superuser = serializers.BooleanField(read_only = True)
    is_staff = serializers.BooleanField(read_only = True)
    is_register = serializers.BooleanField(read_only = True)
    social = SocialSerializer(read_only=True)
    carts = CartSerializer(many=True, read_only=True)
    orders = OrderSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "nickname",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_register",
            "gender",
            "age",
            "zipcode",
            "address",
            "address_detail",
            "profile",
            "created",
            "social",
            "carts",
            "orders",
            "reviews"
        )



