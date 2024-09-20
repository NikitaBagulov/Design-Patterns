from src.abstract_model import abstract_model
from src.utils.validator import Validator
from src.models.ingredient import ingredient_model
from src.models.step import step_model

class recipe_model(abstract_model):
    __name: str = ""
    __servings: int = 1
    __ingredients: list[ingredient_model] = []
    __steps: list[step_model] = []

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        Validator.validate_type(value, str, "name")
        Validator.validate_non_empty(value, "name")
        self.__name = value.strip()

    @property
    def servings(self) -> int:
        return self.__servings
    
    @servings.setter
    def servings(self, value: int):
        Validator.validate_positive_integer(value, "servings")
        self.__servings = value

    @property
    def ingredients(self) -> list:
        return self.__ingredients

    def add_ingredient(self, ingredient: ingredient_model):
        Validator.validate_type(ingredient, ingredient_model, "ingredient")
        self.__ingredients.append(ingredient)

    @property
    def steps(self) -> list:
        return self.__steps

    def add_step(self, step: step_model):
        Validator.validate_type(step, step_model, "step")
        self.__steps.append(step)

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)

    def __repr__(self) -> str:
        return (
            f"<RecipeModel(name={self.__name}, "
            f"servings={self.__servings}, "
            f"ingredients_count={len(self.__ingredients)}, "
            f"steps_count={len(self.__steps)})>"
        )