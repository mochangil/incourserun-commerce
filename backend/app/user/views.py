from django.conf import settings
from django.db.models import Exists, OuterRef
from django.db.models import Prefetch
from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import Withdrawal
from .serializers import UserSocialLoginSerializer, UserSerializer, WithdrawalSerializer
from ..cart.models import Cart
from ..cart.serializers import CartSerializer
from ..order.models import Order, OrderProduct
from ..order.serializers import OrderSerializer
from ..review.models import Review
from ..review.serializers import ReviewSerializer


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
        return Cart.objects.filter(user=self.request.user)


class MeOrderListView(ListAPIView):
    has_review_subquery = Review.objects.filter(order_product=OuterRef('id'))
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch("order_products",
                     queryset=OrderProduct.objects.annotate(has_review=Exists(self.has_review_subquery)))
        )


class MeReviewListView(ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class WithdrawalCreateView(CreateAPIView):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer


class KakaoLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        client_id = settings.KAKAO_CLIENT_ID
        redirect_uri = settings.KAKAO_REDIRECT_URI
        print(client_id, redirect_uri)
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        )
