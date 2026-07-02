from typing import Dict, List, Optional


class NavigationManager:
    """
    Stores menu navigation history for every user.
    """

    def __init__(self):
        self.history: Dict[int, List[str]] = {}

    # ----------------------------------------
    # Create
    # ----------------------------------------

    def create(self, user_id: int):

        if user_id not in self.history:
            self.history[user_id] = []

    # ----------------------------------------
    # Push
    # ----------------------------------------

    def push(self, user_id: int, menu: str):

        self.create(user_id)

        if not self.history[user_id]:
            self.history[user_id].append(menu)
            return

        if self.history[user_id][-1] != menu:
            self.history[user_id].append(menu)

    # ----------------------------------------
    # Current
    # ----------------------------------------

    def current(self, user_id: int) -> Optional[str]:

        self.create(user_id)

        if not self.history[user_id]:
            return None

        return self.history[user_id][-1]

    # ----------------------------------------
    # Back
    # ----------------------------------------

    def back(self, user_id: int) -> Optional[str]:

        self.create(user_id)

        if len(self.history[user_id]) <= 1:
            return None

        self.history[user_id].pop()

        return self.history[user_id][-1]

    # ----------------------------------------
    # Home
    # ----------------------------------------

    def home(self, user_id: int):

        self.create(user_id)

        if self.history[user_id]:
            first = self.history[user_id][0]
            self.history[user_id] = [first]
            return first

        return None

    # ----------------------------------------
    # Reset
    # ----------------------------------------

    def reset(self, user_id: int):

        self.history[user_id] = []

    # ----------------------------------------
    # Remove
    # ----------------------------------------

    def remove(self, user_id: int):

        self.history.pop(user_id, None)


navigation = NavigationManager()
