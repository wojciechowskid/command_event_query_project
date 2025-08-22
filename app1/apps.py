from django.apps import AppConfig
from core.bus_instance import command_bus, query_bus, event_bus
from .handler_registry import COMMAND_HANDLERS, QUERY_HANDLERS, EVENT_HANDLERS

class App1Config(AppConfig):
    name = 'app1'

    def ready(self):
        for command_type, handler in COMMAND_HANDLERS.items():
            command_bus.register_handler(command_type, handler)

        for query_type, handler in QUERY_HANDLERS.items():
            query_bus.register_handler(query_type, handler)

        for event_type, handlers in EVENT_HANDLERS.items():
            for handler in handlers:
                event_bus.register_handler(event_type, handler)

