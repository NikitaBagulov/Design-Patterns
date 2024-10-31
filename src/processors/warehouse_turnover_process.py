from src.models.warehouse_turnover import warehouse_turnover_model
from src.core.abstract_process import abstract_process
from src.settings_manager import settings_manager
from datetime import datetime

class warehouse_turnover_process(abstract_process):
    def __init__(self, manager: settings_manager = None, blocked_turnovers: dict = {}):
        self.block_period = manager.settings.block_period if manager else datetime.now()
        self.blocked_turnovers = blocked_turnovers

    def process(self, transactions) -> list:
        """
        Вычисляет складские обороты по транзакциям после даты block_period.
        """

        turnovers = {}

        for transaction in transactions:
            if transaction.period >= self.block_period:
                key = (
                    transaction.warehouse.unique_code,
                    transaction.nomenclature.unique_code,
                    transaction.range.unique_code
                )

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

        for key, turnover in self.blocked_turnovers.items():
            if key in turnovers:
                turnovers[key].turnover += turnover.turnover
            else:
                turnovers[key] = turnover

        return list(turnovers.values())
