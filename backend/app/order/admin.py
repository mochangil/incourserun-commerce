from django.contrib import admin
from django.contrib.auth import get_user_model
from import_export import resources
from import_export.widgets import ForeignKeyWidget
from import_export.fields import Field
from import_export.admin import ImportExportMixin,ExportActionMixin

from . import models
from django.http import HttpResponse

class OrderResources(resources.ModelResource):
    User=get_user_model()

    id = Field(attribute='id',column_name='id')
    username = Field(attribute='get_user_name',column_name='주문자')
    created_at = Field(attribute='created_at',column_name='생성일시')
    imp_uid = Field(attribute='imp_uid',column_name='결제번호')
    merchant_uid = Field(attribute='merchant_uid',column_name='주문번호')
    shipping_name = Field(attribute='shipping_name',column_name='수령인')
    shipping_phone = Field(attribute='shipping_name',column_name='전화번호')
    shipping_zipcode = Field(attribute='shipping_name',column_name='우편번호')
    shipping_address = Field(attribute='id',column_name='배송주소')
    shipping_address_detail = Field(attribute='shipping_address_detail',column_name='배송상세주소')
    shipping_request = Field(attribute='shipping_request',column_name='배송요청사항')
    shipping_status = Field(attribute='shipping_status',column_name='배송상태')
    pay_method = Field(attribute='pay_method',column_name='결제수단')
    pay_date = Field(attribute="pay_date", column_name='결제일자')
    total_price = Field(attribute="total_price", column_name='총 상품금액')
    delivery_fee = Field(attribute="delivery_fee",column_name='배송비')
    total_paid = Field(attribute="total_paid", column_name='결제금액')
    is_cancelled = Field(attribute="is_cancelled", column_name='취소여부')
    username = Field(column_name='주문인',attribute="user",widget=ForeignKeyWidget(User,"name"))
    class Meta:
        model = models.Order
        fields = (
            'id',
            'get_user_name',
            'get_user_email',
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
            'is_cancelled'
    )

# Register your models here.
@admin.register(models.Order)
class OrderAdmin(ImportExportMixin,ExportActionMixin,admin.ModelAdmin):
    resource_class = OrderResources

    list_display = (
        'id',
        'get_user_name',
        'get_user_email',
        'created_at',
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
        'is_cancelled'
    )
    list_filter = ('shipping_status', 'is_cancelled')
    search_fields = ('=user__name', '^user__email', '^merchant_uid', '=shipping_name', '^shipping_phone', '=shipping_zipcode', 'shipping_address', 'shipping_address_detail')

    def get_user_email(self,obj):
        return obj.user.email
    get_user_email.short_description = "이메일"

    def get_user_name(self,obj):
        return obj.user.name
    get_user_name.short_description = "주문자"


@admin.register(models.OrderProduct)
class OrderProductAdmin(ImportExportMixin,ExportActionMixin,admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'quantity',
        'price',
        'shipping_status',
        'is_cancelled'
    )
    list_filter = ('product', 'shipping_status', 'is_cancelled')
    search_fields = ('^product__name', '^order__merchant_uid', '=order__user__name', '=order__shipping_zipcode', 'order__shipping_address',)