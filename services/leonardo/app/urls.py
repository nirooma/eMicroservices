from rest_framework.routers import DefaultRouter

from app.views.category_view import CategoryViewSet

router = DefaultRouter()

router.register("categories", CategoryViewSet)

urlpatterns = router.urls


