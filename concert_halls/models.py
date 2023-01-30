from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ConcertHall(models.Model):
    name = models.CharField(max_length=512)
    address = models.CharField(max_length=1024)
    lat = models.FloatField() # 위도
    lng = models.FloatField() # 경도

    def __str__(self):
        return self.name


class SeatArea(models.Model):
    concert_hall = models.ForeignKey('concert_halls.ConcertHall',
                                     related_name='seat_areas',
                                     on_delete=models.SET_NULL, null=True)
    floor = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    area = models.CharField(max_length=128)

    def __str__(self):
        return '{}층 {}구역'.format(self.floor, self.area)