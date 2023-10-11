from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Subscribe, User
from .serializers import CustomUserSerializer, SubscribeSerializer


class ListPagination(PageNumberPagination):
    """Паджинатор с лимитом"""
    page_size = 5
    page_size_query_param = 'limit'


class UserView(ModelViewSet):
    """Создание/представление пользоватлей"""
    queryset = User.objects.all().order_by('id')
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny, ]
    pagination_class = ListPagination


class UserDetailView(RetrieveAPIView):
    """Представление для получения одного пользователя"""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, ]


class SubscribeView(ModelViewSet):
    """Представление для подписки на пользователя"""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, ]

    @action(detail=True, methods=['POST'], url_path='subscribe')
    def subscribe(self, request, pk=None):
        """Подписка через /subscribe"""
        follow = self.get_object()
        follower = request.user
        is_sub = Subscribe.objects.filter(
            follow=follow,
            follower=follower
        ).exists()
        if follow == follower:
            return Response(
                {"errors": "It's crazy to subscribe to yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if is_sub:
            return Response(
                {"errors": "Subscribe already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        Subscribe.objects.create(
            follow=follow,
            follower=follower
        )
        sub_serializer = SubscribeSerializer(
            follow,
            context={'request': request}
        )
        return Response(sub_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['DELETE'], url_path='subscribe')
    def unsubscribe(self, request, pk=None):
        """Отписка через /subscribe"""
        follow = self.get_object()
        follower = request.user
        is_sub = Subscribe.objects.filter(
            follow=follow,
            follower=follower
        ).exists()
        if not is_sub:
            return Response(
                {"errors": "Subscribe not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        Subscribe.objects.get(
            follow=follow,
            follower=follower
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeListView(ListAPIView):
    """Представление для списка фолоувоф"""
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = ListPagination

    def get_serializer_context(self):
        """передача параметра сериализатору для ограничения"""
        context = super().get_serializer_context()
        recipes_limit = self.request.query_params.get('recipes_limit')
        if recipes_limit:
            context['recipes_limit'] = int(recipes_limit)
        return context

    def get_queryset(self):
        """Вернет только пользователей фолоувоф"""
        subscribed_users = Subscribe.objects.filter(
            follower=self.request.user
        ).values_list('follow_id', flat=True)
        return User.objects.filter(id__in=subscribed_users)
