import subprocess
from typing import List, Tuple


class FFmpeg:

    @staticmethod
    def run(command: List[str]) -> Tuple[bool, str]:
        """
        Execute an FFmpeg command.

        Returns:
            (success, output)
        """

        try:
            process = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )

            return True, process.stderr

        except subprocess.CalledProcessError as e:
            return False, e.stderr

    @staticmethod
    def run_with_process(command: List[str]):
        """
        Execute FFmpeg and return the process.
        Used later for progress updates.
        """

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        return process
