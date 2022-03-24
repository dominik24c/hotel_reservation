from rest_framework import permissions


class UserReservationPermission(permissions.BasePermission):
    message = "It's not your reservation!"

    def has_object_permission(self, request, view, obj):
        return request.user.username == obj.customer.username
