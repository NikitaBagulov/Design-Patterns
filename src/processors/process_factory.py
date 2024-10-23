class process_factory:
    def __init__(self):
        self.__processes = {}

    def register_process(self, process_name: str, process_class):
        """Регистрирует новый процесс в фабрике."""
        self.__processes[process_name] = process_class

    def get_process(self, process_name: str):
        """Возвращает экземпляр зарегистрированного процесса."""
        process_class = self.__processes.get(process_name)
        if not process_class:
            raise ValueError(f"Процесс с именем {process_name} не зарегистрирован.")
        return process_class()

