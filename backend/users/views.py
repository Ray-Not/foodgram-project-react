from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User
from .serializers import CustomUserSerializer


class UserListPagination(PageNumberPagination):
    """Паджинатор для списка пользователей с лимитом"""
    page_size = 5
    page_size_query_param = 'limit'


class CreateListView(ListCreateAPIView):
    """Дженерик создаст нового пользователя или вернет список"""
    queryset = User.objects.all().order_by('id')
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny, ]
    pagination_class = UserListPagination


class UserDetailView(RetrieveAPIView):
    """Представление для получения одного пользователя"""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, ]
