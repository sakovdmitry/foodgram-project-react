from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.pagination import RecipePagination
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser, Follow
from .serializers import CustomUserSerializer, FollowSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    pagination_class = RecipePagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        permission_classes=[IsAuthenticated],
        methods=['post', 'delete']
        )
    def subscribe(self, request, id=None):
        if request.method == 'POST':
            data = {'user': request.user.id, 'author': id}
            serializer = FollowSerializer(
                data=data,
                context={'request': request}
                )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                    )
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        author = get_object_or_404(CustomUser, id=id) 
        return self.__unsubscribe(user, author)

    @staticmethod
    def __unsubscribe(user, author):
        if user == author:
            return Response(
                {'errors': 'Вы не можете отписываться от самого себя'},
                status=status.HTTP_400_BAD_REQUEST
                )
        follow = Follow.objects.filter(user=user, author=author)
        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
                {'errors': 'Вы не подписаны на данного автора'},
                status=status.HTTP_400_BAD_REQUEST
                )

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
