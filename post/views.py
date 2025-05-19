from rest_framework import filters

from core import models
from core.view import BaseModelViewSet
from post import serializers


class PostModelViewSet(BaseModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostModelSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["created_datetime"]
    ordering = ["-created_datetime"]
    search_fields = ["user__username", "title"]
