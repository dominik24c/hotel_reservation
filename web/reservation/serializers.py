from datetime import datetime
from uuid import UUID

from hotel.models import Room
from rest_framework import serializers

from .models import Reservation


def check_availability_of_room(room_id: UUID, start_date: datetime, end_date: datetime,
                               reservation_id: UUID = None) -> None:
    if not Reservation.objects.room_is_available(room_id, start_date, end_date, reservation_id=reservation_id):
        raise serializers.ValidationError("Room is not available! Choose other date.")


class ReservationSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    room = serializers.CharField(source='room.id')

    class Meta:
        model = Reservation
        fields = ['id', 'room', 'start_date', 'end_date']

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('The end date must be greater than start date!')
        return data

    def create(self, validated_data):
        user = self.context.get('request').user
        room = validated_data.pop('room')
        room = Room.objects.filter(id=room['id']).first()

        if room is None:
            raise serializers.ValidationError("Room doesn't exists!")

        check_availability_of_room(room.id, validated_data['start_date'], validated_data['end_date'])

        return Reservation.objects.create(customer=user, room=room, **validated_data)


class ReservationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date']

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('The end date must be greater than start date!')
        return data

    def update(self, instance, validated_data):
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        check_availability_of_room(instance.room.id, start_date, end_date, reservation_id=instance.id)
        instance.start_date = start_date
        instance.end_date = end_date
        instance.save()

        return instance
