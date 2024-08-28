from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class CustomUser(AbstractUser):
    first_name = None
    last_name = None

    telegram_chat_id = models.CharField(max_length=15)
    email = models.EmailField()

    REQUIRED_FIELDS = ['email', 'telegram_chat_id']


class Post(models.Model):
    text = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    temporary_username = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    post = models.ForeignKey(Post, related_name='ratings', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    star = models.PositiveIntegerField(validators=[
                                            MaxValueValidator(5),
                                            MinValueValidator(1)
                                        ])

    class Meta:
        unique_together = ('post', 'author')