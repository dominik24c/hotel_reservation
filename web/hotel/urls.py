from django.urls import path, include
from rest_framework_nested import routers

from .views import CommentViewSet, HotelViewSet, RoomViewSet

router = routers.SimpleRouter()
router.register('hotels', HotelViewSet)
comments_router = routers.NestedSimpleRouter(router, 'hotels', lookup='hotel')
comments_router.register('comments', CommentViewSet, basename='hotel-comments')
rooms_router = routers.NestedSimpleRouter(router, 'hotels', lookup='hotel')
rooms_router.register('rooms', RoomViewSet, basename='hotel-rooms')

app_name = 'hotel'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(comments_router.urls)),
    path('', include(rooms_router.urls)),
]
