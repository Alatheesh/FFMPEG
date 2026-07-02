from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
import uuid


@dataclass
class HistoryItem:
    """
    Represents one editing operation.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    operation: str = ""

    data: Dict = field(default_factory=dict)

    status: str = "pending"

    created_at: datetime = field(default_factory=datetime.utcnow)


class HistoryManager:

    def __init__(self):

        self.pending: List[HistoryItem] = []

        self.completed: List[HistoryItem] = []

        self.undo_stack: List[HistoryItem] = []

        self.redo_stack: List[HistoryItem] = []

    # ------------------------------------

    def add(self, operation: str, data: Dict):

        item = HistoryItem(
            operation=operation,
            data=data
        )

        self.pending.append(item)

        self.undo_stack.append(item)

        self.redo_stack.clear()

        return item

    # ------------------------------------

    def remove(self, operation_id: str):

        self.pending = [
            item
            for item in self.pending
            if item.id != operation_id
        ]

    # ------------------------------------

    def complete(self, operation_id: str):

        for item in self.pending:

            if item.id == operation_id:

                item.status = "completed"

                self.completed.append(item)

                self.pending.remove(item)

                break

    # ------------------------------------

    def undo(self):

        if not self.undo_stack:
            return None

        item = self.undo_stack.pop()

        self.redo_stack.append(item)

        self.remove(item.id)

        return item

    # ------------------------------------

    def redo(self):

        if not self.redo_stack:
            return None

        item = self.redo_stack.pop()

        self.pending.append(item)

        self.undo_stack.append(item)

        return item

    # ------------------------------------

    def clear(self):

        self.pending.clear()

        self.completed.clear()

        self.undo_stack.clear()

        self.redo_stack.clear()

    # ------------------------------------

    def pending_count(self):

        return len(self.pending)

    # ------------------------------------

    def completed_count(self):

        return len(self.completed)

    # ------------------------------------

    def get_pending(self):

        return self.pending

    # ------------------------------------

    def get_completed(self):

        return self.completed
