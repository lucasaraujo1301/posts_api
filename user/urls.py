from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from user import views


app_name = "user"

urlpatterns = [
    path("auth/register/", views.CreateUserView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("user/me/", views.ManageUserView.as_view(), name="me"),
]
