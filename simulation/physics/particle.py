from simulation.utils.positions import Position2D, Velocity2D

class Particle:
    """Contains information about a particle in a simulation."""
    def __init__(self, mass, position:Position2D, velocity:Velocity2D, radius:int = 5):
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