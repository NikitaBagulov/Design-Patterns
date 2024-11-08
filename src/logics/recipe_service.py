from src.models.nomenclature import nomenclature_model
from src.logics.domain_prototype import domain_prototype
from src.dto.filter_dto import filter_dto
from src.utils.custom_exceptions import ArgumentException, NotFoundException, ConversionException
from src.logics.observe_service import observe_service
from src.core.event_type import event_type
from src.data_reposity import data_reposity
from src.dto.filter_type import filter_type
from src.core.abstract_logic import abstract_logic
from src.logics.nomenclature_service import nomenclature_service

class recipe_service(abstract_logic):
    def __init__(self, reposity: data_reposity):
        observe_service.append(self)
        self.__reposity = reposity

    def update_related_recipes(self, request):
        
        recipes = self.__reposity.data.get(data_reposity.recipes_key(), [])
        for recipe in recipes:
            nomenclature_service.find_and_update_nomenclature(recipe, request)
        return {"status": "Связанные рецепты успешно обновлены"}
        


    def handle_event(self, type: event_type, params):
        if type == event_type.CHANGE_NOMENCLATURE_FROM_RECIPE:
            return self.update_related_recipes(params)
        return {"status": "fail"}
        
    
