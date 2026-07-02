from typing import Dict, Any


class UserSessionManager:
    def __init__(self):
        self.sessions: Dict[int, Dict[str, Any]] = {}

    def create(self, user_id: int):
        self.sessions[user_id] = {
            "step": None,
            "video": None,
            "audios": [],
            "subtitles": [],
            "operation": None,
            "output_name": None,
            "metadata": {},
        }

    def exists(self, user_id: int) -> bool:
        return user_id in self.sessions

    def get(self, user_id: int):
        return self.sessions.get(user_id)

    def set(self, user_id: int, key: str, value):
        if not self.exists(user_id):
            self.create(user_id)

        self.sessions[user_id][key] = value

    def clear(self, user_id: int):
        self.sessions.pop(user_id, None)


session = UserSessionManager()
