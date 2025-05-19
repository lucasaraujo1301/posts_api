from rest_framework import serializers

from core import models


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ["id", "user", "post"]
        read_only_fields = ["id"]
