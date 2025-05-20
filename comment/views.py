from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response

from core import models
from core.view import BaseModelViewSet
from comment import serializers


class CommentModelViewSet(BaseModelViewSet):
    queryset = models.Comment.objects.all().order_by("-id")
    serializer_class = serializers.CommentModelSerializer
    http_method_names = ["get", "post", "delete"]
    filter_backends = [filters.SearchFilter]
    search_fields = ["=post__id"]

    @action(
        detail=False,
        methods=["get"],
        url_path="posts/(?P<post_id>[^/.]+)",
        url_name="list-by-post",
    )
    def get_comments_by_post_id(self, request, post_id: int):
        queryset = self.get_queryset().filter(post_id=post_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
