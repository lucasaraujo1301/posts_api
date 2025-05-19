from rest_framework.routers import SimpleRouter

from comment import views

app_name = "comment"

router = SimpleRouter()
router.register(r"comment", views.CommentModelViewSet)

urlpatterns = router.urls
