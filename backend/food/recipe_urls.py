from rest_framework.routers import SimpleRouter
from .views import RecipeViewSet
from django.urls import include, path

router = SimpleRouter()
router.register('', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
