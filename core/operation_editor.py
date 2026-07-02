from typing import Optional


class OperationEditor:
    """
    Edit pending operations inside a workspace.
    """

    def __init__(self, workspace):
        self.workspace = workspace

    # ------------------------------------------
    # Get operation
    # ------------------------------------------

    def get(self, operation_id: str):

        for item in self.workspace.history.pending:

            if item.id == operation_id:
                return item

        return None

    # ------------------------------------------
    # Delete
    # ------------------------------------------

    def delete(self, operation_id: str):

        item = self.get(operation_id)

        if item is None:
            return False

        self.workspace.history.pending.remove(item)

        return True

    # ------------------------------------------
    # Update data
    # ------------------------------------------

    def update(
        self,
        operation_id: str,
        **kwargs
    ):

        item = self.get(operation_id)

        if item is None:
            return False

        item.data.update(kwargs)

        return True

    # ------------------------------------------
    # Move Up
    # ------------------------------------------

    def move_up(self, operation_id: str):

        operations = self.workspace.history.pending

        for index, item in enumerate(operations):

            if item.id == operation_id:

                if index == 0:
                    return False

                operations[index - 1], operations[index] = (
                    operations[index],
                    operations[index - 1]
                )

                return True

        return False

    # ------------------------------------------
    # Move Down
    # ------------------------------------------

    def move_down(self, operation_id: str):

        operations = self.workspace.history.pending

        for index, item in enumerate(operations):

            if item.id == operation_id:

                if index == len(operations) - 1:
                    return False

                operations[index + 1], operations[index] = (
                    operations[index],
                    operations[index + 1]
                )

                return True

        return False

    # ------------------------------------------
    # Clear All
    # ------------------------------------------

    def clear(self):

        self.workspace.history.pending.clear()

    # ------------------------------------------
    # Count
    # ------------------------------------------

    def count(self):

        return len(self.workspace.history.pending)
