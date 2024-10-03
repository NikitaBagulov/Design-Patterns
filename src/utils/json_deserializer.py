import json
from src.models.nomenclature import nomenclature_model
from src.models.range import range_model
from src.models.group import group_model
from src.models.ingredient import ingredient_model
from src.models.step import step_model
from src.models.recipe import recipe_model

class json_deserializer:

    @staticmethod
    def deserialize_object(data):
        if not isinstance(data, dict):
            raise ValueError("Требуется словар.")

        model_type = data.get("model")
        model_class = json_deserializer.get_model_class(model_type)

        if not model_class:
            raise ValueError(f"Unknown model type: {model_type}")

        model_instance = model_class()

        model_instance.deserialize(data)

        return model_instance

    @classmethod
    def deserialize_json(cls, json_data):
        data = json.loads(json_data)
        models = []

        for item in data:
            model_instance = cls.deserialize_object(item)
            models.append(model_instance)

        return models

    @staticmethod
    def get_model_class(model_type):
        mapping = {
            'nomenclature_model': nomenclature_model,
            'range_model': range_model,
            'group_model': group_model,
            'ingredient_model': ingredient_model,
            'step_model': step_model,
            'recipe_model': recipe_model
        }
        return mapping.get(model_type)
