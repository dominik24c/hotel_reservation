from django.urls import path, include
from rest_framework_nested import routers

from .views import CommentViewSet, HotelViewSet, HotelCreateView, \
    CommentCreateView, CommentDeleteUpdateView, HotelDeleteUpdateView, \
    RoomViewSet, RoomUpdateDeleteView, RoomCreateView

router = routers.SimpleRouter()
router.register('hotels', HotelViewSet)
comments_router = routers.NestedSimpleRouter(router, 'hotels', lookup='hotels')
comments_router.register('comments', CommentViewSet, basename='hotel-comments')
rooms_router = routers.NestedSimpleRouter(router, 'hotels', lookup='hotel')
rooms_router.register('rooms', RoomViewSet, basename='hotel-rooms')

app_name = 'hotel'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(comments_router.urls)),
    path('', include(rooms_router.urls)),

    path('create/', HotelCreateView.as_view(), name='create-hotel-view'),
    path('<str:pk>/', HotelDeleteUpdateView.as_view(), name='update-delete-hotel-view'),

    path('comments/create/', CommentCreateView.as_view(), name='create-comment-view'),
    path('comments/<str:pk>/', CommentDeleteUpdateView.as_view(), name='update-delete-comment-view'),

    path('rooms/create/', RoomCreateView.as_view(), name='create-room-view'),
    path('rooms/<str:pk>/', RoomUpdateDeleteView.as_view(), name='update-delete-room-view'),
]
