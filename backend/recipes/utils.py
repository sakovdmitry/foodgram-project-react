from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response

from .models import RecipeIngredient


def generate_shop_list(user):
    ingredients = RecipeIngredient.objects.filter(
        recipe__carts__user=user).values(
            'ingredient__name',
            'ingredient__measurement_unit',
    ).annotate(Sum('amount'))
    if not ingredients:
        return Response({'error': 'Ваша корзина пуста'},
                        status=status.HTTP_400_BAD_REQUEST)

    shop_list = 'Список покупок: \n'
    for ingredient in ingredients:
        shop_list += (
            f"{ingredient['ingredient__name']} - "
            f"{ingredient['amount__sum']} "
            f"{ingredient['ingredient__measurement_unit']} \n"
        )
    return shop_list
