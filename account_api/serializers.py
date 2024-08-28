from django.db import models
from rest_framework import serializers
from .models import Post, Rating, Comment, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    avarage_rating = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['date_published', 'author', 'avarage_rating']

    def get_avarage_rating(self, obj):
        ratings = obj.ratings.all()
        return ratings.aggregate(models.Avg('star'))['star__avg']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['post', 'date_published', 'author']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'post', 'author', 'star']
        read_only_fields = ['post', 'author']