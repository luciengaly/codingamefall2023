from typing import List, Optional
from vector import Vector
from scan import Scan
from constants import DRONE_MAX_BATTERY, LIGHT_BATTERY_COST, DRONE_BATTERY_REGEN


class Drone:
    def __init__(self, x: float, y: int, _id: int, owner: "Player") -> None:
        self.id: int = _id
        self.owner: Player = owner
        self.pos: Vector = Vector(x, y)
        self.move: Optional[Vector] = None
        self.speed: Vector = Vector(0, 0)

        self.light: int = 0
        self.battery: int = DRONE_MAX_BATTERY
        self.scans: List[Scan] = []
        self.fishes_scanned_this_turn: List[int] = []
        self.light_switch: bool = False
        self.light_on: bool = False
        self.dying: bool = False
        self.dead: bool = False
        self.did_report: bool = False
        self.die_at: float = 0.0
        self.message: str = ""

        # Stats
        self.max_turns_spent_with_scan: int = 0
        self.turns_spent_with_scan: int = 0
        self.max_y: int = 0

    def __repr__(self):
        return f"(id: {self.id}, pos: {self.pos}, spd: {self.speed}, battery: {self.battery})"

    def get_pos(self) -> Vector:
        return self.pos

    def get_speed(self) -> Vector:
        return self.speed

    def is_engine_on(self) -> bool:
        return self.move is not None

    def is_light_on(self) -> bool:
        return self.light_on

    def drain_battery(self) -> None:
        self.battery -= LIGHT_BATTERY_COST

    def recharge_battery(self) -> None:
        if self.battery < DRONE_MAX_BATTERY:
            self.battery += DRONE_BATTERY_REGEN
            if self.battery >= DRONE_MAX_BATTERY:
                self.battery = DRONE_MAX_BATTERY

    def is_dead_or_dying(self) -> bool:
        return self.dying or self.dead

    def get_x(self) -> float:
        return self.pos.get_x()

    def get_y(self) -> int:
        return self.pos.get_y()

    def scan_slot_to_string(self, i: int) -> str:
        if len(self.scans) > i:
            scan = self.scans[i]
            return scan.to_input_string()
        return "-1 -1"

    def set_message(self, message: str) -> None:
        self.message = (
            message[:46] + "..." if message and len(message) > 48 else message
        )
