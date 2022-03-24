from rest_framework import permissions
from rest_framework import viewsets

from .models import Reservation
from .permissions import UserReservationPermission
from .serializers import ReservationSerializer, ReservationUpdateSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, UserReservationPermission]

    def get_queryset(self):
        return Reservation.objects.filter(customer=self.request.user)

    def get_serializer_class(self):
        if self.action == 'update':
            return ReservationUpdateSerializer
        return self.serializer_class
