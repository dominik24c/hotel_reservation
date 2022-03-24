from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import UserListCreateView, CustomerListView, HotelOwnerListView, UserRUDView

app_name = 'account'

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/users/', UserListCreateView.as_view(), name='create-list-view'),
    path('auth/users/<int:pk>/', UserRUDView.as_view(), name='retrieve-update-delete-view'),
    path('customers/', CustomerListView.as_view(), name='customers'),
    path('hotel-owners/', HotelOwnerListView.as_view(), name='hotel-owners')
]
