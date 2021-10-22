from dataclasses import dataclass
from typing import Callable, Tuple

class EventHandler:
    @dataclass
    class Operation:
        function: Callable
        arguments: Tuple

    def __init__(self):
        self._events = {}

    def addEvent(self, event, function, args=None):
        current_operations = self._events.setdefault(event, [])
        current_operations.append(self.Operation(function, args))

    def postEvent(self, event):
        if event in self._events:
            for operation in self._events[event]:
                if operation.arguments:
                    operation.function(*operation.arguments)
                else:
                    operation.function()