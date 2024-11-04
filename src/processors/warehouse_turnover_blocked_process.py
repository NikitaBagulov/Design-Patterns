from src.models.warehouse_turnover import warehouse_turnover_model
from src.core.abstract_process import abstract_process
from src.settings_manager import settings_manager

class warehouse_turnover_blocked_process(abstract_process):
    def __init__(self, manager: settings_manager):
        self.manager = manager
        self.block_period = self.manager.settings.block_period

    def process(self, transactions) -> list:
        """
        Вычисляет и сохраняет обороты по транзакциям до block_period.
        """
        turnovers = {}
        
        for transaction in transactions:
            if transaction.period > self.block_period:
                continue
            
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
        return turnovers

