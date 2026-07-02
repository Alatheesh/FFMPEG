from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from uuid import uuid4


@dataclass
class PendingAction:
    """
    Represents the next user action that the bot
    is waiting for.
    """

    id: str = field(default_factory=lambda: str(uuid4()))

    action: str = ""

    data: Dict[str, Any] = field(default_factory=dict)

    completed: bool = False


class PendingActionManager:

    def __init__(self):

        self.current: Optional[PendingAction] = None

    # --------------------------------------

    def set(
        self,
        action: str,
        **kwargs
    ):

        self.current = PendingAction(
            action=action,
            data=kwargs
        )

        return self.current

    # --------------------------------------

    def get(self):

        return self.current

    # --------------------------------------

    def exists(self):

        return self.current is not None

    # --------------------------------------

    def clear(self):

        self.current = None

    # --------------------------------------

    def complete(self):

        if self.current:
            self.current.completed = True

    # --------------------------------------

    def is_action(
        self,
        action: str
    ):

        if not self.current:
            return False

        return self.current.action == action
