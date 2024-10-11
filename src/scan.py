from typing import Optional
from fish import Fish, FishType


class Scan:
    def __init__(self, fish_data) -> None:
        if isinstance(fish_data, Fish):
            self.fish_id: int = fish_data.id
            self.type: Optional[FishType] = fish_data.type
            self.color: int = fish_data.color
        elif isinstance(fish_data, dict):
            self.fish_id = -1
            self.type = fish_data["type"]
            self.color = fish_data["color"]
        else:
            raise RuntimeError("Unknown instance")

    def to_input_string(self) -> str:
        return str(self.fish_id) if self.fish_id != -1 else ""

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Scan):
            return False
        return self.color == other.color and self.type == other.type

    def __hash__(self) -> int:
        return hash((self.color, self.type))

    def __str__(self) -> str:
        return f"{self.color} {self.type.name.lower()}" if self.type is not None else ""
