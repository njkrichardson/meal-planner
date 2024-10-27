import requests
from recipe import Recipe
from ingredients import Ingredient

API_KEY = '53ddf2df831e8d28f7d194d9451153d1'
application_id = "01f46f06"
url = "https://api.edamam.com/api/recipes/v2"

class RecipeAPI:
    def __init__(self):
        self.request_params = {'type': 'public',
                               'app_key': API_KEY,
                               'app_id': application_id,
                               'q': 'chicken'}

    def query_recipe(self, query: str):
        response = requests.get(url, params={'type': 'public',
                                             'app_key': API_KEY,
                                             'app_id': application_id,
                                             'q': query}).json()

        response_recipe = response['hits'][0]['recipe']

        ingredients = []
        for ingredient in response_recipe['ingredients']:
            ingredients.append(Ingredient(name=ingredient['food'],
                                          quantity=int(ingredient['weight'])))

        recipe = Recipe(name=response_recipe['label'],
                        ingredients = ingredients)

        return recipe


if __name__=="__main__":
    recipe_api = RecipeAPI()
    random_recipe = recipe_api.query_recipe(query='chicken')
