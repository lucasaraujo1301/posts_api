from core import models
from core.view import BaseModelViewSet
from comment import serializers


class CommentModelViewSet(BaseModelViewSet):
    queryset = models.Comment.objects.all().order_by("-id")
    serializer_class = serializers.CommentModelSerializer
    http_method_names = ["get", "post", "delete"]
