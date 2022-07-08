from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportMixin,ExportActionMixin
from . import models
from django.http import HttpResponse


# Register your models here.
@admin.register(models.Order)
class OrderAdmin(ImportExportMixin,ExportActionMixin,admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'get_user_email',
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
        'cancel_amount',
        'is_cancelled'
    )
    list_filter = ('shipping_status', 'is_cancelled')
    search_fields = ('=user__name', '^user__email', '^order_number', '=shipping_name', '^shipping_phone', '=shipping_zipcode', 'shipping_address', 'shipping_address_detail')

    def get_user_email(self,obj):
        return obj.user.email
    get_user_email.short_description = "이메일"


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
    search_fields = ('^product__name', '^order__order_number', '=order__user__name', '=order__shipping_zipcode', 'order__shipping_address',)