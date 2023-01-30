from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    LOGIN_EMAIL = 'email'
    LOGIN_KAKAO = 'kakao'
    # twitter model 따로 만들 예정
    LOGIN_TWITTER = 'twitter'
    LOGIN_CHOICES = (
        (LOGIN_TWITTER, 'Twitter'),
        (LOGIN_KAKAO, 'Kakao'),
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    kakao_id = models.CharField(max_length=128, null=False, primary_key=True)
    nickname = models.CharField(max_length=128, null=True)
    account_name = models.CharField(max_length=128, null=True)
    profile_image_url = models.TextField(null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True)
    age_range = models.CharField(max_length=16, null=True)
    birth_year = models.CharField(max_length=4, null=True)
    birthday_type = models.CharField(max_length=8, null=True)
    birthday = models.CharField(max_length=8, null=True)
    phone_number = models.CharField(max_length=128, null=True)
    login_method = models.CharField(  # twitter model이 따로 생성되면 지워질 필드
        max_length=16, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'kakao_id'
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return '{}:{}'.format(self.login_method, self.email)
