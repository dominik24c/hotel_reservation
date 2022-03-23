from django.urls import path, include
from rest_framework_nested import routers

from .views import CommentViewSet, HotelViewSet, \
    CommentCreateView, CommentDeleteUpdateView

router = routers.SimpleRouter()
router.register('hotels', HotelViewSet)
hotels_router = routers.NestedSimpleRouter(router, 'hotels', lookup='hotels')
hotels_router.register('comment', CommentViewSet, basename='hotel-comments')

app_name = 'hotel'
urlpatterns = [
    # path('rooms/', RoomCreateListView.as_view(), name='create-list-room-view'),
    # path('rooms/<str:pk>', RoomRUDView.as_view(), name='rud-room-view'),
    # path('', HotelCreateListView.as_view(), name='create-list-hotel-view'),
    path('', include(router.urls)),
    path('', include(hotels_router.urls)),
    path('comments/', CommentCreateView.as_view(), name='create-comment-view'),
    path('comments/<str:pk>/', CommentDeleteUpdateView.as_view(), name='update-delete-comment-view'),
    # path('<str:pk>/', HotelRDView.as_view(), name='retrieve-delete-hotel-view'),
    # path('<str:pk>/update/', HotelUpdateView.as_view(), name='update-hotel-view'),
]
