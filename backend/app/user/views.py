import requests
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError
from app.user.serializers import UserSocialLoginSerializer, UserSerializer, CartSerializer, SocialSerializer,WithdrawalUserSerializer
from django.shortcuts import redirect
from django.db.models import Prefetch
from django.conf import settings
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from .models import Cart, Social, Withdrawal
from .filters import UserFilter, CartFilter
from .permissions import CartPermission
from django.db.models import Subquery, OuterRef


class UserSocialLoginView(CreateAPIView):
    """
    유저 소셜로그인
    ---
    소셜로그인의 callback으로 전달받은 code와 state값으로 로그인 또는 회원가입을 합니다.
    """
    serializer_class = UserSocialLoginSerializer


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




class CartListCreateView(ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CartFilter


class CartDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    # permission_classes = [CartPermission]


def kakao_login(request):
    client_id = settings.KAKAO_CLIENT_ID
    redirect_uri = f"{settings.USER_ROOT}/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )
    
def kakao_callback(request):
    code = request.GET.get("code")
    print(code)
    redirect_uri = settings.KAKAO_REDIRECT_URL

    url = f"{settings.USER_ROOT}/social_login"
    data = {
        'code': code,
        'state':'kakao',
        'redirect_uri': redirect_uri,
    }
    response = requests.post(url=url, data=data)
    if not response.ok:
        raise ValidationError()
    return redirect(settings.USER_ROOT)

class UserWithdrawalListCreateView(ListCreateAPIView):
    User = get_user_model()
    queryset = Withdrawal.objects.all()
    print(queryset)
    serializer_class = WithdrawalUserSerializer