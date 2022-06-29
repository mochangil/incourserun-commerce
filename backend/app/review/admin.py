from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display =  (
        'id',
        'user',
        'product',
        'rating',
        'content',
        'created_at'
    )

@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'review',
        'img'
    )

@admin.register(models.Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'review',
        'content',
        'created_at'
    )

