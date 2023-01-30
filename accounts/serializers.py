from rest_framework.serializers import ModelSerializer
from .models import User


class NicknameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname']


class MyPageSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname', 'email', 'login_method']