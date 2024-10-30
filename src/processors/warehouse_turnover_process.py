import json
from src.models.warehouse_turnover import warehouse_turnover_model
from src.core.abstract_process import abstract_process
from src.settings_manager import settings_manager
from datetime import datetime
class warehouse_turnover_process(abstract_process):

    def __init__(self, manager:settings_manager = None):
        self.block_period = manager.settings.block_period if manager else datetime.now()

    def process(self, transactions) -> list:
        """
        Вычисляет складские обороты по транзакциям с учетом даты блокировки.
        """
        turnovers = self.load_saved_turnovers()
        new_turnovers = {}

        for transaction in transactions:
            if transaction.period < self.block_period:
                key = (transaction.warehouse.unique_code, transaction.nomenclature.unique_code, transaction.range.unique_code)
                
                if key not in turnovers:
                    turnovers[key] = warehouse_turnover_model.create(
                        warehouse=transaction.warehouse,
                        nomenclature=transaction.nomenclature,
                        range=transaction.range
                    )

                if transaction.is_incoming:
                    turnovers[key].turnover += transaction.quantity
                else:
                    turnovers[key].turnover -= transaction.quantity
            else:
                key = (transaction.warehouse.unique_code, transaction.nomenclature.unique_code, transaction.range.unique_code)
                
                if key not in new_turnovers:
                    new_turnovers[key] = warehouse_turnover_model.create(
                        warehouse=transaction.warehouse,
                        nomenclature=transaction.nomenclature,
                        range=transaction.range
                    )

                if transaction.is_incoming:
                    new_turnovers[key].turnover += transaction.quantity
                else:
                    new_turnovers[key].turnover -= transaction.quantity

        for key, turnover in new_turnovers.items():
            if key in turnovers:
                turnovers[key].turnover += turnover.turnover
            else:
                turnovers[key] = turnover

        return list(turnovers.values())

    def load_saved_turnovers(self) -> dict:
        """
        Загружает сохраненные обороты из warehouse_turnover.json.
        """
        try:
            full_filename = "blocked_turnovers.json"
            with open(f"src/processors/{full_filename}", 'r', encoding='utf-8') as file:
                data = json.load(file)
                turnovers = {}
                for item in data:
                    turnover = warehouse_turnover_model()
                    turnover.deserialize(item)
                    key = (turnover.warehouse.unique_code, turnover.nomenclature.unique_code, turnover.range.unique_code)
                    turnovers[key] = turnover
                return turnovers
        except FileNotFoundError:
            return {}