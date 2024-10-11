from vector import Vector
from entity import Entity

class Ugly(Entity):
    def __init__(self, x: float, y: float, entity_id: int) -> None:
        self.id: int = entity_id
        self.pos: Vector = Vector(x, y)
        self.speed: Vector = Vector.ZERO
        self.target: Vector or None = None
        self.found_target: bool = False

    def get_pos(self) -> Vector:
        return self.pos

    def get_speed(self) -> Vector:
        return self.speed

    def get_x(self) -> float:
        return self.pos.get_x()

    def get_y(self) -> float:
        return self.pos.get_y()
