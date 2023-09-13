from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import CustomRegisterSerializer


class UserListPagination(PageNumberPagination):
    """Паджинатор для списка пользователей с лимитом"""
    page_size = 5
    page_size_query_param = 'limit'


class ListView(ListCreateAPIView):
    """Дженерик, вернет список пользователей или создаст нового"""
    queryset = User.objects.all()
    serializer_class = CustomRegisterSerializer
    permission_classes = [AllowAny]
    pagination_class = UserListPagination
