from src.models.warehouse_transaction import warehouse_transaction_model
from src.logics.domain_prototype import domain_prototype
from src.utils.validator import Validator
from src.dto.filter_dto import filter_dto, warehouse_nomenclature_filter_dto
from datetime import datetime

class warehouse_transaction_prototype(domain_prototype):

    def create(self, data: list, filt: warehouse_nomenclature_filter_dto):
        if filt.warehouse:
            self.data = self.filter_by_field(data, filt.warehouse, 'warehouse.name')

        if filt.nomenclature:
            self.data = self.filter_by_field(self.data, filt.nomenclature, 'nomenclature.name')

        if filt.period:
            self.data = self.filter_by_period(self.data, filt.period)
        
        return warehouse_transaction_prototype(self.data)

    def filter_by_field(self, source: list, filt: filter_dto, field: str) -> list:
        """
        Универсальная функция для фильтрации по указанному полю.
        """
        Validator.validate_not_none(source, 'source')
        Validator.validate_not_none(filt, 'filt')
        Validator.validate_non_empty(field, 'field')

        filter_value = getattr(filt, 'name', None)
        if not filter_value:
            return source

        result = []
        for item in source:
            item_field_value = self.extract_field(item, field)
            if self.match_field(item_field_value, filter_value, filt.type):
                result.append(item)

        return result

    def extract_field(self, item, field: str):
        """
        Извлекает нужное поле из объекта по его строковому названию (например, warehouse.name).
        """
        fields = field.split('.')
        value = item
        for f in fields:
            value = getattr(value, f, None)
            if value is None:
                break
        return value

    def filter_by_period(self, source: list, period: dict) -> list:
        """
        Фильтрация по периоду (start и end).
        """
        Validator.validate_not_none(period, 'period')

        start_period = period.get('start')
        end_period = period.get('end')

        Validator.validate_not_none(start_period, 'start_period')
        Validator.validate_not_none(end_period, 'end_period')

        start_period = datetime.strptime(start_period, '%Y-%m-%d')
        end_period = datetime.strptime(end_period, '%Y-%m-%d')

        result = []
        for item in source:
            if isinstance(item, warehouse_transaction_model) and item.period:
                item_period = self.extract_field(item, 'period')
                if isinstance(item_period, str):
                    item_period = datetime.strptime(item_period, '%Y-%m-%d')

                if start_period <= item_period <= end_period:
                    result.append(item)
        
        return result
