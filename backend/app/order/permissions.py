from rest_framework.permissions import BasePermission

ALLOWED_IP_ADDRESSES = ['127.0.0.1', '52.78.100.19', '52.78.48.223']


class OrderProductPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.order.user == request.user


class OrderWebhookPermission(BasePermission):
    def has_permission(self, request, view):
        print("urlname : ", request.resolver_match.route)
        # webhook요청이 아닌경우
        if request.resolver_match.route == 'v1/orders/payment/complete':
            return True

        # webhook요청인경우 ip검사
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        print("Your ip = ", ip)

        return ip in ALLOWED_IP_ADDRESSES
