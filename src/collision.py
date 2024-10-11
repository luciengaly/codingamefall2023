from typing import Optional
from entity import Entity

class Collision:
    NONE = None  # Si nécessaire, initialiser à une instance de Collision avec t = -1

    def __init__(self, t: float, a: Optional[Entity] = None, b: Optional[Entity] = None) -> None:
        self.t: float = t
        self.a: Optional[Entity] = a
        self.b: Optional[Entity] = b

    def happened(self) -> bool:
        return self.t >= 0
