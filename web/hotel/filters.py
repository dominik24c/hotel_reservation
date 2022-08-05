from django_filters import rest_framework as filters

from .models import Hotel, Room


class HotelFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='startswith')
    country = filters.CharFilter(lookup_expr='startswith')
    city = filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Hotel
        fields = ['is_wifi', 'is_pools']


class RoomFilter(filters.FilterSet):
    price__lte = filters.NumberFilter(field_name='price', lookup_expr='lte')
    price__gte = filters.NumberFilter(field_name='price', lookup_expr='gte')
    #
    size = filters.NumberFilter()
    size__lte = filters.NumberFilter(field_name='size', lookup_expr='lte')
    size__gte = filters.NumberFilter(field_name='size', lookup_expr='gte')

    beds = filters.NumberFilter()
    beds__lte = filters.NumberFilter(field_name='beds', lookup_expr='lte')
    beds__gte = filters.NumberFilter(field_name='beds', lookup_expr='gte')

    class Meta:
        model = Room
        fields = ['price', 'beds', 'size', 'is_shower', 'is_tv', 'is_toilet']
