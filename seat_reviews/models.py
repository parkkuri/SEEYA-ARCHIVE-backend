from django.db import models
from django.contrib.postgres.fields import ArrayField


class Review(models.Model):
    user = models.ForeignKey('accounts.User',
                             related_name='user_reviews',
                             on_delete=models.SET_NULL, null=True)
    image_url_array = ArrayField(models.CharField(max_length=1024),
                                 blank=True, null=True)
    seat_area = models.ForeignKey('concert_halls.SeatArea',
                                  related_name='seat_area_reviews',
                                  on_delete=models.SET_NULL, null=True)
    artist = models.CharField(max_length=128, blank=True, null=True)
    seat_row = models.CharField(max_length=128, blank=True, null=True)
    seat_num = models.CharField(max_length=128, blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField('accounts.User',
                                        related_name='like_reviews',
                                        blank=True)
    if_crawled = models.BooleanField(default=True)

    def __str__(self):
        return 'review_{}'.format(self.id)


class Comment(models.Model):
    user = models.ForeignKey('accounts.User',
                             related_name='comment_users',
                             on_delete=models.CASCADE)
    review = models.ForeignKey('seat_reviews.Review',
                               related_name='review_comments',
                               on_delete=models.CASCADE)
    comment = models.CharField(max_length=1024)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'id:{} comment:{}..'.format(self.id, self.comment[:15])