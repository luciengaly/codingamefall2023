from typing import List, Union
from vector import Vector
from entity import Entity

class Closest:
    def __init__(self, entities: List[Entity], distance: float) -> None:
        self.entities: List[Entity] = entities
        self.distance: float = distance

    def get(self) -> Union[Entity, None]:
        if self.has_one():
            return self.entities[0]
        return None

    def has_one(self) -> bool:
        return len(self.entities) == 1

    def get_pos(self) -> Union[Vector, None]:
        if not self.has_one():
            return None
        return self.entities[0].get_pos()

    def get_mean_pos(self) -> Union[Vector, None]:
        if self.has_one():
            return self.get_pos()

        total_x, total_y = 0, 0
        for entity in self.entities:
            total_x += entity.get_pos().x
            total_y += entity.get_pos().y

        mean_x = total_x / len(self.entities)
        mean_y = total_y / len(self.entities)
        return Vector(mean_x, mean_y)
