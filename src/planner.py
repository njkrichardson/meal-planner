import enum 
import random 
from typing import Optional, Sequence


import recipe

DAYS_IN_WEEK: int = 5

class ProposalStrategies(enum.IntEnum): 
    RANDOM=enum.auto()

class MealPlanner: 
    def __init__(self, db: Optional[recipe.RecipeDatabase]=None, debug: Optional[bool]=False, verbose: Optional[bool]=False): 
        if db is None: 
            self._recipe_database = recipe.RecipeDatabase(debug=debug, verbose=verbose)
        else: 
            self._recipe_database = db
        self._proposal: Sequence[recipe.Recipe] = [] 
        
    @property 
    def proposal(self) -> Sequence[recipe.Recipe]: 
        return self._proposal 

    def generate_proposal(self, strategy: Optional[ProposalStrategies]=ProposalStrategies.RANDOM, index: Optional[int]=None) -> Sequence[recipe.Recipe]: 
        all_recipes: Sequence[recipe.Recipe] = self._recipe_database.read_all()
        if len(all_recipes) < DAYS_IN_WEEK: 
            raise ValueError(f"Not enough recipes (only {len(all_recipes)} in the database) to fill a week of meals!")
        if strategy == ProposalStrategies.RANDOM: 
            if index is None: 
                self._proposal = random.sample(all_recipes, DAYS_IN_WEEK)
            else: 
                self._proposal[index] = random.choice(all_recipes)
        else: 
            raise NotImplementedError(f"Proposal strategy {strategy} is not supported.")

        return self.proposal 