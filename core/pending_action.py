from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from uuid import uuid4


@dataclass
class PendingAction:
    """
    Represents the current action that the bot is
    waiting for from the user.
    """

    id: str = field(default_factory=lambda: str(uuid4()))

    action: str = ""

    data: Dict[str, Any] = field(default_factory=dict)

    completed: bool = False


class PendingActionManager:
    """
    Stores exactly one pending action for a workspace.
    """

    def __init__(self):

        self.current: Optional[PendingAction] = None

    # ==================================================
    # Set
    # ==================================================

    def set(self, action: str, **kwargs) -> PendingAction:

        self.current = PendingAction(
            action=action,
            data=kwargs
        )

        return self.current

    # ==================================================
    # Get
    # ==================================================

    def get(self) -> Optional[PendingAction]:

        return self.current

    # ==================================================
    # Action
    # ==================================================

    def action(self) -> Optional[str]:

        if self.current is None:
            return None

        return self.current.action

    # ==================================================
    # Data
    # ==================================================

    def data(self) -> Dict[str, Any]:

        if self.current is None:
            return {}

        return self.current.data

    # ==================================================
    # Get Value
    # ==================================================

    def value(self, key: str, default=None):

        if self.current is None:
            return default

        return self.current.data.get(key, default)

    # ==================================================
    # Exists
    # ==================================================

    def exists(self) -> bool:

        return self.current is not None

    # ==================================================
    # Is Action
    # ==================================================

    def is_action(self, action: str) -> bool:

        if self.current is None:
            return False

        return self.current.action == action

    # ==================================================
    # Complete
    # ==================================================

    def complete(self):

        if self.current is not None:
            self.current.completed = True

    # ==================================================
    # Completed
    # ==================================================

    def is_completed(self) -> bool:

        if self.current is None:
            return False

        return self.current.completed

    # ==================================================
    # Clear
    # ==================================================

    def clear(self):

        self.current = None

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):

        self.clear()

    # ==================================================
    # Dictionary
    # ==================================================

    def to_dict(self):

        if self.current is None:
            return None

        return {
            "id": self.current.id,
            "action": self.current.action,
            "data": self.current.data,
            "completed": self.current.completed
        }

    # ==================================================
    # String
    # ==================================================

    def __str__(self):

        if self.current is None:
            return "None"

        return self.current.action

    # ==================================================
    # Bool
    # ==================================================

    def __bool__(self):

        return self.current is not None
