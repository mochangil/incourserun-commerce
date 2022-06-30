from rest_framework.permissions import BasePermission

class ReviewPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class PhotoPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.review.user == request.user

class ReplyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff