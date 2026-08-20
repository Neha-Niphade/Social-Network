from rest_framework import serializers
from .models import Tweet, Comment


class TweetSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    likes_count = serializers.IntegerField(
        source="likes.count",
        read_only=True
    )

    comments_count = serializers.IntegerField(
        source="comments.count",
        read_only=True
    )

    bookmarks_count = serializers.IntegerField(
        source="bookmarks.count",
        read_only=True
    )

    class Meta:
        model = Tweet
        fields = [
            "id",
            "username",
            "text",
            "photo",
            "likes_count",
            "comments_count",
            "bookmarks_count",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "username",
            "likes_count",
            "comments_count",
            "bookmarks_count",
            "created_at",
        ]


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    likes_count = serializers.IntegerField(
        source="likes.count",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "username",
            "tweet",
            "text",
            "likes_count",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "username",
            "likes_count",
            "created_at",
        ]