from typing import Type, Dict, Callable, Any

class QueryBus:
    def __init__(self):
        self._handlers: Dict[Type, Callable] = {}

    def register_handler(self, query_type: Type, handler: Callable):
        if query_type in self._handlers:
            raise ValueError(f"Handler already registered for {query_type}")
        self._handlers[query_type] = handler

    def handle(self, query: Any) -> Any:
        handler = self._handlers.get(type(query))
        if not handler:
            raise ValueError(f"No handler for {type(query)}")

        if hasattr(handler, "handle"):
            return handler.handle(query)
        elif callable(handler):
            return handler(query)
        else:
            raise TypeError("Handler must be callable or have .handle()")

