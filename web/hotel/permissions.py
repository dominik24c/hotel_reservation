from account.groups import G_HOTEL_OWNER
from rest_framework import permissions


class HotelOwnerPermission(permissions.BasePermission):
    message = 'User belonging to the group of hotel owner can create hotel model!'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.first().name == G_HOTEL_OWNER


class OwnerEditHotelPermission(permissions.BasePermission):
    message = 'Only owner can delete or update hotel model!'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.username == obj.owner.username


class RoomHotelOwnerPermission(permissions.BasePermission):
    message = 'Only hotel owner can create room for your hotel!'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.username == obj.hotel.owner.username


class UserCommentPermission(permissions.BasePermission):
    message = "It's not your comment, you cannot delete or update it!"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.username == obj.user.username
