from core import models
from core.view import BaseModelViewSet
from like import serializers


class LikeModelViewSet(BaseModelViewSet):
    queryset = models.Like.objects.all().order_by("-id")
    serializer_class = serializers.LikeModelSerializer
    http_method_names = ["get", "post", "delete"]
