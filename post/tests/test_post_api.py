from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core import models
from core.tests import helpers

BASE_POST_URL = reverse("post:post-list")


def detail_url(post_id):
    return reverse("post:post-detail", kwargs={"pk": post_id})


class PublicPostApiTests(TestCase):
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

    def test_retrieve_posts_unauthorized(self):
        """
        The test_retrieve_user_unauthorized function tests that authentication is required for users.
        The test:
        - Makes a GET request to the ME_URL endpoint (which requires authentication)
        - Asserts that the response status code is 401 unauthorized

        :param self: Represent the instance of the class
        :return: A 401 unauthorized status code
        :doc-author: Trelent
        """
        res = self.client.get(BASE_POST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            "Authentication credentials were not provided.", res.data["detail"]
        )

    def test_create_posts_unauthorized(self):
        res = self.client.post(BASE_POST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            "Authentication credentials were not provided.", res.data["detail"]
        )


class PrivatePostApiTests(TestCase):
    def setUp(self):
        self.user = helpers.create_user(
            email="test2@example.com", password="testpass123", name="Test Name"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post = helpers.create_post(title="test", content="testcontent")

    def test_retrieve_posts(self):
        res = self.client.get(BASE_POST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data["count"],
            1,
        )

    def test_create_posts(self):
        payload = {
            "title": "test",
            "content": "testcontent",
        }
        res = self.client.post(BASE_POST_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(models.Post.objects.count(), 2)

    def test_update_post(self):
        payload = {"title": "newTest"}

        url = detail_url(self.post.id)

        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], "newTest")

    def test_delete_post(self):
        url = detail_url(self.post.id)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(models.Post.objects.count(), 0)
