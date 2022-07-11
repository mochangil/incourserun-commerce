from xml.dom import ValidationErr
from django.forms import ValidationError
from django.shortcuts import render
from django_filters import rest_framework as filters
from django.db.models import Exists, OuterRef, Prefetch
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, CreateAPIView
from .models import Order, OrderProduct
from ..review.models import Review
from .serializers import OrderSerializer, OrderUpdateSerializer, OrderProductUpdateSerializer, CancelSerializer
from .filters import OrderFilter, OrderProductFilter
from ..common.permissions import IsStaff, IsOwner
from .permissions import OrderProductPermission
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

# class PaymentValidationView(ListCreateAPIView):
#     serializer_class = PaymentValidationSerializer


def payment_check(amounts, amounts_be_paid,status):
    res = ""
    if amounts == amounts_be_paid:
        if status == "ready":
            res = "unsupported features"
        elif status == "paid":
            res = "결제완료"
        else:
            res = "cancelled"
    
    return res


def payment_complete(request):
    # 결제번호, 주문번호 - post
    # Webhook, 일반적 결제완료
    if request.method == 'POST':
        imp_uid = request.POST['imp_uid']
        merchant_uid = request.POST['merchant_uid']
    # mobile
    if request.method == 'GET':
        imp_uid = request.GET['imp_uid']
        merchant_uid = request.GET['merchant_uid']

    # test id
    # imp_uid = '결제 id'
    # merchant_uid = '주문 id'
    
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
    header = {'Authorization':f'Bearer {access_token}'}
    imp_inf = requests.get(url=url,headers=header)
    print("imp_inf => \n",imp_inf)
    # if not imp_inf.ok:
    #     raise ValidationError("Paydata Error")
    imp_inf = imp_inf.json()
    data = imp_inf['response']


    #test data
    # data = {
    #     'merchant_uid':merchant_uid,
    #     'status':'paid',
    #     'amounts':10,
    #     }
    # print(data)


    #3 검증
    merchant_uid = data['merchant_uid']
    status = data['status']
    amounts = data['amounts']
    order = Order.objects.get(merchant_uid=merchant_uid)
    amounts_be_paid = order.total_paid
    res = payment_check(amounts,amounts_be_paid,status)
    
    if res == "결제완료":
        order.imp_uid = imp_uid
        order.shipping_status = "결제완료"
        redirect_url = f"{settings.ORDER_ROOT}/{order.id}"
    elif res == 'unsupported features':
        order.delete()
        redirect_url = f"{settings.ORDER_ROOT}"
        raise ValidationError("지원하지 않는 결제 수단입니다.")
    else:
        order.delete()
        redirect_url = f"{settings.ORDER_ROOT}"
        raise ValidationError("환불되었거나 결제금액이 일치하지 않습니다. 위/변조된 결제")
    
    print(res)
    #결제완료 페이지 (현재는 해당 유저의 주문내역)
    #front에 return해줄 응답
    return redirect(redirect_url)


class CancelCreateView(CreateAPIView):
    serializer_class = CancelSerializer