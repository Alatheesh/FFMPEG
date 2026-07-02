from typing import Dict, Any
from uuid import uuid4
from datetime import datetime

from constants import Operation


class OperationQueue:
    """
    Handles adding, removing and managing
    pending operations inside a workspace.
    """

    def __init__(self, workspace):
        self.workspace = workspace

    # --------------------------------------------------

    def add(
        self,
        operation: Operation,
        data: Dict[str, Any]
    ):
        """
        Add a new pending operation.
        """

        item = {
            "id": str(uuid4()),
            "operation": operation.value,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat(),
            "data": data
        }

        self.workspace.history.add(
            operation=operation.value,
            data=item
        )

        return item

    # --------------------------------------------------

    def remove(self, operation_id: str):

        self.workspace.history.remove(operation_id)

    # --------------------------------------------------

    def pending(self):

        return self.workspace.history.get_pending()

    # --------------------------------------------------

    def completed(self):

        return self.workspace.history.get_completed()

    # --------------------------------------------------

    def pending_count(self):

        return self.workspace.history.pending_count()

    # --------------------------------------------------

    def clear(self):

        self.workspace.history.clear()
