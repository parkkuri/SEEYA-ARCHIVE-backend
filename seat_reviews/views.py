from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticatedOrReadOnly
from .serializers import SeatReviewListSerializer, SeatReviewDetailSerializer, SeatReviewCreateSerializer,\
    CommentSerializer, SeatReviewImageUploadS3Serializer, ViewComparisonSerializer, ReviewLikeUserSerializer
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.pagination import PageNumberPagination
from .models import Review, Comment
from concert_halls.models import SeatArea
from accounts.models import User
from django.contrib.sessions.models import Session


## Pagination
class Pagination(PageNumberPagination):
    page_size = 6


## Permission
class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


## ViewSet
# s3에 이뷰 이미지 업로드
class ReviewImageUploadViewSet(ModelViewSet):
    queryset = Review.objects.none()
    serializer_class = SeatReviewImageUploadS3Serializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]


# 이미지 제외한 리뷰 CRUD
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    pagination_class = Pagination
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return SeatReviewListSerializer
        elif self.action == 'create':
            return SeatReviewCreateSerializer
        else:
            return SeatReviewDetailSerializer

    def get_queryset(self):
        seat_area_id = self.kwargs['seat_area_id']
        return self.queryset.filter(seat_area=seat_area_id).all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        queryset = self.get_queryset()
        pk = self.kwargs['pk']

        next_id, previous_id = None, None
        next_obj = queryset.filter(id__gt=pk).first()
        if next_obj is not None:
            next_id = next_obj.id

        prev_obj = queryset.filter(id__lt=pk).last()
        if prev_obj is not None:
            previous_id = prev_obj.id

        serialized_data = serializer.data
        serialized_data['previous_id'] = previous_id
        serialized_data['next_id'] = next_id

        return Response(serialized_data)

    def create(self, request, *args, **kwargs):
        session_key = self.request.session.session_key
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        request.data['user'] = user.id
        request.data['seat_area'] = self.kwargs['seat_area_id']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


# 리뷰 댓글 CRUD
class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(review=self.kwargs['review_id'])

    def create(self, request, *args, **kwargs):
        session_key = self.request.session.session_key
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        request.data['user'] = user.id
        request.data['review'] = self.kwargs['review_id']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


# 리뷰 좋아요 추가 및 삭제
class ReviewLikeViewSet(RetrieveModelMixin,
                        UpdateModelMixin,
                        DestroyModelMixin,
                        GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewLikeUserSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # 유저 정보는 세션에서 가져와서 사용
        session_key = self.request.session.session_key
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        like_users = self.get_object().like_users.all()
        if self.request.GET.get('like_review').lower() == 'true' and user not in like_users:
            self.get_object().like_users.add(request.user)
        elif self.request.GET.get('like_review').lower() == 'false' and user in like_users:
            self.get_object().like_users.remove(request.user)
        else:
            return Response(data={'Like User Mismatch'}, status=HTTP_400_BAD_REQUEST)
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=200)

    def get_object(self):
        review_id = self.kwargs['review_id']
        review = self.queryset.get(pk=review_id)
        return review


# 특정 콘서트장, 특정 층, 특정 좌석 리뷰 호출
class CompareViewSet(ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ViewComparisonSerializer

    def get_queryset(self):
        concert_hall_id = self.request.GET.get('concert_hall_id')
        floor = self.request.GET.get('floor')
        seat_area_name = self.request.GET.get('seat_area_name').upper()
        seat_area = SeatArea.objects.filter(concert_hall_id=concert_hall_id, floor=floor, area=seat_area_name).all()
        queryset = self.queryset.filter(seat_area__in=seat_area).all()
        return queryset