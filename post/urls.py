from rest_framework.routers import SimpleRouter

from post import views

app_name = "post"

router = SimpleRouter()
router.register(r"post", views.PostModelViewSet)

urlpatterns = router.urls
