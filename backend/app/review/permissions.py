from rest_framework.permissions import BasePermission


class PhotoPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.review.user == request.user