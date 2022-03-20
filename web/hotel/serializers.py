from account.groups import G_HOTEL_OWNER
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import validators

from .models import Hotel, Room


class HotelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        exclude = ['owner', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': False}, 'description': {'required': False},
            'country': {'required': False}, 'city': {'required': False},
            'street': {'required': False}, 'zip_code': {'required': False},
            'is_wifi': {'required': False}, 'is_pools': {'required': False}
        }


class HotelSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username')
    address = serializers.CharField(source='full_address', read_only=True)
    street = serializers.CharField(write_only=True)
    city = serializers.CharField(write_only=True)
    zip_code = serializers.CharField(write_only=True)
    is_wifi = serializers.BooleanField(required=False)
    is_pools = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    rooms = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                view_name='hotel:create-list-room-view')

    class Meta:
        model = Hotel
        fields = '__all__'

    def create(self, validated_data):
        owner = validated_data.pop('owner')
        user = User.objects.prefetch_related('groups').filter(username=owner['username']).first()

        if user is None:
            raise serializers.ValidationError("User doesn't exist!")
        elif user.groups.first().name != G_HOTEL_OWNER:
            raise serializers.ValidationError("Only Hotel owner can create hotel model!")

        return Hotel.objects.create(**validated_data, owner=user)


class RoomSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    hotel_id = serializers.CharField(source='hotel.id')
    number = serializers.IntegerField(validators=[
        validators.UniqueValidator(
            queryset=Room.objects.all(),
            message='Room with that number has already existed!')
    ])
    is_shower = serializers.BooleanField(required=False)
    is_tv = serializers.BooleanField(required=False)
    is_toilet = serializers.BooleanField(required=False)

    class Meta:
        model = Room
        exclude = ['hotel', 'created_at', 'updated_at']

    def create(self, validated_data) -> Room:
        hotel_data = validated_data.pop('hotel')
        room = Room(**validated_data)
        hotel = Hotel.objects.filter(id=hotel_data['id']).first()
        if hotel is None:
            raise serializers.ValidationError("Hotel was not found!")
        room.hotel = hotel
        return room

#
# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = '__all__'
