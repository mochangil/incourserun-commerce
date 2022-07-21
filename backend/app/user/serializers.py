from tempfile import NamedTemporaryFile
from urllib.request import urlopen

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.files import File
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Social, SocialKindChoices, AgeChoices, GenderChoices, Withdrawal


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
        # print('validation: ', attrs['code'], attrs['state'], attrs['redirect_uri'])
        social_user_data = self.get_social_user_data(attrs['code'], attrs['state'], attrs['redirect_uri'])
        if social_user_data['kakao_account'].get('age_range') == '1~9':
            raise ValidationError({'age_range': '10대 미만은 가입할 수 없습니다.'})
        attrs['social_user_data'] = social_user_data
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data['social_user_data']
        social_user_id = user_data['id']
        kakao_account = user_data['kakao_account']
        state = validated_data['state']
        # print('social user id: ', social_user_id)

        user, created = User.objects.get_or_create(username=f'{social_user_id}@{state}.social', defaults={
            'password': make_password(None)
        })

        if created or user.is_active is False:  # 신규가입 / 재가입일 경우
            # 재가입인 경우
            if user.is_active is False:
                user.is_active = True
            
            user.email = kakao_account.get('email')
            user.nickname = kakao_account['profile'].get('nickname')

            # 프로필 이미지 저장
            print('profile_image_url' in kakao_account['profile'])
            if 'profile_image_url' in kakao_account['profile']:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(kakao_account['profile']['profile_image_url']).read())
                img_temp.flush()
                user.avatar.save(f'avatar{user.pk}.jpg', File(img_temp))

            # Social 정보 저장
            Social.objects.create(user=user, kind=state)

        # 유저 정보 업데이트
        if kakao_account.get('gender') == 'male':
            user.gender = GenderChoices.MALE.value
        elif kakao_account.get('gender') == 'female':
            user.gender = GenderChoices.FEMALE.value
        else:
            user.gender = None

        age_range = kakao_account.get('age_range')
        if age_range is None:
            user.age_range = None
        elif age_range == '10~14' or age_range == '15~19':
            user.age_range = AgeChoices.TEEN.value
        elif age_range == '20~29':
            user.age_range = AgeChoices.TWENTY.value
        elif age_range == '30~39':
            user.age_range = AgeChoices.THIRTY.value
        elif age_range == '40~49':
            user.age_range = AgeChoices.FORTY.value
        else:
            user.age_range = AgeChoices.OVER_FIFTY.value

        user.save()

        # 토큰 발급
        refresh = RefreshToken.for_user(user)
        print("JWT token:", refresh.access_token)

        return {
            'access': refresh.access_token,
            'refresh': refresh,
            'is_register': user.is_register,
        }

    def get_social_user_data(self, code, state, redirect_uri):
        social_user_data = getattr(self, f'get_{state}_user_data')(code, redirect_uri)
        return social_user_data

    def get_kakao_user_data(self, code, redirect_uri):
        print('get_kakao_user_data: ', settings.KAKAO_CLIENT_ID, settings.KAKAO_CLIENT_SECRET, redirect_uri, code)
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
        print('kakao token: ', data)

        url = 'https://kapi.kakao.com/v2/user/me'
        headers = {
            'Authorization': f'Bearer {data["access_token"]}'
        }
        response = requests.get(url=url, headers=headers)
        if not response.ok:
            raise ValidationError('KAKAO ME API ERROR')
        data = response.json()
        print('me: ', data)
        return data

    def get_naver_user_data(self, code, redirect_uri):
        pass


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    social = SocialSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "name",
            "nickname",
            "email",
            "phone",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_register",
            "gender",
            "age_range",
            "zipcode",
            "address",
            "address_detail",
            "avatar",
            "created_at",
            "agree_all_terms",
            "required_terms",
            "private_info_terms",
            "marketing_terms",
            "social",
        )


class WithdrawalSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Withdrawal
        fields = (
            "id",
            "user",
            "reasons",
            "reason_others",
            "created_at"
        )

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        if attrs['reasons'] != '기타' and 'reason_others' in attrs:
            raise ValidationError({'reason_others': "'기타'를 선택했을 때만 기타사유를 작성할 수 있습니다."})
        return attrs

    def create(self, validated_data):
        # Withdrawal Object 생성
        withdrawal, created = Withdrawal.objects.get_or_create(user=validated_data['user'])
        withdrawal.reasons = validated_data['reasons']
        withdrawal.reason_others = validated_data.get('reason_others', None)
        withdrawal.save()

        # 해당 user 비활성화, 데이터 초기화
        user = User.objects.get(email=validated_data.get('user'))
        user.is_active = False
        user.is_register = False

        user.name = None
        user.nickname = ''
        user.phone = None
        user.gender = None
        user.age_range = None
        user.zipcode = None
        user.address = None
        user.address_detail = None
        user.avatar = None
        user.agree_all_terms = False
        user.required_terms = False
        user.private_info_terms = False
        user.marketing_terms = False

        user.save()

        # 카카오 계정 연결 끊기
        url = 'https://kapi.kakao.com/v1/user/unlink'
        data = {
            'target_id_type': 'user_id',
            'target_id': validated_data['user'].username.split('@')[0]
        }
        headers = {
            'Authorization': f'KakaoAK {settings.KAKAO_APP_ADMIN_KEY}'
        }
        response = requests.post(url=url, data=data, headers=headers)
        print(response)
        if not response.ok:
            raise ValidationError('KAKAO UNLINK API ERROR')

        return withdrawal
