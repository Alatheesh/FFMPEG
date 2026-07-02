from typing import Callable, Dict


class OperationRegistry:
    """
    Stores every available operation.
    """

    def __init__(self):
        self._operations: Dict[str, Callable] = {}

    def register(self, name: str):
        """
        Decorator to register an operation.
        """

        def decorator(func: Callable):
            if name in self._operations:
                raise ValueError(
                    f"Operation '{name}' is already registered."
                )

            self._operations[name] = func
            return func

        return decorator

    def get(self, name: str):
        """
        Get an operation by name.
        """
        return self._operations.get(name)

    def exists(self, name: str):
        return name in self._operations

    def all(self):
        return self._operations

    def names(self):
        return list(self._operations.keys())


registry = OperationRegistry()
