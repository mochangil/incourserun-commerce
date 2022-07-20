import requests
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Order, OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):
    has_review = serializers.BooleanField(read_only=True)

    class Meta:
        model = OrderProduct
        fields = ('id', 'product', 'quantity', 'price', 'shipping_status', 'is_cancelled', 'has_review')


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True)
    merchant_uid = serializers.CharField(read_only=True)
    imp_uid = serializers.CharField(read_only=True)
    cancel_amount = serializers.IntegerField(read_only=True)
    shipping_status = serializers.CharField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'created_at',
            'imp_uid',
            'merchant_uid',
            'shipping_name',
            'shipping_phone',
            'shipping_zipcode',
            'shipping_address',
            'shipping_address_detail',
            'shipping_request',
            'shipping_status',
            'pay_method',
            'pay_date',
            'total_price',
            'delivery_fee',
            'total_paid',
            'cancel_amount',
            'is_cancelled',
            'order_products'
        )

    def validate(self, attrs):
        # 프론트에서 보낸 금액이랑 백에서 계산한 금액이랑 비교
        total_price = 0
        for order_product in attrs['order_products']:
            total_price += order_product['price'] * order_product['quantity']
        if total_price != attrs['total_price']:
            raise ValidationError("total_price", "총 상품금액이 계산된 값과 일치하지 않습니다.")

        delivery_fee = 0
        if total_price < 30000:
            delivery_fee = 3000
        if delivery_fee != attrs['delivery_fee']:
            raise ValidationError("delivery_fee", "배송비가 일치하지 않습니다.")
        if attrs['total_price'] + attrs['delivery_fee'] != attrs['total_paid']:
            raise ValidationError("total_paid", "결제금액이 총 상품금액 + 배송비와 일치하지 않습니다.")

        # 상품이 없을 경우 ValidationError 발생
        if 'order_products' not in attrs:
            raise ValidationError("order_products", "상품이 최소 1개 이상 있어야 합니다.")

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        order_products = validated_data.pop('order_products')
        order = Order.objects.create(**validated_data)
        order.merchant_uid = f'ORD{order.created_at.strftime("%y%m%d")}-{str(order.id).zfill(6)}'
        order.save()
        for order_product in order_products:
            OrderProduct.objects.create(order=order, **order_product)
        return order


def get_token():  # 토큰 발급
    url = 'https://api.iamport.kr/users/getToken'
    data = {
        'imp_key': settings.IMP_KEY,
        'imp_secret': settings.IMP_SECRET
    }
    token = requests.post(url=url, data=data)
    access_token = token.json()
    access_token = access_token['response'].get('access_token')
    # print("access_token => \n", access_token, "\n")
    return access_token


class OrderPaymentSerializer(serializers.Serializer):
    imp_uid = serializers.CharField(write_only=True)
    merchant_uid = serializers.CharField(write_only=True)
    status = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)
    order = OrderSerializer(read_only=True)

    def validate(self, attrs):
        access_token = get_token()
        print('access_token: ', access_token)
        data = self.get_imp_info(access_token, attrs['imp_uid'])
        # print(data)

        attrs['access_token'] = access_token
        attrs['data'] = data
        # print(attrs)
        return attrs

    def create(self, validated_data):
        data = validated_data['data']
        imp_uid = validated_data['imp_uid']
        data = self.imp_validation(data, imp_uid)
        # print("create:", data)
        return data

    def payment_check(self, amounts, amounts_be_paid, status):
        res = ""
        if amounts == amounts_be_paid:
            if status == "ready":
                res = "unsupported features"
            elif status == "paid":
                res = "결제완료"
            else:
                res = "cancelled"
        return res

    def get_imp_info(self, access_token, imp_uid):  # 결제정보 조회
        url = f"https://api.iamport.kr/payments/{imp_uid}"
        header = {'Authorization': f'Bearer {access_token}'}
        imp_inf = requests.get(url=url, headers=header)
        # print("imp_inf => \n", imp_inf)
        data = imp_inf.json()
        if not imp_inf.ok:
            raise ValidationError({"Paydata Error": data['message']})
        return data['response']

    def imp_validation(self, data, imp_uid):  # 결제정보 검증
        merchant_uid = data['merchant_uid']
        status = data['status']
        amounts = data['amount']
        order = Order.objects.get(merchant_uid=merchant_uid)
        amounts_be_paid = order.total_paid
        res = self.payment_check(amounts, amounts_be_paid, status)
        # print(res)

        if res == "결제완료":
            order.imp_uid = imp_uid
            order.shipping_status = "결제완료"
            order.save()
            message = "결제완료"
        elif res == 'unsupported features':
            raise ValidationError({"결제 실패": "unsupported features"})
        else:
            raise ValidationError("결제 실패")

        data = {
            "status": status,
            "message": message,
            "order": order
        }
        return data


class CancelSerializer(serializers.Serializer):
    merchant_uid = serializers.CharField(write_only=True)
    cancel_request_amount = serializers.CharField(write_only=True)
    reason = serializers.CharField(write_only=True)
    result = OrderSerializer(read_only=True)

    def validate(self, attrs):
        merchant_uid = attrs['merchant_uid']
        # 결제정보 조회
        order = get_object_or_404(Order, merchant_uid=merchant_uid)
        imp_uid, amount, cancel_amount = order.imp_uid, order.total_paid, order.cancel_amount
        cancelable_amount = amount - cancel_amount
        if cancelable_amount <= 0:
            raise ValidationError({"merchant_uid": "이미 전액환불된 주문입니다."})
        if order.shipping_status != '결제완료':
            raise ValidationError({"merchant_uid": "결제완료 상태에서만 주문취소가 가능합니다."})

        # 결제환불 요청
        access_token = get_token()
        url = "https://api.iamport.kr/payments/cancel"
        data = {
            'merchant_uid': merchant_uid,
            'amount': attrs['cancel_request_amount'],
            'reason': attrs['reason'],
            'checksum': cancelable_amount,
        }
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.post(url=url, data=data, headers=headers)
        data = response.json()

        if not response.ok:
            raise ValidationError({'IAMPORT CANCEL API ERROR': data['message']})

        # 응답 코드가 200이라도 응답 body의 code가 0이 아니면 환불에 실패했다는 의미
        if data['code'] != 0:
            raise ValidationError({'환불 실패': data['message']})
        return data

    def create(self, validated_data):
        response = validated_data['response']  # 환불 결과

        # 환불 결과 동기화
        merchant_uid = response['merchant_uid']
        order = Order.objects.get(merchant_uid=merchant_uid)
        order.cancel_amount = response['cancel_amount']
        order.is_cancelled = True
        order.save()
        return {
            'result': order
        }
