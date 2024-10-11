import math


class Vector:
    ZERO = None

    def __init__(self, a=None, b=None):
        if isinstance(a, Vector) and isinstance(b, Vector):
            self.x = b.x - a.x
            self.y = b.y - a.y
        elif b is None:
            self.x = math.cos(a)
            self.y = math.sin(a)
        else:
            self.x = a
            self.y = b

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def rotate(self, angle: float) -> "Vector":
        nx = (self.x * math.cos(angle)) - (self.y * math.sin(angle))
        ny = (self.x * math.sin(angle)) + (self.y * math.cos(angle))
        return Vector(nx, ny)

    def round(self) -> "Vector":
        return Vector(round(self.x), round(self.y))

    def truncate(self) -> "Vector":
        return Vector(int(self.x), int(self.y))

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

    def distance(self, other: "Vector") -> float:
        return ((other.x - self.x) ** 2 + (other.y - self.y) ** 2) ** 0.5

    def in_range(self, other: "Vector", range_: float) -> bool:
        return (other.x - self.x) ** 2 + (other.y - self.y) ** 2 <= range_**2

    def add(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def mult(self, factor: float) -> "Vector":
        return Vector(self.x * factor, self.y * factor)

    def sub(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def length(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

    def length_squared(self) -> float:
        return self.x**2 + self.y**2

    def normalize(self) -> "Vector":
        length = self.length()
        if length == 0:
            return Vector(0, 0)
        return Vector(self.x / length, self.y / length)

    def dot(self, other: "Vector") -> float:
        return self.x * other.x + self.y * other.y

    def angle(self) -> float:
        return math.atan2(self.y, self.x)

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}]"

    def to_int_string(self) -> str:
        return f"{int(self.x)} {int(self.y)}"

    def project(self, force: "Vector") -> "Vector":
        normalize = self.normalize()
        return normalize.mult(normalize.dot(force))

    def cross(self, s: float) -> "Vector":
        return Vector(-s * self.y, s * self.x)

    def vsymmetric(self, center=None) -> "Vector":
        if center is None:
            return Vector(int(self.x), int(-self.y))
        else:
            return Vector(int(self.x), int(2 * center - self.y))

    def hsymmetric(self, center=None) -> "Vector":
        if center is None:
            return Vector(int(-self.x), int(self.y))
        else:
            return Vector(int(2 * center - self.x), int(self.y))

    def symmetric(self, center=None) -> "Vector":
        if center is None:
            return Vector(0, 0)
        else:
            return Vector(int(2 * center.x - self.x), int(2 * center.y - self.y))

    def within_bounds(self, minx: float, miny: float, maxx: float, maxy: float) -> bool:
        return minx <= self.x < maxx and miny <= self.y < maxy

    def is_zero(self) -> bool:
        return self.x == 0 and self.y == 0

    def symmetric_truncate(self, origin: "Vector" = None) -> "Vector":
        origin = origin if origin else Vector(0, 0)
        return self.sub(origin).truncate().add(origin)

    def euclidean_to(self, x: float, y: float) -> float:
        return ((x - self.x) ** 2 + (y - self.y) ** 2) ** 0.5

    def sqr_euclidean_to(self, x: float, y: float) -> float:
        return (x - self.x) ** 2 + (y - self.y) ** 2

    def sqr_euclidean_to(self, a, b=None):
        if isinstance(a, Vector):
            return (self.x - a.x) ** 2 + (self.y - a.y) ** 2
        else:
            if b is not None:
                return (a - self.x) ** 2 + (b - self.y) ** 2
            else:
                raise RuntimeError("b is None")

    def manhattan_to(self, x: float, y: float) -> float:
        return abs(x - self.x) + abs(y - self.y)

    def chebyshev_to(self, x: float, y: float) -> float:
        return max(abs(x - self.x), abs(y - self.y))

    def epsilon_round(self) -> "Vector":
        return Vector(
            round(self.x * 10000000) / 10000000, round(self.y * 10000000) / 10000000
        )
