from django.shortcuts import redirect
from rest_framework import viewsets
from .serializers import *
from .models import ConcertHall, SeatArea


class ConcertHallViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ConcertHallSerializer
    queryset = ConcertHall.objects.all()


class SeatAreaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SeatAreaSerializer

    def get_queryset(self):
        concert_hall_id = self.kwargs['concert_hall_id']
        queryset = SeatArea.objects.filter(concert_hall_id=concert_hall_id).all()
        return queryset


def mini_seat_olympic(request):
    return redirect('https://q07w2g2l9e.execute-api.ap-northeast-2.amazonaws.com/seeya/mini-seat-olympic')


def seat_olympic(request):
    return redirect('https://q07w2g2l9e.execute-api.ap-northeast-2.amazonaws.com/seeya/seat-olympic')


def upload_olympic(request):
    return redirect('https://q07w2g2l9e.execute-api.ap-northeast-2.amazonaws.com/seeya/upload-olympic')