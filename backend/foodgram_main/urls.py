from django.contrib import admin
from django.urls import include, path

from users.views import ListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', ListView.as_view(), name='user-list'),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.authtoken')),
]
