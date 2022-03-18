from rest_framework import permissions


class OwnerPermission(permissions.BasePermission):
    message = 'Update or Delete user profile is not allowed.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
