from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models
from core.tests import helpers


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """
        The test_create_user_with_email_successful function tests that creating a new user with an email is successful

        :param self: Represent the instance of the class
        :return: A user object
        :doc-author: Trelent
        """
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        The test_new_user_email_normalized function tests that the email address is normalized before saving it to
        the database.
        The test_new_user_email_normalized function creates a list of sample emails and their expected normalized
        versions.
        It then loops through each sample email, creating a user with that email address, and asserts that the user's
        actual email matches its expected normalized version.

        :param self: Access the attributes and methods of the class in python
        :return: A list of tuples
        :doc-author: Trelent
        """
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(expected, user.email)

    def test_new_user_without_email_raises_error(self):
        """
        The test_new_user_without_email_raises_error function tests that a new user without an email address raises
        an error.

        :param self: Represent the instance of the class
        :return: An error if the email is not provided
        :doc-author: Trelent
        """

        with self.assertRaises(ValueError) as cm:
            get_user_model().objects.create_user("", "sample123")

        exception = cm.exception
        self.assertEqual(str(exception), "Email must be provided.")

    def test_new_user_with_email_raises_error(self):
        """
        The test_new_user_with_email_raises_error function tests that the create_user function raises an error if we
        try to pass in a non-string email address.
        We use the assertRaises method of unittest.TestCase to test for this behavior.

        :param self: Access the instance of the class
        :return: An exception
        :doc-author: Trelent
        """
        with self.assertRaises(TypeError) as cm:
            get_user_model().objects.create_user(123, "sample123")

        exception = cm.exception
        self.assertEqual(str(exception), "Email must be an string.")

    def test_create_superuser(self):
        """
        The test_create_superuser function is a test case that checks if the create_superuser function
        in our custom user model works as expected. We first call the create_superuser function with some
        test data and then assert that it returns a user object, which has is_staff and is_superuser set to True.

        :param self: Represent the instance of the class
        :return: A user object
        :doc-author: Trelent
        """
        user = get_user_model().objects.create_superuser("test@example.com", "test123")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_post(self):
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(email=email, password=password)

        post = models.Post.objects.create(
            title="Test Post", content="Test Content", user=user
        )

        self.assertIsNotNone(post)
        self.assertEqual(post.user.id, user.id)

    def test_create_like(self):
        email = "test2@example.com"
        password = "testpass123"
        user = helpers.create_user(email=email, password=password)
        post = helpers.create_post(title="Test Post", content="Test Content")

        like = models.Like.objects.create(post=post, user=user)

        self.assertEqual(like.post.id, post.id)
        self.assertEqual(post.like_count, 1)

    def test_delete_like(self):
        email = "test2@example.com"
        password = "testpass123"
        user = helpers.create_user(email=email, password=password)
        post = helpers.create_post(title="Test Post", content="Test Content")

        like = models.Like.objects.create(post=post, user=user)

        self.assertEqual(post.like_count, 1)

        like.delete()

        self.assertEqual(post.like_count, 0)

    def test_create_comment(self):
        email = "test2@example.com"
        password = "testpass123"
        user = helpers.create_user(email=email, password=password)
        post = helpers.create_post(title="Test Post", content="Test Content")

        comment = models.Comment.objects.create(
            content="Test Content", user=user, post=post
        )

        self.assertEqual(comment.post.id, post.id)
        self.assertEqual(comment.user.id, user.id)
        self.assertEqual(post.comment_count, 1)

    def test_delete_comment(self):
        email = "test2@example.com"
        password = "testpass123"
        user = helpers.create_user(email=email, password=password)
        post = helpers.create_post(title="Test Post", content="Test Content")

        comment = models.Comment.objects.create(
            content="Test Content", user=user, post=post
        )

        self.assertEqual(post.comment_count, 1)

        comment.delete()

        self.assertEqual(post.comment_count, 0)
