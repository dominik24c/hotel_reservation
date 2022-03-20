from django.urls import path

from .views import HotelCreateListView, HotelRDView, HotelUpdateView, \
    RoomCreateListView

app_name = 'hotel'
urlpatterns = [
    path('rooms/', RoomCreateListView.as_view(), name='create-list-room-view'),
    path('', HotelCreateListView.as_view(), name='create-list-hotel-view'),
    path('<str:pk>/', HotelRDView.as_view(), name='retrieve-delete-hotel-view'),
    path('<str:pk>/update/', HotelUpdateView.as_view(), name='update-hotel-view'),
]
