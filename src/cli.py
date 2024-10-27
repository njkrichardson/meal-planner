import enum 
import random
import sys 
from typing import Sequence

import prompt_toolkit 

import constants
import planner 
import recipe

class InteractionTokens(enum.IntEnum): 
    CONFIRM=enum.auto()
    EXIT=enum.auto()

def main(): 
    # setup the recipe database and planner
    db = recipe.RecipeDatabase()
    meal_planner = planner.MealPlanner(db)

    # initial proposal
    proposed_meals: Sequence[recipe.Recipe] = meal_planner.generate_proposal()

    buttons: list[tuple[str, int]] = list(zip(constants.DAYS_OF_WEEK, range(len(constants.DAYS_OF_WEEK))))
    buttons.extend([
        ("Confirm", InteractionTokens.CONFIRM.name), 
        ("Exit", InteractionTokens.EXIT.name), 
    ]
    )

    while True: 
        result = prompt_toolkit.shortcuts.button_dialog(
            title="Meal Planner CLI",
            text=f"""
            Proposed Meal Plan
            ------------------
            Monday: {proposed_meals[0]!r}
            Tuesday: {proposed_meals[1]!r}
            Wednesday: {proposed_meals[2]!r}
            Thursday: {proposed_meals[3]!r}
            Friday: {proposed_meals[4]!r}
            """,
            buttons=buttons,
        ).run()

        if result == InteractionTokens.EXIT.name: 
            prompt_toolkit.shortcuts.clear()
            sys.exit(0)
        elif result == InteractionTokens.CONFIRM.name: 
            print("Confirmed meal plan...")
            break
        else: 
            assert isinstance(result, int)
            proposed_meals = meal_planner.generate_proposal(index=result)
            
if __name__=="__main__": 
    main()