from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions

from .models import Customer, HotelOwner
from .permissions import OwnerPermission
from .serializers import UserSerializer, ListUserSerializer, UserRUDSerializer


class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CustomerListView(generics.ListAPIView):
    serializer_class = ListUserSerializer
    queryset = Customer.objects.all()


class HotelOwnerListView(generics.ListAPIView):
    serializer_class = ListUserSerializer
    queryset = HotelOwner.objects.all()


class UserRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserRUDSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, OwnerPermission]

# login, token refresh token
