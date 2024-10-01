from src.core.abstract_model import abstract_model
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
        if other_object is None:
            return False
        if not isinstance(other_object, abstract_model):
            return False

        return self.unique_code == other_object.unique_code
     
    def __str__(self) -> str:
        ingredients_str = ', '.join(str(ingredient) for ingredient in self.__ingredients)
        steps_str = ', '.join(str(step) for step in self.__steps)
        return (
            f"<RecipeModel(name='{self.__name}', "
            f"servings={self.__servings}, "
            f"ingredients=[{ingredients_str}], "
            f"steps=[{steps_str}])>"
        )

    def _deserialize_additional_fields(self, data: dict):
        """
        Десериализация дополнительных полей для recipe_model.
        """
        if 'servings' in data:
            servings = data['servings']
            Validator.validate_positive_integer(servings, "servings")
            self.servings = servings

        if 'ingredients' in data and isinstance(data['ingredients'], list):
            for ingredient_data in data['ingredients']:
                ingredient_instance = ingredient_model()
                ingredient_instance.deserialize(ingredient_data)
                self.add_ingredient(ingredient_instance)

        if 'steps' in data and isinstance(data['steps'], list):
            for step_data in data['steps']:
                step_instance = step_model()
                step_instance.deserialize(step_data) 
                self.add_step(step_instance)