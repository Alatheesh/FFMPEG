from dataclasses import dataclass
from typing import Optional


@dataclass
class CallbackData:
    """
    Parsed callback data.

    Format:
        category:action:value
    """

    category: str
    action: str
    value: Optional[str] = None


class CallbackParser:

    @staticmethod
    def parse(data: str) -> CallbackData:
        """
        Parse callback data.

        Examples:

        audio:replace:2
        subtitle:remove:1
        workspace:apply
        menu:audio
        """

        parts = data.split(":")

        if len(parts) == 1:
            return CallbackData(
                category=parts[0],
                action="",
                value=None
            )

        if len(parts) == 2:
            return CallbackData(
                category=parts[0],
                action=parts[1],
                value=None
            )

        return CallbackData(
            category=parts[0],
            action=parts[1],
            value=":".join(parts[2:])
        )

    @staticmethod
    def build(
        category: str,
        action: str,
        value: Optional[str] = None
    ) -> str:

        if value is None:
            return f"{category}:{action}"

        return f"{category}:{action}:{value}"
