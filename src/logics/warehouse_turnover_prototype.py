from src.models.warehouse_turnover import warehouse_turnover_model

class warehouse_turnover_prototype(warehouse_turnover_model):
    
    def clone(self):
        return warehouse_turnover_prototype(
            warehouse=self.warehouse,
            nomenclature=self.nomenclature,
            range=self.range,
            turnover=self.turnover
        )

    def __init__(self, warehouse=None, nomenclature=None, range=None, turnover=0.0):
        super().__init__()
        self.warehouse = warehouse
        self.nomenclature = nomenclature
        self.range = range
        self.turnover = turnover
