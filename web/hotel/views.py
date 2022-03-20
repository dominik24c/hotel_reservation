from base.view_utils import create_view_handlers
from rest_framework import generics, permissions

from .models import Hotel, Room
from .permissions import HotelOwnerPermission, OwnerEditHotelPermission, RoomHotelOwnerPermission
from .serializers import HotelSerializer, HotelUpdateSerializer, RoomSerializer


class HotelCreateListView(generics.ListCreateAPIView):
    queryset = Hotel.objects.prefetch_related('owner').all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticated, HotelOwnerPermission]

    def create(self, request, *args, **kwargs):
        return create_view_handlers(self, request, {'message': 'Hotel was created!'}, *args, **kwargs)


class HotelRDView(generics.RetrieveDestroyAPIView):
    queryset = Hotel.objects.prefetch_related('owner').all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticated, OwnerEditHotelPermission]


class HotelUpdateView(generics.UpdateAPIView):
    queryset = Hotel.objects.prefetch_related('owner').all()
    serializer_class = HotelUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, OwnerEditHotelPermission]


class RoomCreateListView(generics.ListCreateAPIView):
    queryset = Room.objects.prefetch_related('hotel__owner').all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated, RoomHotelOwnerPermission]

    def create(self, request, *args, **kwargs):
        return create_view_handlers(self, request, {'message': 'Room was created!'}, *args, **kwargs)
