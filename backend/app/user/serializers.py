import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from app.user.models import User, Social, SocialKindChoices, Cart, AgeChoices, GenderChoices,Withdrawal
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

        social_user_data = self.get_social_user_data(attrs['code'], attrs['state'])
        kakao_account = social_user_data['kakao_account']
        if kakao_account['has_age_range']:
            if kakao_account['age_range'] == '1~9':
                raise ValidationError({'age': '10대 미만은 가입할 수 없습니다.'})
        attrs['social_user_data'] = social_user_data
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

            if kakao_account['has_gender']:
                if kakao_account['gender'] == 'male':
                    user.gender = GenderChoices.MALE.value
                if kakao_account['gender'] == 'female':
                    user.gender = GenderChoices.FEMALE.value

            if kakao_account['has_age_range']:
                age = kakao_account['age_range']
                if age == '10~14' or age == '15~19':
                    user.age = AgeChoices.TEEN.value
                elif age == '20~29':
                    user.age = AgeChoices.TWENTY.value
                elif age == '30~39':
                    user.age = AgeChoices.THIRTY.value
                elif age == '40~49':
                    user.age = AgeChoices.FORTY.value
                else:
                    user.age = AgeChoices.OVER_FIFTY.value

            # 프로필 이미지 저장
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(kakao_account['profile']['profile_image_url']).read())
            img_temp.flush()
            user.profile_img.save(f'profile{user.pk}.jpg', File(img_temp))
            
            user.save()

            # Social 정보 저장
            Social.objects.create(user=user, kind=state)
        
        #탈퇴했던 유저인경우
        elif user.is_active == False:
            user.is_active = True
            if kakao_account['has_gender']:
                if kakao_account['gender'] == 'male':
                    user.gender = GenderChoices.MALE.value
                if kakao_account['gender'] == 'female':
                    user.gender = GenderChoices.FEMALE.value

            if kakao_account['has_age_range']:
                age = kakao_account['age_range']
                if age == '10~14' or age == '15~19':
                    user.age = AgeChoices.TEEN.value
                elif age == '20~29':
                    user.age = AgeChoices.TWENTY.value
                elif age == '30~39':
                    user.age = AgeChoices.THIRTY.value
                elif age == '40~49':
                    user.age = AgeChoices.FORTY.value
                else:
                    user.age = AgeChoices.OVER_FIFTY.value

            # 프로필 이미지 저장
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(kakao_account['profile']['profile_image_url']).read())
            img_temp.flush()
            user.profile_img.save(f'profile{user.pk}.jpg', File(img_temp))

            user.save()
            
            Social.objects.create(user=user, kind=state)

        refresh = RefreshToken.for_user(user)
        print("token:", refresh.access_token)

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
        print(data)
        return data

    def get_naver_user_data(self, code, redirect_uri):
        pass


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = '__all__'


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
            "profile_img",
            "created_at",
            "social",
            "carts",
            "orders",
            "reviews"
        )

class WithdrawalUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        withdrawal_user, created = Withdrawal.objects.get_or_create(user=validated_data['user'])
        withdrawal_user.reasons = validated_data['reasons']
        withdrawal_user.reason_others = validated_data['reason_others']
        print(validated_data['user'])
        withdrawal_user.save()
        #해당 user 비활성화
        user = User.objects.get(email = validated_data.get('user'))
        print(user)
        user.is_active = False
        user.save()
        return withdrawal_user

    class Meta:
        model = Withdrawal
        fields = (
            "id",
            "user",
            "reasons",
            "reason_others",
            "created_at"
        )