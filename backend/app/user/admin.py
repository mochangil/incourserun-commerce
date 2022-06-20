from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    fieldsets = (
        ('Personal info', 
            {'fields': (
            "username",
            "password",
            'nickname',
            'email', 
            "is_active",
            "is_staff",
            "is_superuser",
            "is_register",
            "gender",
            "age",
            "address",
            "profile",
            )}
        ),
    )

    list_filter = UserAdmin.list_filter

    list_display = (
        "username",
        "nickname",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_register",
        "gender",
        "age",
        "address",
        "profile",
        "created"
    )

@admin.register(models.Social)
class SocialAdmin(admin.ModelAdmin):

    """Review Admin Definition"""

    list_display = ("user","kind")

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "amount")
