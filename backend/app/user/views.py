import requests
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from app.user.serializers import UserSocialLoginSerializer, UserSerializer, SocialSerializer, WithdrawalSerializer
from django.shortcuts import redirect
from django.db.models import Prefetch
from django.conf import settings
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from .models import Social, Withdrawal
from .filters import UserFilter
from .permissions import UserPermission
from ..cart.models import Cart
from ..cart.serializers import CartSerializer
from ..order.models import Order
from ..order.serializers import OrderSerializer
from ..review.models import Review
from ..review.serializers import ReviewSerializer
from ..review.paginations import ReviewPagination


class UserSocialLoginView(CreateAPIView):
    """
    유저 소셜로그인
    ---
    소셜로그인의 callback으로 전달받은 code와 state값으로 로그인 또는 회원가입을 합니다.
    """
    serializer_class = UserSocialLoginSerializer
    permission_classes = [AllowAny]


class MeDetailUpdateDeleteView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class MeCartListView(ListAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user = self.request.user)


class MeOrderListView(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user)


class MeReviewListView(ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination

    def get_queryset(self):
        return Review.objects.filter(user = self.request.user)


class WithdrawalCreateView(CreateAPIView):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer


def kakao_login(request):
    client_id = settings.KAKAO_CLIENT_ID
    # redirect_uri = settings.KAKAO_REDIRECT_URI
    redirect_uri = 'http://172.30.1.17:3000'
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )