from abc import ABC, abstractmethod
from vector import Vector

class Entity(ABC):
    @abstractmethod
    def get_pos(self) -> Vector:
        pass

    @abstractmethod
    def get_speed(self) -> Vector:
        pass
