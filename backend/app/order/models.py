from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class ShippingStatusChoices(models.TextChoices):
    PAID = 'paid', '결제완료'
    READY = 'ready', '상품준비중'
    SHIPPING = 'shipping', '배송중'
    SHIPPED = 'shipped', '배송완료'

class PayMethodChoices(models.TextChoices):
    CARD = 'card', '신용카드'

class PayStatusChoices(models.TextChoices):
    PAID = 'paid', '결제완료'
    CANCELLED = 'cancelled', '결제취소'


class Order(models.Model):
    user = models.ForeignKey('user.User', related_name="orders", on_delete = models.CASCADE)
    created = models.DateTimeField(verbose_name="주문일시", auto_now_add=True)
    shipping_name = models.CharField(verbose_name="수령인", max_length=10)
    shipping_phone = models.CharField(verbose_name="전화번호", max_length=13)
    shipping_zipcode = models.CharField(verbose_name="우편번호", max_length=7)
    shipping_address = models.CharField(verbose_name="배송주소", max_length=1000)
    shipping_address_detail = models.CharField(verbose_name="배송상세주소", max_length=1000)
    shipping_request = models.CharField(verbose_name="배송요청사항", max_length=300)
    shipping_status = models.CharField(verbose_name="배송상태", choices=ShippingStatusChoices.choices, max_length=8)
    pay_method = models.CharField(verbose_name="결제수단", choices=PayMethodChoices.choices, max_length=4)
    pay_date = models.DateField(verbose_name="결제일자", auto_now_add=True)
    pay_status = models.CharField(verbose_name="결제상태", choices=PayStatusChoices.choices, max_length=9)
    total_amount = models.IntegerField(verbose_name="총 상품금액")
    delivery_fee = models.IntegerField(verbose_name="배송비")

    class Meta:
        verbose_name = "주문"
        verbose_name_plural = verbose_name


class OrderProduct(models.Model):
    order = models.ForeignKey('order.Order', related_name="order_products", on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', related_name="order_products", on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name="수량", validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = "주문-상품"
        verbose_name_plural = verbose_name