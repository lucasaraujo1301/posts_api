from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core import models
from core.tests import helpers

BASE_LIKE_URL = reverse("comment:comment-list")


def detail_url(comment_id):
    return reverse("comment:comment-detail", kwargs={"pk": comment_id})


class PublicCommentApiTests(TestCase):
    def setUp(self):
        """
        The setUp function is a special function that gets run before each test.
        It's used to set up any state specific to the execution of the given test case.
        In this case, we're using it to create an APIClient instance, which will be used for making API requests.

        :param self: Represent the instance of the class
        :return: The client
        :doc-author: Trelent
        """
        self.client = APIClient()

    def test_retrieve_comment_unauthorized(self):
        """
        The test_retrieve_user_unauthorized function tests that authentication is required for users.
        The test:
        - Makes a GET request to the ME_URL endpoint (which requires authentication)
        - Asserts that the response status code is 401 unauthorized

        :param self: Represent the instance of the class
        :return: A 401 unauthorized status code
        :doc-author: Trelent
        """
        res = self.client.get(BASE_LIKE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            "Authentication credentials were not provided.", res.data["detail"]
        )

    def test_create_comment_unauthorized(self):
        res = self.client.post(BASE_LIKE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            "Authentication credentials were not provided.", res.data["detail"]
        )


class PrivateCommentApiTests(TestCase):
    def setUp(self):
        self.user = helpers.create_user(
            email="test2@example.com", password="testpass123", name="Test Name"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post = helpers.create_post(title="test", content="testcontent")
        self.comment = helpers.create_comment(
            self.post,
            "test",
            self.user,
        )

    def test_create_comment(self):
        res = self.client.post(
            BASE_LIKE_URL, {"post": self.post.id, "content": "testing"}, format="json"
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post = models.Post.objects.get(pk=self.post.id)
        self.assertEqual(post.comment_count, 2)

    def test_retrieve_comments(self):
        res = self.client.get(BASE_LIKE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 1)

    def test_delete_comment(self):
        url = detail_url(self.comment.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        post = models.Post.objects.get(pk=self.post.id)
        self.assertEqual(post.comment_count, 0)
