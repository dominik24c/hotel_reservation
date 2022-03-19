from base.view_utils import create_view_handlers
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions

from .models import Customer, HotelOwner
from .permissions import OwnerPermission
from .serializers import UserSerializer, ListUserSerializer, UserRUDSerializer


class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.prefetch_related('groups', 'profile').all()

    def create(self, request, *args, **kwargs):
        return create_view_handlers(self, request, {'message': 'User was created!'}, *args, **kwargs)


class CustomerListView(generics.ListAPIView):
    serializer_class = ListUserSerializer
    queryset = Customer.objects.prefetch_related('groups', 'profile').all()


class HotelOwnerListView(generics.ListAPIView):
    serializer_class = ListUserSerializer
    queryset = HotelOwner.objects.prefetch_related('groups', 'profile').all()


class UserRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserRUDSerializer
    queryset = User.objects.prefetch_related('groups', 'profile').all()
    permission_classes = [permissions.IsAuthenticated, OwnerPermission]
