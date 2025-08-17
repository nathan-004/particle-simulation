from dataclasses import dataclass

@dataclass
class Position2D:
    x: float
    y: float

    def __sub__(self, other) -> tuple:
        if isinstance(other, Position2D):
            return (self.x - other.x, self.y - other.y)
        elif type(other) in (int, float):
            return (self.x - other, self.y - other)
        else:
            return NotImplemented
        
    def __iadd__(self, other):
        if isinstance(other, tuple):
            self.x += other[0]
            self.y += other[1]
        elif isinstance(other, Velocity2D):
            self.x += other.vx
            self.y += other.vy
        else:
            return NotImplemented
        return self

@dataclass
class Velocity2D:
    vx: float
    vy: float

    def __iadd__(self, other):
        if isinstance(other, tuple):
            self.vx += other[0]
            self.vy += other[1]
        return self
    
    def __sub__(self, other) -> 'Velocity2D':
        if isinstance(other, Velocity2D):
            return Velocity2D(self.vx - other.vx, self.vy - other.vy)
        elif type(other) in (int, float):
            return Velocity2D(self.vx - other, self.vy - other)
        else:
            return NotImplemented
        
    def length(self) -> float:
        """
        Calculate the length of the velocity vector.
        
        :return: Length of the velocity vector.
        """
        return (self.vx**2 + self.vy**2) ** 0.5