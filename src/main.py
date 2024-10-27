import copy 
import sqlalchemy 

import ingredients
import planner 
import recipe

def main(): 
    db = recipe.RecipeDatabase()

    # @solodova 1. read something from the external API 
    
    # @solodova 2. convert to out internal format? 

    # @solodova 3. write to db 

    # write a few recipes to the db (if you haven't yet) 
    try: 
        tuna = ingredients.Ingredient(name="tuna", quantity=250) # quantities in g by default
        mushrooms = ingredients.Ingredient(name="mushrooms", quantity=300)
        pasta = ingredients.Ingredient(name="pasta", quantity=500)
        pepper = ingredients.Ingredient(name="pepper", quantity=500)

        tuna_pasta = recipe.Recipe(name="Tuna pasta", ingredients=[tuna, pasta])
        mushroom_pasta = recipe.Recipe(name="Mushroom pasta", ingredients=[mushrooms, pasta])
        tuna_mushrooms = recipe.Recipe(name="Tuna and mushrooms", ingredients=[mushrooms, tuna])
        tuna_mushrooms_pepper = recipe.Recipe(name="Tuna and mushrooms and pepper", ingredients=[mushrooms, tuna, pepper])
        pasta_mushrooms_pepper = recipe.Recipe(name="Pasta and mushrooms and pepper", ingredients=[pasta, mushrooms, pepper])

        db.write(tuna_pasta)
        db.write(mushroom_pasta)
        db.write(tuna_mushrooms)
        db.write(tuna_mushrooms_pepper)
        db.write(pasta_mushrooms_pepper)

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