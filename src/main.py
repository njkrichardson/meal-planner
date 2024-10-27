import copy 
import sqlalchemy 

import ingredients
import planner 
import recipe
from recipe_api import query_recipe_api

def main(): 
    db = recipe.RecipeDatabase()

    # @solodova 1. read something from the external API
    # @solodova 2. convert to out internal format?
    # @solodova 3. write to db
    random_recipes = query_recipe_api(query='chicken', num_recipes=1)

    try:
        db.write(random_recipes[0])
    except sqlalchemy.exc.IntegrityError:
        pass

    # read the random recipe entry
    result = db.read('Shredded chicken')
    print(type(result))
    print(result)

    # write a few recipes to the db (if you haven't yet) 
    try: 
        tuna = ingredients.Ingredient(name="tuna", weight=250, quantity=None, quantity_measure=None) # quantities in g by default
        mushrooms = ingredients.Ingredient(name="mushrooms", weight=300, quantity=None, quantity_measure=None)
        pasta = ingredients.Ingredient(name="pasta", weight=500, quantity=None, quantity_measure=None)

        tuna_pasta = recipe.Recipe(name="Tuna pasta", ingredients=[tuna, pasta])
        mushroom_pasta = recipe.Recipe(name="Mushroom pasta", ingredients=[mushrooms, pasta])
        tuna_mushrooms = recipe.Recipe(name="Tuna and mushrooms", ingredients=[mushrooms, tuna])

        db.write(tuna_pasta)
        db.write(mushroom_pasta)
        db.write(tuna_mushrooms)

    except sqlalchemy.exc.IntegrityError: 
        # already wrote these to the db! 
        pass

    # read the tuna pasta entry 
    result = db.read("Tuna pasta")
    print(type(result))
    print(result)

    # read everything in the db 
    print(db.read_all())

    # using the planner 
    meal_planner = planner.MealPlanner(db)
    proposal = meal_planner.generate_proposal(planner.ProposalStrategies.RANDOM)

    print(f"Proposed meal plan: {proposal}")

if __name__=="__main__": 
    main()