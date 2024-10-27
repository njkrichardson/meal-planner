import sqlalchemy 

import database 
import ingredients
import recipe

def main(): 
    db = recipe.RecipeDatabase()

    # @solodova 1. read something from the external API 
    
    # @solodova 2. convert to out internal format? 

    # @solodova 3. write to db 

    # write a few recipes to the db (if you haven't yet) 
    try: 
        tuna = ingredients.Ingredient(name="tuna")
        mushrooms = ingredients.Ingredient(name="mushrooms")
        pasta = ingredients.Ingredient(name="pasta")

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