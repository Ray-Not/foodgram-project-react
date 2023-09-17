from django.urls import path
from djoser.views import UserViewSet

from .views import CreateListView, UserDetailView

urlpatterns = [
    path('', CreateListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('me/', UserViewSet.as_view({'get': 'me'})),
    path('set_password/', UserViewSet.as_view({'post': 'set_password'})),
]
