import requests
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError
from app.user.serializers import UserSocialLoginSerializer, UserSerializer, CartSerializer, SocialSerializer,WithdrawalUserSerializer
from django.shortcuts import redirect
from django.db.models import Prefetch
from django.conf import settings
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework.permissions import AllowAny
from .models import Social, Withdrawal
from .filters import UserFilter
from .permissions import UserPermission
from django.db.models import Subquery, OuterRef
from ..cart.models import Cart

class UserSocialLoginView(CreateAPIView):
    """
    유저 소셜로그인
    ---
    소셜로그인의 callback으로 전달받은 code와 state값으로 로그인 또는 회원가입을 합니다.
    """
    serializer_class = UserSocialLoginSerializer
    permission_classes = [AllowAny]
    

class UserListView(ListAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = UserFilter


class UserDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [UserPermission]


def kakao_login(request):
    client_id = settings.KAKAO_CLIENT_ID
    redirect_uri = settings.KAKAO_REDIRECT_URI
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )

class UserWithdrawalListCreateView(ListCreateAPIView):
    queryset = Withdrawal.objects.all()
    # print(queryset)
    serializer_class = WithdrawalUserSerializer
    #permission_classes = [UserPermission]

class UserWithdrawalUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalUserSerializer