from typing import Callable, Dict

from core.job_engine import JobEngine


class Processor:

    def __init__(self, workspace):
        self.workspace = workspace
        self.engine = JobEngine()

        self.handlers: Dict[str, Callable] = {}

        self.register_default_handlers()

    def register(self, operation: str, handler: Callable):
        """
        Register an operation handler.
        """
        self.handlers[operation] = handler

    def register_default_handlers(self):

        self.register("replace_audio", self.replace_audio)
        self.register("merge_audio", self.merge_audio)
        self.register("remove_audio", self.remove_audio)
        self.register("swap_audio", self.swap_audio)
        self.register("rename_audio", self.rename_audio)

        self.register("add_subtitle", self.add_subtitle)
        self.register("remove_subtitle", self.remove_subtitle)

        self.register("change_thumbnail", self.change_thumbnail)
        self.register("change_metadata", self.change_metadata)

    def load_operations(self):
        self.engine.operations = self.workspace.get(
            "pending_operations",
            []
        )

    def process(self):

        self.load_operations()

        if self.engine.is_empty():
            return False

        for operation in self.engine.get_all():

            operation_type = operation["type"]
            data = operation["data"]

            handler = self.handlers.get(operation_type)

            if handler:
                handler(data)
            else:
                print(f"Unknown operation: {operation_type}")

        return True

    # ----------------------------------------------------
    # AUDIO
    # ----------------------------------------------------

    def replace_audio(self, data):
        pass

    def merge_audio(self, data):
        pass

    def remove_audio(self, data):
        pass

    def swap_audio(self, data):
        pass

    def rename_audio(self, data):
        pass

    # ----------------------------------------------------
    # SUBTITLES
    # ----------------------------------------------------

    def add_subtitle(self, data):
        pass

    def remove_subtitle(self, data):
        pass

    # ----------------------------------------------------
    # THUMBNAIL / METADATA
    # ----------------------------------------------------

    def change_thumbnail(self, data):
        pass

    def change_metadata(self, data):
        pass
