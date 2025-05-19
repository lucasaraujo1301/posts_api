from rest_framework import serializers

from core import models


class LikeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = ["id", "user", "post"]
        read_only_fields = ["id"]
