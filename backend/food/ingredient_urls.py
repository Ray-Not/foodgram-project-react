from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import IngredientViewSet

router = SimpleRouter()
router.register('', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
