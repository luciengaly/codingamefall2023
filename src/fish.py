from enum import Enum
from typing import Tuple

from vector import Vector
from entity import Entity


class FishType(Enum):
    JELLY = 0
    FISH = 1
    CRAB = 2


class Fish(Entity):
    def __init__(
        self,
        x: float,
        y: float,
        fish_type: FishType,
        color: int,
        entity_id: int,
        low_y: int,
        high_y: int,
    ) -> None:
        self.id: int = entity_id
        self.pos: Vector = Vector(x, y)
        self.type: FishType = fish_type
        self.color: int = color
        self.low_y: int = low_y
        self.high_y: int = high_y
        self.speed: Vector = Vector.ZERO
        self.is_fleeing: bool = False
        self.fleeing_from_player: int or None = None

    def __repr__(self):
        return f"(id: {self.id}, pos: {self.pos}, spd: {self.speed}, color: {self.color}, type: {self.type})"

    def get_pos(self) -> Vector:
        return self.pos

    def get_speed(self) -> Vector:
        return self.speed

    def get_x(self) -> float:
        return self.pos.get_x()

    def get_y(self) -> float:
        return self.pos.get_y()

    def get_obs(self) -> Tuple[float, float, float, float]:
        return (
            self.get_x(),
            self.get_y(),
            self.get_speed().get_x(),
            self.get_speed().get_y(),
        )
