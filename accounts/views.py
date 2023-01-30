from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.contrib.auth import login, logout
from django.db.models import Q
if settings.DEBUG:
    from seeyaArchive.settings.development import SOCIAL_OAUTH_CONFIG
else:
    from seeyaArchive.settings.production import SOCIAL_OAUTH_CONFIG
import random, requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import User
from .serializers import MyPageSerializer, NicknameSerializer

KAKAO_REST_API_KEY = SOCIAL_OAUTH_CONFIG['KAKAO_REST_API_KEY']
KAKAO_REDIRECT_URI = SOCIAL_OAUTH_CONFIG['KAKAO_REDIRECT_URI']
KAKAO_SECRET_KEY = SOCIAL_OAUTH_CONFIG['KAKAO_SECRET_KEY']
KAKAO_ADMIN_KEY = SOCIAL_OAUTH_CONFIG['KAKAO_ADMIN_KEY']


## Nickname

# nickname 중복 확인
class CheckNicknameDuplicateViewSet(APIView):
    def get(self, request):
        users = User.objects.filter(~Q(id=self.request.user.pk) &  # 임의의 별명이 설정되어있는 상태이므로 로그인한 유저 제외
                                    Q(nickname=self.request.GET.get('nickname')))
        if users:
            return Response(data=False, status=HTTP_400_BAD_REQUEST)
        return Response(data=True, status=HTTP_200_OK)


# nickname 설정
class SetNicknameViewSet(RetrieveModelMixin,
                         UpdateModelMixin,
                         GenericAPIView):
    queryset = User.objects.all()
    serializer_class = NicknameSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):  # session에서 login한 user 가져옴
        session_key = self.request.session.session_key
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        return user


## ViewSet

class MyPageViewSet(RetrieveModelMixin,
                    GenericAPIView):
    queryset = User.objects.all()
    serializer_class = MyPageSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        session_key = self.request.session.session_key
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        return user


## Kakao

@api_view(['GET'])
def kakao_login(request):
    return redirect(
        f'https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code'
    )


@api_view(['GET'])
def kakao_login_callback(request):
    code = request.GET.get('code', None)
    request_access_token = requests.post(
        f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_REDIRECT_URI}&code={code}&client_secret={KAKAO_SECRET_KEY}',
        headers={'Accept': 'application/json'},
    )
    access_token_json = request_access_token.json()
    access_token = access_token_json.get('access_token')
    profile_request = requests.post(
        'https://kapi.kakao.com/v2/user/me',
        headers={'Content-Type': 'application/x-www-form-urlencoded',
                 'Authorization': f'Bearer {access_token}'},
    )
    # token_info = requests.get(
    #     'https://kapi.kakao.com/v1/user/access_token_info',
    #     headers={'Authorization': f'Bearer {access_token}'},
    # )
    json_response = profile_request.json()
    kakao_account = json_response.get('kakao_account')
    kakao_id = json_response.get('id')
    email = kakao_account.get('email', None)
    gender = kakao_account.get('gender', None)
    birth_year = kakao_account.get('birthyear', None)
    birthday_type = kakao_account.get('birthday_type', None)
    birthday = kakao_account.get('birthday', None)
    age_range = kakao_account.get('age_range', None)
    name = kakao_account.get('name', None)
    profile = kakao_account.get('profile', None)

    profile_image_url = None
    if profile is not None:
        profile_image_url = profile.get('profile_image_url')
    user = User.objects.filter(kakao_id=kakao_id).first()
    # 이미 회원인 유저는 로그인
    if user is not None:
        login(request, user)
        return redirect('https://seeya-archive.com')
    # 새로 가입한 유저 모델에 저장 후 로그인 및 닉네임 설정
    else:
        user = User.objects.create_user(
            kakao_id=kakao_id,
            email=email,
            username=kakao_id,
            nickname=make_random_nickname(kakao_id), # 닉네임은 임의로 생성하여 저장
            profile_image_url=profile_image_url,
            gender=gender,
            age_range=age_range,
            birth_year=birth_year,
            birthday_type=birthday_type,
            birthday=birthday,
            account_name=name,
            login_method=User.LOGIN_KAKAO,
            password=None,
        )
        user.set_unusable_password()
        user.save()
        login(request, user)
        return redirect('https://seeya-archive.com/auth/nickname')


@csrf_exempt
def kakao_logout(request):
    requests.post(
        f'https://kapi.kakao.com/v1/user/logout?target_id_type=user_id&target_id={request.user.kakao_id}',
        headers={'Content-Type': 'application/x-www-form-urlencoded',
                 'Authorization': f'KakaoAK {KAKAO_ADMIN_KEY}'},
    )
    logout(request)
    return redirect('https://seeya-archive.com')


def kakao_withdrawal(request):
    user = User.objects.get(pk=request.user.pk)
    requests.post(
        f'https://kapi.kakao.com/v1/user/unlink?target_id_type=user_id&target_id={request.user.kakao_id}',
        headers={'Content-Type': 'application/x-www-form-urlencoded',
                 'Authorization': f'KakaoAK {KAKAO_ADMIN_KEY}'},
    )
    logout(request)
    user.delete()
    return redirect('https://seeya-archive.com')


# 닉네임 설정 전에 랜덤으로 닉네임을 지어주는 함수
def make_random_nickname(kakao_id):
    random_nickname = str(kakao_id)
    with open('accounts/words.txt', encoding='utf-8') as f:
        nicknames = f.read().splitlines()
    for i in range(2):
        random_nickname += random.choice(nicknames)
    return random_nickname