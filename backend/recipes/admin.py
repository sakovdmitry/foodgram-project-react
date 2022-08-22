from django.contrib import admin

from .models import (
    Recipe,
    Ingredient,
    FavoriteRecipe,
    RecipeIngredient,
    Cart,
    Tag
)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',)
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ('count_favorites',)

    def count_favorites(self, obj):
        return obj.favorites.count()

    count_favorites.short_description = (
        'Количество добавлений рецепта в избранное'
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
