from base.view_utils import create_view_handlers
from rest_framework import generics, permissions, viewsets
from rest_framework import mixins

from .models import Hotel, Room, Comment
from .permissions import HotelOwnerPermission, \
    OwnerEditHotelPermission, RoomHotelOwnerPermission, \
    UserCommentPermission
from .serializers import HotelSerializer, \
    HotelUpdateSerializer, RoomSerializer, \
    RoomUpdateDeleteSerializer, CommentSerializer, \
    CommentCreateSerializer


class UpdateDestroyApiView(mixins.DestroyModelMixin,
                           mixins.UpdateModelMixin,
                           generics.GenericAPIView):
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class HotelViewSet(viewsets.ModelViewSet):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.prefetch_related('owner').all()
    permission_classes = [permissions.IsAuthenticated]


class HotelCreateView(generics.CreateAPIView):
    queryset = Hotel.objects.prefetch_related('owner').all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticated, HotelOwnerPermission]

    def create(self, request, *args, **kwargs):
        return create_view_handlers(self, request, {'message': 'Hotel was created!'}, *args, **kwargs)


class HotelDeleteUpdateView(UpdateDestroyApiView):
    queryset = Hotel.objects.prefetch_related('owner').all()
    serializer_class = HotelUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, OwnerEditHotelPermission]


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Room.objects.prefetch_related('hotel__owner').filter(hotel=self.kwargs['hotel_pk'])


class RoomCreateView(generics.CreateAPIView):
    queryset = Room.objects.prefetch_related('hotel__owner').all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated, RoomHotelOwnerPermission]

    def create(self, request, *args, **kwargs):
        return create_view_handlers(self, request, {'message': 'Room was created!'}, *args, **kwargs)


class RoomUpdateDeleteView(UpdateDestroyApiView):
    queryset = Room.objects.prefetch_related('hotel__owner').all()
    serializer_class = RoomUpdateDeleteSerializer
    permission_classes = [permissions.IsAuthenticated, RoomHotelOwnerPermission]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(hotel=self.kwargs['hotels_pk'])


class CommentDeleteUpdateView(UpdateDestroyApiView):
    queryset = Comment.objects.select_related('user').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, UserCommentPermission]


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
