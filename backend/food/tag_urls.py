from rest_framework.routers import SimpleRouter
from .views import TagViewSet
from django.urls import include, path

router = SimpleRouter()
router.register('', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
