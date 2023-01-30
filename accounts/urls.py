from django.urls import path
from . import views


urlpatterns = [
    path('kakao_login/', views.kakao_login),
    path('kakao_logout/', views.kakao_logout),
    path('kakao_withdrawal/', views.kakao_withdrawal),
    path('accounts/kakao/login/callback/', views.kakao_login_callback),
    path('set/nickname', views.SetNicknameViewSet.as_view()),
    path('check/nickname/duplicate', views.CheckNicknameDuplicateViewSet.as_view()),
    path('me/', views.MyPageViewSet.as_view()),
]