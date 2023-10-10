from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import RecipeViewSet, dowload_shopping_list

router = SimpleRouter()
router.register(r'', RecipeViewSet)

urlpatterns = [
    path('download_shopping_cart/', dowload_shopping_list),
    path('', include(router.urls))
]
