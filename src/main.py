import sqlalchemy 

import database 
import recipe

def main(): 
    db = recipe.RecipeDatabase()

    # write a few recipes to the db (if you haven't yet) 
    try: 
        db.write(recipe.Recipe(name="Tuna pasta"))
        db.write(recipe.Recipe(name="Mushroom pasta"))
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