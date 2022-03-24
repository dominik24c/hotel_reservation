from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ReservationViewSet

router = SimpleRouter()
router.register('', ReservationViewSet, basename='reservation')

app_name = 'reservation'

urlpatterns = [
    path('', include(router.urls))
]
