from typing import Type, Dict, Callable, Any

class CommandBus:
    def __init__(self):
        self._handlers: Dict[Type, Callable] = {}

    def register_handler(self, command_type: Type, handler: Callable):
        if command_type in self._handlers:
            raise ValueError(f"Handler already registered for {command_type}")
        self._handlers[command_type] = handler

    def handle(self, command: Any) -> Any:
        handler = self._handlers.get(type(command))
        if not handler:
            raise ValueError(f"No handler for {type(command)}")

        if hasattr(handler, "handle"):
            return handler.handle(command)
        elif callable(handler):
            return handler(command)
        else:
            raise TypeError("Handler must be callable or have .handle()")

