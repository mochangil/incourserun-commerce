from xml.dom import ValidationErr
from django.forms import ValidationError
from django.shortcuts import render
from django_filters import rest_framework as filters
from django.db.models import Exists, OuterRef, Prefetch
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from .models import Order, OrderProduct
from ..review.models import Review
from .serializers import OrderSerializer, OrderUpdateSerializer, OrderProductUpdateSerializer, PaymentValidationSerializer
from .filters import OrderFilter, OrderProductFilter
from ..common.permissions import IsStaff, IsOwner
from .permissions import OrderProductPermission
from config.settings.base import iamport
from django.shortcuts import redirect
from django.db.models import Prefetch
from django.conf import settings
import requests


has_review_subquery = Review.objects.filter(order_product=OuterRef('id'))

class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all().prefetch_related(
        Prefetch("order_products", queryset = OrderProduct.objects.annotate(has_review = Exists(has_review_subquery)))
    )
    serializer_class = OrderSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OrderFilter
    # permission_classes = [IsStaff]


class OrderDetailUpdateDeleteView(RetrieveUpdateAPIView):
    queryset = Order.objects.all().prefetch_related(
        Prefetch("order_products", queryset = OrderProduct.objects.annotate(has_review = Exists(has_review_subquery)))
    )
    serializer_class = OrderUpdateSerializer
    # permission_classes = [IsOwner]


class OrderProductDetailUpdateView(RetrieveUpdateAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductUpdateSerializer
    # permission_classes = [OrderProductPermission]

class PaymentValidationView(ListCreateAPIView):
    serializer_class = PaymentValidationSerializer




def payment_complete(request):
    # iamport-webhook post요청 처리필요

    # 결제번호, 주문번호 - post
    # imp_uid = request.POST['imp_uid']
    # merchant_uid = request.POST['merchant_uid']
    imp_uid = 'imp_114101979999'
    merchant_uid = '2207050002'
    
    #1. access token
    url = 'https://api.iamport.kr/users/getToken'
    data = {
        'imp_key': settings.IMP_KEY,
        'imp_secret': settings.IMP_SECRET
    }
    token = requests.post(url=url,data=data)
    access_token = token.json()
    access_token = access_token['response'].get('access_token')
    print("access_token => \n",access_token,"\n")

    #2. imp_uid로 아임포트 서버에서 결제 정보 조회
    url = f"https://api.iamport.kr/payments/{imp_uid}"
    header = {'HTTP_Authorization':f'Bearer {access_token}'}
    imp_inf = requests.get(url=url,headers=header)
    print("imp_inf => \n",imp_inf)
    # if not imp_inf.ok:
    #     raise ValidationError("Paydata Error")
    imp_inf = imp_inf.json()
    data = imp_inf['response']

    #test data
    data = {
        'merchant_uid':merchant_uid,
        'status':'paid',
        'amounts':10,
        }
    print(data)

    #3 검증
    merchant_uid = data['merchant_uid']
    status = data['status']
    amounts = data['amounts']
    order = Order.objects.get(order_number=merchant_uid)

    amount_be_paid = order.total_paid
    if amounts == amount_be_paid:
        if status == "paid":
            print("success\n")
            order.shipping_status = "결제완료"
    else:
        #order.delete()
        raise ValidationError("결제금액 불일치. 위/변조된 결제")

    #결제완료 페이지 (현재는 해당 유저의 주문내역)
    #front에 return해줄 응답
    order = Order.objects.get(order_number=merchant_uid)
    return redirect(f"{settings.ORDER_ROOT}/{order.id}")

