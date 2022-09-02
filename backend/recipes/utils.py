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
    shop_list = {}
    for item in ingredients:
        name = item['ingredient__name']
        if name not in shop_list:
            shop_list[name] = {
                'name': item['ingredient__name'],
                'unit': item['ingredient__measurement_unit'],
                'amount': item['amount__sum']
            }
        else:
            shop_list[name]['amount'] += item['amount__sum']
    final_list = 'Список покупок: \n'
    for ingredient in shop_list:
        final_list += (
            f"{shop_list[ingredient]['name']} - "
            f"{shop_list[ingredient]['amount']} "
            f"{shop_list[ingredient]['unit']} \n"
        )
    return final_list
