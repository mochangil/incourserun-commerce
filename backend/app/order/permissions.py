from rest_framework.permissions import BasePermission

class OrderProductPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.order.user == request.user