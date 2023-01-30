import boto3
import uuid
from datetime import datetime
from accounts.models import User
from django.conf import settings
from rest_framework.exceptions import APIException
from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)
from .models import Review, Comment


# AWS
AWS_ACCESS_KEY_ID = settings.SOCIAL_OAUTH_CONFIG['MY_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = settings.SOCIAL_OAUTH_CONFIG['MY_AWS_SECRET_ACCESS_KEY']
AWS_REGION = settings.SOCIAL_OAUTH_CONFIG['AWS_REGION']
AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
AWS_ROOT_STORAGE_BUCKET_NAME = settings.SOCIAL_OAUTH_CONFIG['AWS_ROOT_STORAGE_BUCKET_NAME']
AWS_S3_CUSTOM_DOMAIN = settings.AWS_S3_CUSTOM_DOMAIN


## Exception

class ImageRequiredException(APIException):
    status_code = 204
    default_detail = "Image is Required"
    default_code = "NoContent"


class TooManyImagesException(APIException):
    status_code = 413
    default_detail = "Too Many Images. Max Size is 5"
    default_code = "RequestEntityTooLarge"


## Serializer

class LikeUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "nickname"]


class ReviewLikeUserSerializer(ModelSerializer):
    like_users = LikeUserSerializer(many=True, read_only=True)
    like_user_count = SerializerMethodField()

    class Meta:
        model = Review
        fields = ["like_user_count", "like_users"]

    def get_like_user_count(self, obj):
        return obj.like_users.count()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "kakao_id", "nickname"]
        read_only_fields = ["id"]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "review", "user", "comment", "create_at", "update_at"]
        read_only_fields = ["id"]


class SeatReviewImageUploadS3Serializer(Serializer):
    def to_representation(self, image_url_list):
        image_dict = {'image_urls': image_url_list}
        return image_dict

    def create(self, validate_data):
        images_data = self.context["request"].FILES

        if len(images_data.getlist("image")) > 5:
            raise TooManyImagesException
        if len(images_data.getlist("image")) == 0:
            raise ImageRequiredException

        current_date = datetime.now().strftime('%Y_%m_%d-%H:%M:%S')
        image_url_list = []
        s3r = boto3.resource(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        for image_data in images_data.getlist('image'):
            image_data._set_name(str(uuid.uuid4()))
            s3r.Bucket(AWS_ROOT_STORAGE_BUCKET_NAME).put_object(
                Key='%s/%s-%s' % (AWS_STORAGE_BUCKET_NAME, current_date, image_data),
                Body=image_data,
                ContentType='jpg',
            )
            image_url_list.append(
                AWS_S3_CUSTOM_DOMAIN
                + '%s/%s-%s' % (AWS_STORAGE_BUCKET_NAME, current_date, image_data)
            )
        return self.to_representation(image_url_list)


class SeatReviewListSerializer(ModelSerializer):
    preview_image = SerializerMethodField()
    image_url_array = SerializerMethodField()
    like_users = SerializerMethodField()
    nickname = SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id',
            'seat_area',
            'user',
            'nickname',
            'review',
            'like_users',
            'preview_image',
            'image_url_array',
        ]
        read_only_fields = ['id']

    def get_preview_image(self, obj): # DB상 첫 번째 이미지가 preview image
        return obj.image_url_array[0]

    def get_image_url_array(self, obj):
        return obj.image_url_array

    def get_like_users(self, obj):
        return obj.like_users.count()

    def get_nickname(self, obj):
        return obj.user.nickname


class SeatReviewCreateSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'seat_area',
            'user',
            'image_url_array',
            'review',
            'create_at']
        read_only_fields = ['id']


class SeatReviewDetailSerializer(ModelSerializer):
    seat_area = SerializerMethodField()
    concert_hall_name = SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    user = UserSerializer(many=False, read_only=True)
    like_users = LikeUserSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'seat_area',
            'concert_hall_name',
            'image_url_array',
            'create_at',
            'update_at',
            'review',
            'review_comments',
            'like_users'
        ]
        read_only_fields = ['id']

    def get_seat_area(self, obj):
        return obj.seat_area.area

    def get_concert_hall_name(self, obj):
        return obj.seat_area.concert_hall.name


class ViewComparisonSerializer(ModelSerializer):
    count_like_users = SerializerMethodField(source="like_users")
    thumbnail_image = SerializerMethodField(source="image_url_array")
    user_nickname = SerializerMethodField()
    count_comments = SerializerMethodField()
    seat_area_name = SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id',
            'user_nickname',
            'thumbnail_image',
            'seat_area_name',
            'review',
            'create_at',
            'count_like_users',
            'count_comments',
        ]
        read_only_fields = ['id']

    def get_count_like_users(self, obj):
        return obj.like_users.count()

    def get_thumbnail_image(self, obj):
        return obj.image_url_array[0]

    def get_user_nickname(self, obj):
        return obj.user.nickname

    def get_count_comments(self, obj):
        return obj.comments.count()

    def get_seat_area_name(self, obj):
        return obj.seat_area.area
