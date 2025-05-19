from rest_framework.routers import SimpleRouter

from like import views

app_name = "like"

router = SimpleRouter()
router.register(r"like", views.LikeModelViewSet)

urlpatterns = router.urls
