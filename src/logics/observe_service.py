from src.core.abstract_logic import abstract_logic
from src.utils.custom_exceptions import ArgumentException
from src.core.event_type import event_type

class observe_service:
    observers = []

    @staticmethod
    def append(service: abstract_logic):

        if service is None:
            return

        if not isinstance(service, abstract_logic):
            raise ArgumentException("service", "Некорректный тип данных!")

        items =  list(map( lambda x: type(x).__name__,  observe_service.observers))
        found =    type( service ).__name__ in items 
        if not found: 
            observe_service.observers.append( service )

    @staticmethod
    def raise_event(e_type: event_type, params):
        statuses = {}
        for instance in observe_service.observers:
            if instance is not None:
                class_name = type(instance).__name__
                status = instance.handle_event(e_type, params)
                statuses[class_name] = status
        return statuses
        