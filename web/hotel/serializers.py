from account.groups import G_HOTEL_OWNER
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import validators

from .models import Hotel, Room, Comment


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

    # rooms = serializers.HyperlinkedRelatedField(many=True, read_only=True,
    #                                             view_name='hotel:create-list-room-view')

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
        hotel_pk = self.context.get('hotel_pk')
        hotel = Hotel.objects.get(pk=hotel_pk)
        room = Room(hotel=hotel, **validated_data)
        room.save()
        return room


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    date = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'username', 'content', 'rating', 'date']

    def create(self, validated_data):
        request = self.context.get('request')
        hotel_pk = self.context.get('hotel_pk')
        hotel = Hotel.objects.get(pk=hotel_pk)
        return Comment.objects.create(**validated_data, hotel=hotel, user=request.user)


class CommentCreateSerializer(serializers.ModelSerializer):
    pass
#     hotel_id = serializers.CharField(source='hotel.id', write_only=True)
#
#     class Meta:
#         model = Comment
#         fields = ['content', 'rating', 'hotel_id']
#
#     def create(self, validated_data):
#         hotel = validated_data.pop('hotel')
#         hotel_obj = Hotel.objects.filter(id=hotel['id']).first()
#         request = self.context.get('request')
#
#         if hotel_obj is None:
#             raise serializers.ValidationError("Hotel doesn't exist!")
#         return Comment.objects.create(**validated_data, hotel=hotel_obj, user=request.user)
