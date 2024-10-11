from typing import List, Set, Optional
from fish import Fish
from scan import Scan


class Player:
    def __init__(self, index: int) -> None:
        self.message: Optional[str] = None
        self.drones: List[Drone] = []
        self.visible_fishes: Set[Fish] = set()
        self.scans: Set[Scan] = set()
        self.count_fish_saved: List[int] = []
        self.points: int = 0
        self.index: int = index

    def get_expected_output_lines(self) -> int:
        return len(self.drones)

    def get_message(self) -> Optional[str]:
        return self.message

    def reset(self) -> None:
        self.message = None
        for d in self.drones:
            d.move = None
            d.fishes_scanned_this_turn.clear()
            d.did_report = False
            d.message = ""

    def get_nickname_token(self) -> str:
        return f"Player_{self.index}"

    def get_index(self) -> int:
        return self.index
