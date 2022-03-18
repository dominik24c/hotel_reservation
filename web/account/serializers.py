from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers

from .groups import GROUPS
from .models import Profile


class ListUserSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='profile.country')
    date_of_birth = serializers.DateField(source='profile.date_of_birth')

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'country',
            'date_of_birth'
        ]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class BaseUserSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='profile.country', required=False)
    date_of_birth = serializers.DateField(source='profile.date_of_birth', required=False)
    groups = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'groups',
            'country',
            'date_of_birth'
        ]


class UserSerializer(BaseUserSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    group_name = serializers.CharField(source='groups.name', write_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'password', 'group_name'] + BaseUserSerializer.Meta.fields
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        group_data = validated_data.pop('groups')

        group = Group.objects.filter(name=group_data['name']).first()
        if group is None:
            raise serializers.ValidationError(f"This group doesn't exist! Only {', '.join(GROUPS)} is allowed!")

        password = validated_data.pop('password')
        profile_data = validated_data.pop('profile')
        user = User(**validated_data)
        user.set_password(password)
        profile = Profile(**profile_data)
        profile.user = user

        with transaction.atomic():
            user.save()
            user.groups.add(group)
            profile.save()

        return user


class UserRUDSerializer(BaseUserSerializer):
    """ Retrieve update delete serializer"""

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields

    def update(self, instance, validated_data):
        profile = validated_data.pop('profile')
        instance.profile.country = profile.get('country', instance.profile.country).lower()
        instance.profile.date_of_birth = profile.get('date_of_birth', instance.profile.date_of_birth)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.first_name = validated_data.get('first_name', instance.first_name)

        with transaction.atomic():
            instance.save()
            instance.profile.save()
        return instance
