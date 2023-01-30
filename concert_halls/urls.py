from django.urls import include, path
from rest_framework import routers
from . import views

concert_hall_router = routers.SimpleRouter(trailing_slash=False)
concert_hall_router.register('concert_halls', views.ConcertHallViewSet, basename='concert_hall')

seat_area_router = routers.SimpleRouter(trailing_slash=False)
seat_area_router.register('seat_areas', views.SeatAreaViewSet, basename='seat_area')


urlpatterns = [
    path('', include(concert_hall_router.urls)),
    path('concert_halls/<int:concert_hall_id>/', include(seat_area_router.urls)),
    path('mini_seat_olympic/', views.mini_seat_olympic),
    path('seat_olympic/', views.seat_olympic),
    path('upload_olympic/', views.upload_olympic),
]