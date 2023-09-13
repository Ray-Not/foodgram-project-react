from django.contrib import admin
from django.urls import path, include
from users.views import ListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls.authtoken')),
    path('api/users/', ListView.as_view(), name='user-list'),
]
