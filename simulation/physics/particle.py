from simulation.utils.positions import Position2D, Velocity2D
from simulation.utils.constants import PARTICLE_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT

class Particle:
    """Contains information about a particle in a simulation."""
    def __init__(self, mass, position:Position2D, velocity:Velocity2D, radius:int = PARTICLE_RADIUS):
        """
        Initialize a particle with its properties.

        :param mass: Mass of the particle.
        :param position: Initial position of the particle.
        :param velocity: Initial velocity of the particle.
        """
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.radius = radius

    def invert_velocity(self):
        """
        Invert the particle's velocity.
        This is used to simulate a bounce or collision response.
        """
        self.velocity.vx = -self.velocity.vx
        self.velocity.vy = -self.velocity.vy

    def update_position(self, dt:float) -> None:
        """
        Update the particle's position based on its current velocity.
        """
        self.position += (self.velocity.vx * dt, self.velocity.vy * dt)

        if self.touch_ground('x'):
            self.velocity.vx = -self.velocity.vx
            self.position.x = abs(self.position.x) if self.position.x < 0 else SCREEN_WIDTH - (self.position.x - SCREEN_WIDTH)
        if self.touch_ground('y'):
            self.velocity.vy = -self.velocity.vy
            self.position.y = abs(self.position.y) if self.position.y < 0 else SCREEN_HEIGHT - (self.position.y - SCREEN_HEIGHT)

    def touch_ground(self, axis='y'):
        """
        Check if the particle is touching the ground (boundary on the specified axis).
        
        :param axis: 'x' or 'y' to check the corresponding boundary.
        :return: True if the particle is touching the boundary, False otherwise.
        """
        if axis == 'y':
            return self.position.y <= 0 or self.position.y >= SCREEN_HEIGHT - self.radius
        elif axis == 'x':
            return self.position.x <= 0 or self.position.x >= SCREEN_WIDTH - self.radius
        else:
            raise ValueError("axis must be 'x' or 'y'")