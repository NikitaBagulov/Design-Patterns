from src.core.abstract_model import abstract_model
from src.utils.validator import Validator

class step_model(abstract_model):
    __step_number: int = 1
    __description: str = ""

    @property
    def step_number(self) -> int:
        return self.__step_number
    
    @step_number.setter
    def step_number(self, value: int):
        Validator.validate_positive_integer(value, "step_number")
        self.__step_number = value

    @property
    def description(self) -> str:
        return self.__description
    
    @description.setter
    def description(self, value: str):
        Validator.validate_type(value, str, "description")
        Validator.validate_non_empty(value, "description")
        self.__description = value.strip()

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)

    def __str__(self) -> str:
        return (
            f"<StepModel(step_number={self.__step_number}, "
            f"description='{self.__description}')>"
        )
    
    def _deserialize_additional_fields(self, data: dict):
        """
        Десериализация дополнительных полей для step_model.
        """
        if 'step_number' in data:
            step_number = data['step_number']
            Validator.validate_positive_integer(step_number, "step_number")
            self.step_number = step_number

        if 'description' in data:
            description = data['description']
            Validator.validate_type(description, str, "description")
            Validator.validate_non_empty(description, "description")
            self.description = description.strip()