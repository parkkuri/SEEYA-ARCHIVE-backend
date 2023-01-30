from rest_framework import serializers
from .models import ConcertHall, SeatArea


class ConcertHallSerializer(serializers.ModelSerializer):
    concert_hall_id = serializers.IntegerField(source='id')

    class Meta:
        model = ConcertHall
        fields = ['concert_hall_id', 'name', 'address', 'lat', 'lng']


class SeatAreaSerializer(serializers.ModelSerializer):
    count_reviews = serializers.SerializerMethodField()
    seat_area_id = serializers.IntegerField(source='id')

    class Meta:
        model = SeatArea
        fields = ['seat_area_id', 'floor', 'area', 'count_reviews']

    def get_count_reviews(self, obj):
        return obj.seat_area_reviews.count()