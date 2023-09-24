from rest_framework.routers import SimpleRouter
from .views import IngredientViewSet
from django.urls import include, path

router = SimpleRouter()
router.register('', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
