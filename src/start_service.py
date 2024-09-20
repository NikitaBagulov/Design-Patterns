from src.abstract_logic import abstract_logic
from src.data_reposity import data_reposity
from src.utils.validator import Validator
from src.utils.work_with_recipe_files import extract_ingredients_from_recipes, extract_steps_from_recipes, extract_servings_from_recipes
from src.models.group import group_model
from src.models.range import range_model
from src.models.ingredient import ingredient_model
from src.models.step import step_model
from src.models.recipe import recipe_model
from src.settings_manager import settings_manager
from src.models import settings

class start_service(abstract_logic):
    __reposity: data_reposity = None
    __settings_manager: settings_manager = None

    def __init__(self, reposity: data_reposity, manager: settings_manager ) -> None:
        super().__init__()
        Validator.validate_not_none(reposity, "Reposity")
        Validator.validate_type(reposity, data_reposity, "Reposity")
        
        Validator.validate_not_none(manager, "Settings Manager")
        Validator.validate_type(manager, settings_manager, "Settings Manager")
        self.__reposity = reposity
        self.__settings_manager = manager

    @property 
    def settings(self) -> settings:
        return self.__settings_manager.settings

    def __create_nomenclature_groups(self):
        list = []
        list.append(group_model.default_group_cold())
        list.append( group_model.default_group_source())
        self.__reposity.data[data_reposity.group_key()] = list    

    def __create_nomenclature(self):
        ingredients = extract_ingredients_from_recipes()
        self.__reposity.data[data_reposity.nomenclature_key()] = ingredients


    def __create_range(self):
        list_units = []
        list_units.append(range_model.default_unit_kg())
        list_units.append(range_model.default_unit_piece())
        list_units.append(range_model.default_unit_gram())
        self.__reposity.data[data_reposity.range_key()] = list_units

    def __create_receipts(self):
        ingredients_data = extract_ingredients_from_recipes()
        steps_data = extract_steps_from_recipes()
        servings = extract_servings_from_recipes()

        recipes = []

        for file_idx, ingredients in enumerate(ingredients_data):
            recipe = recipe_model()
            recipe.name = f"Рецепт {file_idx + 1}"
            recipe.servings = servings[file_idx]
            for ingredient in ingredients:
                name, quantity, unit = ingredient
                ingredient_model_instance = ingredient_model()
                ingredient_model_instance.name = name
                ingredient_model_instance.quantity = float(quantity)
                ingredient_model_instance.unit = unit
                recipe.add_ingredient(ingredient_model_instance)


            for step_number, description in steps_data:
                step = step_model()
                step.step_number = step_number
                step.description = description
                recipe.add_step(step)
            recipes.append(recipe)

        self.__reposity.data[data_reposity.recipes_key()] = recipes

    def create(self):
        self.__create_nomenclature_groups()
        self.__create_nomenclature()
        self.__create_range()
        self.__create_receipts()


    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)    