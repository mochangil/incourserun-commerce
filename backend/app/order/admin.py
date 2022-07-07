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