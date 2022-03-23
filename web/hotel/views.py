from base.view_utils import create_view_handlers
from rest_framework import generics, permissions, viewsets
from rest_framework import mixins

from .models import Hotel, Room, Comment
from .permissions import HotelOwnerPermission, \
    OwnerEditHotelPermission, RoomHotelOwnerPermission, \
    UserCommentPermission
from .serializers import HotelSerializer, \
    HotelUpdateSerializer, RoomSerializer, \
    RoomUpdateSerializer, CommentSerializer, \
    CommentCreateSerializer


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


class RoomRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.prefetch_related('hotel__owner').all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated, RoomHotelOwnerPermission]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return RoomUpdateSerializer
        else:
            return self.serializer_class


class CommentCreateListView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, UserCommentPermission]


class HotelViewSet(viewsets.ModelViewSet):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.prefetch_related('owner').all()
    permission_classes = [permissions.IsAuthenticated, OwnerEditHotelPermission]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(hotel=self.kwargs['hotels_pk'])


class CommentDeleteUpdateView(mixins.DestroyModelMixin,
                              mixins.UpdateModelMixin,
                              generics.GenericAPIView):
    queryset = Comment.objects.select_related('user').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, UserCommentPermission]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
