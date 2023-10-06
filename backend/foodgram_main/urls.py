from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/tags/', include('food.tag_urls')),
    path('api/ingredients/', include('food.ingredient_urls')),
    path('api/recipes/', include('food.recipe_urls')),
]

handler404 = 'core.views.page_not_found'
