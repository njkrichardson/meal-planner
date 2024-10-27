from typing import Optional, List

import requests

from ingredients import Ingredient
from recipe import Recipe

API_KEY = '53ddf2df831e8d28f7d194d9451153d1'
application_id = "01f46f06"
url = "https://api.edamam.com/api/recipes/v2"

meal_types = ["Breakfast", "Dinner", "Lunch", "Snack", "Teatime"]
dish_types = ["Biscuits and cookies", "Bread", "Cereals", "Condiments and sauces", "Desserts", "Drinks", "Main course",
              "Pancake", "Preps", "Preserve", "Salad", "Sandwiches", "Side dish", "Soup", "Starter", "Sweets"]
cuisine_types = ["American", "Asian", "British", "Caribbean", "Central Europe", "Chinese", "Eastern Europe", "French",
                 "Indian", "Italian", "Japanese", "Kosher", "Mediterranean", "Mexican", "Middle Eastern", "Nordic",
                 "South American", "South East Asian"]


def query_recipe_api(query: str,
                     meal_type: Optional[str] = None,
                     cuisine_type: Optional[str] = None,
                     dish_type: Optional[str] = None,
                     range_num_ingredients: Optional[tuple] = None,
                     num_recipes: Optional[int] = 1):
    if query is None:
        if meal_type is None and cuisine_type is None and dish_type is None and range_num_ingredients is None:
            raise Exception("Must specify query or some other input to api request.")
    if meal_type is not None:
        if meal_type not in meal_types:
            raise Exception(f"{meal_type} not one of valid options: {meal_types}")
    if dish_type is not None:
        if dish_type not in dish_types:
            raise Exception(f"{dish_type} not one of valid options: {dish_types}")
    if cuisine_type is not None:
        if cuisine_type not in cuisine_types:
            raise Exception(f"{cuisine_types} not one of valid options: {cuisine_types}")

    range_num_ingredients_input: Optional[str] = None
    if range_num_ingredients is not None:
        if range_num_ingredients[0] is None:
            range_num_ingredients_input = f"{range_num_ingredients[1]}"
        elif range_num_ingredients[1] is None:
            range_num_ingredients_input = f"{range_num_ingredients[0]}+"
        else:
            range_num_ingredients_input = f"{range_num_ingredients[0]}-{range_num_ingredients[1]}"

    response = requests.get(url, params={'type': 'public',
                                         'app_key': API_KEY,
                                         'app_id': application_id,
                                         'q': query,
                                         'mealType': meal_type,
                                         'dishType': dish_type,
                                         'cuisineType': cuisine_type,
                                         'ingr': range_num_ingredients_input}
                            ).json()

    if len(response['hits']) == 0:
        raise Exception("No recipes found for query.")

    recipes: List[Recipe] = []

    for i, response in enumerate(response['hits']):
        if i == num_recipes:
            break

        response_recipe = response['recipe']

        ingredients: List[Ingredient] = []
        for ingredient in response_recipe['ingredients']:
            ingredients.append(Ingredient(name=ingredient['food'],
                                          quantity=int(ingredient['weight'])))

        recipe: Recipe = Recipe(name=response_recipe['label'],
                                ingredients=ingredients)
        recipes.append(recipe)

    return recipes


if __name__ == "__main__":
    random_recipes = query_recipe_api(query='chicken', num_recipes=10)
