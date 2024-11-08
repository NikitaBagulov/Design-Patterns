from src.models.nomenclature import nomenclature_model
from src.logics.domain_prototype import domain_prototype
from src.dto.filter_dto import filter_dto
from src.utils.custom_exceptions import ArgumentException, NotFoundException, ConversionException
from src.logics.observe_service import observe_service
from src.core.event_type import event_type
from src.data_reposity import data_reposity
from src.dto.filter_type import filter_type
from src.core.abstract_logic import abstract_logic

class nomenclature_service(abstract_logic):
    def __init__(self, reposity: data_reposity):
        observe_service.append(self)
        self.__reposity = reposity
        

    def get_nomenclature(self, request):
        unique_code = request.get('unique_code')
        if not unique_code:
            return {"error": "Unique code is required."}
        
        nomenclature_filt = filter_dto(unique_code=unique_code, type=filter_type.EQUALS)
        existing_nomenclatures = self.filter_model(nomenclature_filt)
        if len(existing_nomenclatures) == 0:
            return {"status": "Номенклатура с указанным уникальным кодом не найдена."}
        
        return existing_nomenclatures

    def add_nomenclature(self, request) -> nomenclature_model:
        name = request.get('name')
        full_name = request.get('full_name')
        group_id = request.get('group_id')
        range_id = request.get('range_id')
        group_filt = filter_dto(unique_code=group_id, type=filter_type.EQUALS)
        group = next(iter(self.filter_model(group_filt, data_reposity.group_key())), None)
        
        range_filt = filter_dto(unique_code=range_id, type=filter_type.EQUALS)
        range_ = next(iter(self.filter_model(range_filt, data_reposity.range_key())), None)
        
        if not group:
            return {"status": f"Группа с ID '{group_id}' не найдена."}
        if not range_:
            return {"status": f"Диапазон с ID '{range_id}' не найден."}
        
        nomenclature = nomenclature_model.create(name, full_name, group, range_)
        nomenclature_filt = filter_dto(unique_code=nomenclature.unique_code, type=filter_type.EQUALS)
        existing_nomenclatures = self.filter_model(nomenclature_filt)
        
        if existing_nomenclatures:
            return {"status": f"Номенклатура с уникальным кодом '{nomenclature.unique_code}' уже существует."}
        
        self.__reposity.data[data_reposity.nomenclature_key()].append(nomenclature)
        return nomenclature

    def update_nomenclature(self, request):
        unique_code = request.get('unique_code')
        if not unique_code:
            return {"error": "Отсутствует уникальный код!"}
        nomenclature_filt = filter_dto(unique_code=unique_code, type=filter_type.EQUALS)
        nomenclature = self.filter_model(nomenclature_filt)[0]
        print(nomenclature)
        if not nomenclature:
            return {"status": f"Номенклатура с уникальным кодом '{unique_code}' не найдена."}

        if 'name' in request:
            nomenclature.name = request['name']
        if 'full_name' in request:
            nomenclature.full_name = request['full_name']

        if 'group_id' in request:
            group_filt = filter_dto(unique_code=request['group_id'], type=filter_type.EQUALS)
            group = next(iter(self.filter_model(group_filt, data_reposity.group_key())), None)
            if not group:
                return {"status": f"Группа с ID '{request['group_id']}' не найдена."}
            nomenclature.group = group

        if 'range_id' in request:
            range_filt = filter_dto(unique_code=request['range_id'], type=filter_type.EQUALS)
            range_ = next(iter(self.filter_model(range_filt, key=data_reposity.range_key())), None)
            if not range_:
                return {"status": f"Диапазон с ID '{request['range_id']}' не найден."}
            nomenclature.range = range_

        observe_service.raise_event(event_type.CHANGE_NOMENCLATURE_FROM_RECIPE, request)
        observe_service.raise_event(event_type.CHANGE_NOMENCLATURE_FROM_TRANSACTION, request)

        return {"status": "Номенклатура успешно обновлена"}
        

    def find_and_update_nomenclature(self, obj, request):
        """
        Рекурсивно ищет номенклатуру по уникальному коду и обновляет ее данные на основе запроса.
        """
        unique_code = request.get('unique_code')
        if hasattr(obj, 'unique_code') and obj.unique_code == unique_code:
            if 'name' in request:
                obj.name = request['name']
            if 'full_name' in request:
                obj.full_name = request['full_name']

            if 'group_id' in request:
                group_filt = filter_dto(unique_code=request['group_id'], type=filter_type.EQUALS)
                group = next(iter(self.filter_model(group_filt, data_reposity.group_key())), None)
                if not group:
                    return {"status": f"Группа с ID '{request['group_id']}' не найдена."}
                obj.group = group

            if 'range_id' in request:
                range_filt = filter_dto(unique_code=request['range_id'], type=filter_type.EQUALS)
                range_ = next(iter(self.filter_model(range_filt, data_reposity.range_key())), None)
                if not range_:
                    return {"status": f"Диапазон с ID '{request['range_id']}' не найден."}
                obj.range = range_

            return True

        if isinstance(obj, dict):
            for key, value in obj.items():
                if self.find_and_update_nomenclature(value, unique_code, request):
                    return True
        elif isinstance(obj, (list, tuple)):
            for item in obj:
                if self.find_and_update_nomenclature(item, unique_code, request):
                    return True
        elif hasattr(obj, '__dict__'):
            for attr_name in vars(obj):
                attr_value = getattr(obj, attr_name)
                if self.find_and_update_nomenclature(attr_value, unique_code, request):
                    return True

        return False

    def delete_nomenclature(self, request):
        unique_code = request.get('unique_code')
        if not unique_code:
            return {"error": "Отсутствует уникальный код!"}

        nomenclature_filt = filter_dto(unique_code=unique_code, type=filter_type.EQUALS)
        nomenclature = next(iter(self.filter_model(nomenclature_filt)), None)

        if not nomenclature:
            return {"status": f"Номенклатура с уникальным кодом '{unique_code}' не найдена."}

        if self.is_nomenclature_in_recipes(nomenclature) or self.is_nomenclature_in_saved_data(nomenclature):
            return {"status": f"Номенклатура '{unique_code}' не может быть удалена, так как она используется в рецептах или сохраненных данных."}

        self.__reposity.data[data_reposity.nomenclature_key()] = [
            n for n in self.__reposity.data[data_reposity.nomenclature_key()] if n.unique_code != unique_code
        ]
        return {"status": "Номенклатура успешно удалена"}

    def filter_model(self, filt: filter_dto, key=data_reposity.nomenclature_key()) -> list[nomenclature_model]:
        models = self.__reposity.data.get(key, [])
        prototype = domain_prototype(models)
        filtered_prototype = prototype.create(models, filt)
        return filtered_prototype.data

    def is_nomenclature_in_recipes(self, nomenclature: nomenclature_model) -> bool:
        filt = filter_dto(unique_code=nomenclature.unique_code, type=filter_type.EQUALS)
        filtered_recipes = self.filter_model(filt, data_reposity.recipes_key())
        return len(filtered_recipes) != 0

    def is_nomenclature_in_saved_data(self, nomenclature: nomenclature_model) -> bool:
        filt = filter_dto(unique_code=nomenclature.unique_code, type=filter_type.EQUALS)
        filtered_transactions = self.filter_model(filt, data_reposity.transactions_key())
        return len(filtered_transactions) != 0
    
    def set_exception(self, ex: Exception):
        super().set_exception(ex)

    def handle_event(self, type: event_type, params):
        """
        Обрабатывает событие с заданным типом и параметрами.

        Args:
            type (event_type): Тип события, которое необходимо обработать.
            params (dict): Параметры события.
        """
        super().handle_event(type, params)
        
        if type == event_type.CHANGE_NOMENCLATURE:
            return self.update_nomenclature(params)
        elif type == event_type.DELETE_NOMENCLATURE:
            return self.delete_nomenclature(params)
        return {"status": "fail"}
            
