from django.db import models
from django.core.validators import MinValueValidator

from users.models import CustomUser


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=40,
        blank=False,
        verbose_name='Единица измерения'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='name_unit_uniq'),
        )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    GREEN = '#33B918'
    YELLOW = '#f6fa05'
    BLUE = '#052efa'
    MALACHITE = '#0BDA51'
    SAND = '#FCDD76'
    COBALT = '#0047AB'
    PINK = '#DDA0DD'

    COLORS_CHOICE = [
        (GREEN, 'Зеленый'),
        (YELLOW, 'Желтый'),
        (BLUE, 'Синий'),
        (MALACHITE, 'Малахит'),
        (SAND, 'Песок'),
        (COBALT, 'Кобальт'),
        (PINK, 'Орхидея')
    ]

    name = models.CharField(
        max_length=20,
        blank=False,
        unique=True,
        verbose_name='Название тега'
    )
    color = models.CharField(
        max_length=7,
        choices=COLORS_CHOICE,
        unique=True,
        blank=False,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        max_length=20,
        unique=True,
        blank=False
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=250,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка'
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Список ингредиентов'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=(MinValueValidator(1),),
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    amount = models.FloatField(
        validators=(MinValueValidator(
            0.1,
            message='Укажите количество больше нуля!',
        ),),
        verbose_name='Количество',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient',),
                name='recipe_ingredient_exists'),
        )
        ordering = ['-id']
        verbose_name = 'Количество ингредиентов'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorite',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorite',
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='Избранный рецепт')
        ]


class Cart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='Рецепты в корзине')
        ]
