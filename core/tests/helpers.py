from django.contrib.auth import get_user_model

from core import models


def create_post(title: str, content: str) -> models.Post:
    email = "test@example.com"
    password = "testpass123"
    user = create_user(email=email, password=password)

    post = models.Post.objects.create(title=title, content=content, user=user)

    return post


def create_user(**params):
    """
    The create_user function creates a user with the given username, email and password.


    :param **params: Pass in a dictionary of parameters to the create_user function
    :return: A user object
    :doc-author: Trelent
    """
    return get_user_model().objects.create_user(**params)


def create_comment(
    post: models.Post, content: str, user: models.User
) -> models.Comment:
    return models.Comment.objects.create(post=post, content=content, user=user)


def create_like(post: models.Post, user: models.User) -> models.Like:
    return models.Like.objects.create(post=post, user=user)
