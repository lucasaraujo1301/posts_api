from rest_framework import serializers

from core import models


class PostModelSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(
        source="user",
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = models.Post
        fields = [
            "id",
            "title",
            "content",
            "username",
            "user",
            "created_datetime",
            "like_count",
            "comment_count",
        ]
        read_only_fields = [
            "created_datetime",
            "id",
            "username",
            "like_count",
            "comment_count",
        ]
        extra_kwargs = {"user": {"write_only": True}}
