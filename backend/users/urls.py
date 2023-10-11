from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

from .views import SubscribeListView, SubscribeView, UserDetailView, UserView

router = DefaultRouter()
router.register(r'', UserView)

urlpatterns = [
    path('me/', UserViewSet.as_view({'get': 'me'})),
    path('<int:pk>/', UserDetailView.as_view()),
    path('<int:pk>/subscribe/', SubscribeView.as_view({
        'post': 'subscribe',
        'delete': 'unsubscribe'
    })),
    path('subscriptions/', SubscribeListView.as_view()),
    path('set_password/', UserViewSet.as_view({'post': 'set_password'})),
    path('', include(router.urls)),
]
