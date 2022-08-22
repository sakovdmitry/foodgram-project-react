from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import CustomUserSerializer
from .models import Cart, FavoriteRecipe, Ingredient, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
    )
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientSerializer(
        many=True
    )
    image = Base64ImageField(
        max_length=None,
        use_url=True,
    )
    text = serializers.CharField()
    cooking_time = serializers.IntegerField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Cart.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source='recipe_image')
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe', 'image', 'cooking_time')

    def validate(self, data):
        request = self.context.get('request')
        recipe = data['recipe']
        if FavoriteRecipe.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists():
            raise serializers.ValidationError(
                {'errors': 'Рецепт уже в избранном'}
            )
        return data


class CartSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source='recipe__image')
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Cart
        fields = ('user', 'recipe', 'image', 'cooking_time')

    def validate(self, data):
        request = self.context.get('request')
        recipe = data['recipe']
        if Cart.objects.filter(user=request.user, recipe=recipe).exists():
            raise serializers.ValidationError(
                {'errors': 'Рецепт уже в корзине'}
            )
        return data
