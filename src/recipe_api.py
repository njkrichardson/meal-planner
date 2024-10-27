from typing import Optional, List

import requests

from ingredients import Ingredient
from recipe import Recipe

API_KEY = '53ddf2df831e8d28f7d194d9451153d1'
application_id = "01f46f06"
url = "https://api.edamam.com/api/recipes/v2"


class RecipeAPI:
    def __init__(self):
        self.request_params = {'type': 'public',
                               'app_key': API_KEY,
                               'app_id': application_id,
                               'q': 'chicken'}

    def query_recipe(self, query: str, num_recipes: Optional[int] = 1):
        response = requests.get(url, params={'type': 'public',
                                             'app_key': API_KEY,
                                             'app_id': application_id,
                                             'q': query}).json()

        if len(response['hits']) == 0:
            return []

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
    recipe_api = RecipeAPI()
    random_recipes = recipe_api.query_recipe(query='chicken', num_recipes=10)
