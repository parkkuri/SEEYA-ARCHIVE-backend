from django.urls import path, include
from rest_framework import routers
from .views import CommentViewSet, ReviewViewSet, ReviewImageUploadViewSet, CompareViewSet, ReviewLikeViewSet

comment_router = routers.SimpleRouter(trailing_slash=False)
comment_router.register('comments', CommentViewSet, basename='comment')

compare_router = routers.SimpleRouter(trailing_slash=False)
compare_router.register('compare', CompareViewSet, basename='comparison')

review_image_router = routers.SimpleRouter(trailing_slash=False)
review_image_router.register('review_images', ReviewImageUploadViewSet, basename='review_image')

review_router = routers.SimpleRouter(trailing_slash=False)
review_router.register('reviews', ReviewViewSet, basename='review')


urlpatterns = [
    # 댓글
    path('reviews/<int:review_id>/', include(comment_router.urls)),
    # 비교
    path('', include(compare_router.urls)),
    # s3에 리뷰 이미지 업로드
    path('s3/upload/', include(review_image_router.urls)),
    # 리뷰 (이미지 제외)
    path('seat_areas/<int:seat_area_id>/', include(review_router.urls)),
    # 좋아요
    path('reviews/<int:review_id>/likes', ReviewLikeViewSet.as_view()),
]