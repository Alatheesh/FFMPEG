import uuid

class MediaAsset:
    def __init__(self, file_path, file_size, file_type, metadata=None, id=None):
        self.id = id or str(uuid.uuid4())
        self.file_path = file_path
        self.file_size = file_size
        self.file_type = file_type  # 'video', 'audio', 'subtitle', 'thumbnail'
        self.metadata = metadata or {}  # Format metadata, stream list, codecs

    def to_dict(self):
        return {
            "id": self.id,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "file_type": self.file_type,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        return cls(
            id=data.get("id"),
            file_path=data.get("file_path"),
            file_size=data.get("file_size"),
            file_type=data.get("file_type"),
            metadata=data.get("metadata")
        )

class PipelineOperation:
    def __init__(self, op_type, params=None, id=None):
        self.id = id or str(uuid.uuid4())
        self.op_type = op_type  # 'replace_audio', 'remove_subtitle', 'add_thumbnail', 'set_metadata', 'trim_video'
        self.params = params or {}  # Parameter payload

    def to_dict(self):
        return {
            "id": self.id,
            "op_type": self.op_type,
            "params": self.params
        }

    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        return cls(
            id=data.get("id"),
            op_type=data.get("op_type"),
            params=data.get("params")
        )

class Workspace:
    def __init__(self, user_id, assets=None, pipeline=None, history=None, 
                 pending_action=None, output_settings=None, dashboard_message_id=None,
                 runtime_state=None, main_video_id=None):
        self.user_id = user_id
        self.assets = assets or {}  # asset_id -> MediaAsset
        self.pipeline = pipeline or []  # List of PipelineOperation
        self.history = history or []  # List of edit history strings
        self.pending_action = pending_action  # e.g., 'replace_audio', 'add_subtitle'
        self.output_settings = output_settings or {
            "format": "mkv",
            "video_codec": "copy",
            "audio_codec": "copy",
            "compress": None
        }
        self.dashboard_message_id = dashboard_message_id
        self.runtime_state = runtime_state or {}  # Processing percentage, exporting flags
        self.main_video_id = main_video_id

    def add_asset(self, file_path, file_size, file_type, metadata=None):
        asset = MediaAsset(file_path, file_size, file_type, metadata)
        self.assets[asset.id] = asset
        if file_type == "video" and not self.main_video_id:
            self.main_video_id = asset.id
        return asset

    def add_operation(self, op_type, params=None):
        op = PipelineOperation(op_type, params)
        self.pipeline.append(op)
        # Log to history
        self.add_history(f"Added operation: {op_type}")
        return op

    def add_history(self, action_desc):
        self.history.append(action_desc)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "assets": {k: v.to_dict() for k, v in self.assets.items()},
            "pipeline": [op.to_dict() for op in self.pipeline],
            "history": self.history,
            "pending_action": self.pending_action,
            "output_settings": self.output_settings,
            "dashboard_message_id": self.dashboard_message_id,
            "runtime_state": self.runtime_state,
            "main_video_id": self.main_video_id
        }

    @classmethod
    def from_dict(cls, user_id, data):
        if not data:
            return cls(user_id)
        
        assets = {k: MediaAsset.from_dict(v) for k, v in data.get("assets", {}).items()}
        pipeline = [PipelineOperation.from_dict(op) for op in data.get("pipeline", [])]
        
        return cls(
            user_id=user_id,
            assets=assets,
            pipeline=pipeline,
            history=data.get("history", []),
            pending_action=data.get("pending_action"),
            output_settings=data.get("output_settings"),
            dashboard_message_id=data.get("dashboard_message_id"),
            runtime_state=data.get("runtime_state", {}),
            main_video_id=data.get("main_video_id")
        )
