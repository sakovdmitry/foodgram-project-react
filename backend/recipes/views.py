from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientSearchFilter, RecipeFilter
from .models import (
    Cart,
    FavoriteRecipe,
    Ingredient,
    Recipe,
    Tag
)
from .pagination import RecipePagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    RecipeListSerializer,
    TagSerializer,
    FavoriteRecipeSerializer,
    CartSerializer
)
from .utils import generate_shop_list


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = RecipePagination
    permission_classes = [IsAuthorOrReadOnly]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeSerializer

    @staticmethod
    def __create_obj(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def __delete_obj(model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепт не в списке'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def __method_handler(self, request, pk, serializer, model):
        if request.method == 'POST':
            return self.__create_obj(
                request,
                pk,
                serializer
            )
        return self.__delete_obj(
            model,
            request.user,
            pk,
        )

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        return self.__method_handler(
            request,
            pk,
            FavoriteRecipeSerializer,
            FavoriteRecipe
        )

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        return self.__method_handler(request, pk, CartSerializer, Cart)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shop_list = generate_shop_list(request.user)
        return HttpResponse(shop_list, content_type='text/plain')


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    filter_backends = [IngredientSearchFilter, ]
    search_fields = ('name',)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
