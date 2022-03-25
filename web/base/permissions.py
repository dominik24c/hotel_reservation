from account.groups import G_CUSTOMER
from rest_framework import permissions


class CustomerPermission(permissions.BasePermission):
    message = "You are not customer!"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.first().name == G_CUSTOMER
