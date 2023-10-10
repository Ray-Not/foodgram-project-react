from django.urls import path, include
from djoser.views import UserViewSet

from rest_framework.routers import DefaultRouter
from .views import UserView, UserDetailView, SubscribeView

router = DefaultRouter()
router.register(r'', UserView)

urlpatterns = [
    path('me/', UserViewSet.as_view({'get': 'me'})),
    path('<int:pk>/', UserDetailView.as_view()),
    path('<int:pk>/subscribe/', SubscribeView.as_view({
        'post': 'subscribe',
        'delete': 'unsubscribe'
    })),
    path('set_password/', UserViewSet.as_view({'post': 'set_password'})),
    path('', include(router.urls)),
]
