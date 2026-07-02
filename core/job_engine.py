from typing import Dict, List


class JobEngine:
    """
    Stores pending operations for a workspace.
    """

    def __init__(self):
        self.operations: List[Dict] = []

    def add(self, operation_type: str, data: Dict):
        self.operations.append({
            "type": operation_type,
            "data": data
        })

    def remove(self, index: int):
        if 0 <= index < len(self.operations):
            self.operations.pop(index)

    def clear(self):
        self.operations.clear()

    def get_all(self):
        return self.operations

    def count(self):
        return len(self.operations)

    def is_empty(self):
        return len(self.operations) == 0
