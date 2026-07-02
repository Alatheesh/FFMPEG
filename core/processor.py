import os

from core.job_engine import JobEngine


class Processor:

    def __init__(self, workspace):
        self.workspace = workspace
        self.engine = JobEngine()

    def load_operations(self):
        """
        Load pending operations from the workspace.
        """

        self.engine.operations = self.workspace.get(
            "pending_operations",
            []
        )

    def process(self):
        """
        Execute every pending operation.
        """

        self.load_operations()

        if self.engine.is_empty():
            return False

        for operation in self.engine.get_all():

            operation_type = operation["type"]
            data = operation["data"]

            print(f"Running: {operation_type}")

            if operation_type == "replace_audio":
                self.replace_audio(data)

            elif operation_type == "merge_audio":
                self.merge_audio(data)

            elif operation_type == "remove_audio":
                self.remove_audio(data)

            elif operation_type == "swap_audio":
                self.swap_audio(data)

            elif operation_type == "rename_audio":
                self.rename_audio(data)

            elif operation_type == "add_subtitle":
                self.add_subtitle(data)

            elif operation_type == "remove_subtitle":
                self.remove_subtitle(data)

            elif operation_type == "change_thumbnail":
                self.change_thumbnail(data)

            elif operation_type == "change_metadata":
                self.change_metadata(data)

        return True

    # ---------------- Audio ---------------- #

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

    # -------------- Subtitle --------------- #

    def add_subtitle(self, data):
        pass

    def remove_subtitle(self, data):
        pass

    # --------------- Others ---------------- #

    def change_thumbnail(self, data):
        pass

    def change_metadata(self, data):
        pass
