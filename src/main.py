import sqlalchemy 

import ingredients
import recipe
from recipe_api import RecipeAPI

def main(): 
    db = recipe.RecipeDatabase()

    # @solodova 1. read something from the external API
    # @solodova 2. convert to out internal format?
    # @solodova 3. write to db 
    recipe_api = RecipeAPI()
    random_recipe = recipe_api.query_recipe(query='chicken')

    try:
        db.write(random_recipe)
    except sqlalchemy.exc.IntegrityError:
        pass

    # read the random recipe entry
    result = db.read('Shredded chicken')
    print(type(result))
    print(result)

    # write a few recipes to the db (if you haven't yet) 
    try: 
        tuna = ingredients.Ingredient(name="tuna", quantity=250) # quantities in g by default
        mushrooms = ingredients.Ingredient(name="mushrooms", quantity=300)
        pasta = ingredients.Ingredient(name="pasta", quantity=500)

        tuna_pasta = recipe.Recipe(name="Tuna pasta", ingredients=[tuna, pasta])
        mushroom_pasta = recipe.Recipe(name="Mushroom pasta", ingredients=[mushrooms, pasta])

        db.write(tuna_pasta)
        db.write(mushroom_pasta)
    except sqlalchemy.exc.IntegrityError: 
        # already wrote these to the db! 
        pass

    # read the tuna pasta entry 
    result = db.read("Tuna pasta")
    print(type(result))
    print(result)

    # read everything in the db 
    print(db.read_all())

if __name__=="__main__": 
    main()