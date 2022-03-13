from django.contrib.auth.models import User, Group
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
    country = serializers.CharField(source='profile.country')
    date_of_birth = serializers.DateField(source='profile.date_of_birth')
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
        password = validated_data.pop('password')
        group_data = validated_data.pop('groups')
        profile_data = validated_data.pop('profile')
        user = User(**validated_data)
        user.set_password(password)
        profile = Profile(**profile_data)

        group = Group.objects.filter(name=group_data['name']).first()
        if group is None:
            serializers.ValidationError(f"This group doesnt exists! Only [{', '.join(GROUPS)}] is allowed")

        profile.user = user

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

        country = profile.get('country')
        if country is not None:
            instance.profile.country = country.lower()

        date_of_birth = profile.get('date_of_birth')
        if date_of_birth is not None:
            instance.profile.date_of_birth = date_of_birth

        last_name = validated_data.get('last_name')
        if last_name is not None:
            instance.last_name = last_name

        first_name = validated_data.get('first_name')
        if first_name is not None:
            instance.first_name = first_name

        instance.save()
        return instance
