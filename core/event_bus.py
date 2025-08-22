import asyncio
from typing import Type, Dict, List, Callable, Any

class EventBus:
    def __init__(self):
        self._handlers: Dict[Type, List[Callable]] = {}

    def register_handler(self, event_type: Type, handler: Callable):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event: Any):
        handlers = self._handlers.get(type(event), [])
        for handler in handlers:
            if hasattr(handler, "handle"):
                result = handler.handle(event)
            elif callable(handler):
                result = handler(event)
            else:
                raise TypeError("Handler must be callable or have .handle()")

            if asyncio.iscoroutine(result):
                asyncio.run(result)

