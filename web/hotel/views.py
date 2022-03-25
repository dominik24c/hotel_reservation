from base.permissions import CustomerPermission
from base.view_utils import create_view_handlers
from rest_framework import permissions, viewsets

from .models import Hotel, Room, Comment
from .permissions import HotelOwnerPermission, \
    OwnerEditHotelPermission, RoomHotelOwnerPermission, \
    UserCommentPermission
from .serializers import HotelSerializer, \
    HotelUpdateSerializer, RoomSerializer, \
    CommentSerializer


class HotelViewSet(viewsets.ModelViewSet):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.prefetch_related('owner').all()
    permission_classes = [permissions.IsAuthenticated, HotelOwnerPermission, OwnerEditHotelPermission]

    def get_serializer_class(self):
        if self.action == 'update':
            return HotelUpdateSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        return create_view_handlers(self, request, {'message': 'Hotel was created!'}, *args, **kwargs)


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated, RoomHotelOwnerPermission]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Room.objects.none()
        return Room.objects.prefetch_related('hotel__owner').filter(hotel=self.kwargs['hotel_pk'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['hotel_pk'] = self.kwargs.get('hotel_pk')
        return context

    def create(self, request, *args, **kwargs):
        return create_view_handlers(self, request, {'message': 'Room was created!'}, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated,
                          CustomerPermission,
                          UserCommentPermission]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Comment.objects.none()
        return Comment.objects.filter(hotel=self.kwargs['hotel_pk'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['hotel_pk'] = self.kwargs.get('hotel_pk')
        return context
