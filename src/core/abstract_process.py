from abc import ABC, abstractmethod

class abstract_process(ABC):
    
    @abstractmethod
    def process(self, transactions: list) -> list:
        """Процесс обработки транзакций. На вход список транзакций, на выходе список результатов."""
        pass
