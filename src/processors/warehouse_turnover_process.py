from src.models.warehouse_turnover import warehouse_turnover_model
from src.core.abstract_process import abstract_process

class warehouse_turnover_process(abstract_process):

    def process(self, transactions) -> list:
        """
        Вычисляет складские обороты по транзакциям.
        """
        turnovers = {}

        for transaction in transactions:
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

        return list(turnovers.values())