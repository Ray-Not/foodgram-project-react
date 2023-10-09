from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import RecipeViewSet

router = SimpleRouter()
router.register(r'', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
