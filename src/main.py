import database 
import recipe

def main(): 
    db = recipe.RecipeDatabase(debug=True)

    db.write(recipe.Recipe(name="Tuna pasta"))
    db.write(recipe.Recipe(name="Mushroom pasta"))

    result = db.read("Tuna pasta")
    print(type(result))
    print(result)
    print(db.read_all())

if __name__=="__main__": 
    main()