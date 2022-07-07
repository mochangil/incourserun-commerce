from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'created_at',
        'order_number',
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
    list_filter = ('shipping_status', 'is_cancelled')
    search_fields = ('=user__name', '^user__email', '^order_number', '=shipping_name', '^shipping_phone', '=shipping_zipcode', 'shipping_address', 'shipping_address_detail')


@admin.register(models.OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
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
    search_fields = ('^product__name', '^order__order_number', '=order__user__name', '=order__shipping_zipcode', 'order__shipping_address',)