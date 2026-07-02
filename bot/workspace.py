from typing import Dict, Any
import time


class WorkspaceManager:
    def __init__(self):
        self.workspaces: Dict[int, Dict[str, Any]] = {}

    def create(self, user_id: int):
        self.workspaces[user_id] = {
            "created_at": time.time(),

            # Main video
            "video": None,

            # Uploaded resources
            "assets": {
                "audios": [],
                "subtitles": [],
                "thumbnail": None,
                "fonts": [],
                "attachments": []
            },

            # Operations waiting to be applied
            "pending_operations": [],

            # Output settings
            "output": {
                "filename": None,
                "container": None
            },

            # Current conversation state
            "state": None
        }

    def exists(self, user_id: int):
        return user_id in self.workspaces

    def get(self, user_id: int):
        return self.workspaces.get(user_id)

    def set(self, user_id: int, key: str, value):
        if not self.exists(user_id):
            self.create(user_id)

        self.workspaces[user_id][key] = value

    def add_audio(self, user_id: int, audio):
        self.workspaces[user_id]["assets"]["audios"].append(audio)

    def add_subtitle(self, user_id: int, subtitle):
        self.workspaces[user_id]["assets"]["subtitles"].append(subtitle)

    def set_thumbnail(self, user_id: int, thumbnail):
        self.workspaces[user_id]["assets"]["thumbnail"] = thumbnail

    def add_operation(self, user_id: int, operation: dict):
        self.workspaces[user_id]["pending_operations"].append(operation)

    def clear(self, user_id: int):
        if user_id in self.workspaces:
            del self.workspaces[user_id]


workspace = WorkspaceManager()
