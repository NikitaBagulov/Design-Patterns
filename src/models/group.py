from src.core.abstract_model import abstract_model

class group_model(abstract_model):

    @staticmethod
    def default_group_source():
        item = group_model()
        item.name = "Сырье"
        return item

    @staticmethod
    def default_group_cold():
        item = group_model()
        item.name = "Заморозка"
        return item

    def set_compare_mode(self, other_object) -> bool:
        if other_object is None:
            return False
        if not isinstance(other_object, group_model):
            return False
        return self.name == other_object.name
    
    def __str__(self) -> str:
        return f"<GroupModel(name='{self.name}')>"

    def _deserialize_additional_fields(self, data: dict):
        pass