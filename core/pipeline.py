from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4


class PipelineStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class PipelineStep:

    id: str = field(default_factory=lambda: str(uuid4()))

    operation: str = ""

    data: Dict = field(default_factory=dict)

    enabled: bool = True

    status: PipelineStatus = PipelineStatus.PENDING

    error: Optional[str] = None


class Pipeline:

    def __init__(self):

        self.steps: List[PipelineStep] = []

    # --------------------------------------

    def add(self, operation: str, data: Dict):

        step = PipelineStep(
            operation=operation,
            data=data
        )

        self.steps.append(step)

        return step

    # --------------------------------------

    def remove(self, step_id: str):

        self.steps = [
            step
            for step in self.steps
            if step.id != step_id
        ]

    # --------------------------------------

    def get(self, step_id: str):

        for step in self.steps:

            if step.id == step_id:
                return step

        return None

    # --------------------------------------

    def enable(self, step_id: str):

        step = self.get(step_id)

        if step:
            step.enabled = True

    # --------------------------------------

    def disable(self, step_id: str):

        step = self.get(step_id)

        if step:
            step.enabled = False

    # --------------------------------------

    def move_up(self, step_id: str):

        for i, step in enumerate(self.steps):

            if step.id == step_id:

                if i == 0:
                    return

                self.steps[i], self.steps[i - 1] = (
                    self.steps[i - 1],
                    self.steps[i]
                )

                return

    # --------------------------------------

    def move_down(self, step_id: str):

        for i, step in enumerate(self.steps):

            if step.id == step_id:

                if i == len(self.steps) - 1:
                    return

                self.steps[i], self.steps[i + 1] = (
                    self.steps[i + 1],
                    self.steps[i]
                )

                return

    # --------------------------------------

    def pending(self):

        return [
            step
            for step in self.steps
            if (
                step.enabled and
                step.status == PipelineStatus.PENDING
            )
        ]

    # --------------------------------------

    def reset(self):

        for step in self.steps:

            step.status = PipelineStatus.PENDING
            step.error = None

    # --------------------------------------

    def clear(self):

        self.steps.clear()
