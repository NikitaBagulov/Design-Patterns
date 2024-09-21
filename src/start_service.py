from src.abstract_logic import abstract_logic
from src.data_reposity import data_reposity
from src.utils.validator import Validator
from src.utils.recipe_manager import recipe_manager
from src.models.group import group_model
from src.models.range import range_model
from src.models.nomenclature import nomenclature_model
from src.models.step import step_model
from src.models.recipe import recipe_model
from src.settings_manager import settings_manager
from src.models import settings

class start_service(abstract_logic):
    __reposity: data_reposity = None
    __settings_manager: settings_manager = None
    __recipe_manager: recipe_manager = None

    def __init__(self, reposity: data_reposity, manager: settings_manager, rec_manager: recipe_manager) -> None:
        super().__init__()
        Validator.validate_not_none(reposity, "Reposity")
        Validator.validate_type(reposity, data_reposity, "Reposity")
        
        Validator.validate_not_none(manager, "Settings Manager")
        Validator.validate_type(manager, settings_manager, "Settings Manager")
        
        Validator.validate_not_none(rec_manager, "Recipe Manager")
        Validator.validate_type(rec_manager, recipe_manager, "Recipe Manager")

        self.__reposity = reposity
        self.__settings_manager = manager
        self.__recipe_manager = rec_manager

    @property 
    def settings(self) -> settings:
        return self.__settings_manager.settings

    def __create_nomenclature_groups(self):
        list = []
        list.append(group_model.default_group_cold())
        list.append(group_model.default_group_source())
        self.__reposity.data[data_reposity.group_key()] = list    

    def __create_nomenclature(self):
        ingredients = self.__recipe_manager.extract_ingredients()
        self.__reposity.data[data_reposity.nomenclature_key()] = ingredients

    def __create_range(self):
        list_units = []
        list_units.append(range_model.default_unit_kg())
        list_units.append(range_model.default_unit_piece())
        list_units.append(range_model.default_unit_gram())
        self.__reposity.data[data_reposity.range_key()] = list_units

    def __create_receipts(self):
        ingredients_data = self.__recipe_manager.extract_ingredients()
        steps_data = self.__recipe_manager.extract_steps()
        servings_data = self.__recipe_manager.extract_servings()

        recipes = []

        for file_idx, ingredients in enumerate(ingredients_data):
            recipe = recipe_model()
            recipe.name = f"Рецепт {file_idx + 1}"
            recipe.servings = servings_data[file_idx]

            for ingredient in ingredients:
                name, quantity, unit = ingredient
                nomenclature_model_instance = nomenclature_model()
                nomenclature_model_instance.name = name
                nomenclature_model_instance.quantity = float(quantity)

                range_model_instance = range_model()
                range_model_instance.name = unit
                nomenclature_model_instance.unit = range_model_instance

                recipe.add_ingredient(nomenclature_model_instance)

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
