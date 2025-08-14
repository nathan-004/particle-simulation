from simulation.physics.particle import Particle
from simulation.utils.positions import Position2D, Velocity2D
from simulation.utils.constants import G

def distance_euclidienne(p1:Particle, p2:Particle) -> float:
    """
    Calculate the Euclidean distance between two particles.

    :param p1: First particle.
    :param p2: Second particle.
    :return: Euclidean distance between the two particles.
    """
    dx = p1.position.x - p2.position.x
    dy = p1.position.y - p2.position.y
    return (dx**2 + dy**2)**0.5

def force_gravitationnelle(p1:Particle, p2:Particle) -> float:
    """
    Calculate the gravitational force between two particles.

    :param p1: First particle.
    :param p2: Second particle.
    :return: Gravitational force between the two particles.
    """
    distance = distance_euclidienne(p1, p2)
    
    if distance == 0:
        return 0  # Avoid division by zero
    
    force = G * (p1.mass * p2.mass) / (distance**2)
    return force

def collision(p1:Particle, p2:Particle) -> bool:
    """
    Check if two particles collide based on their positions and radii.

    :param p1: First particle.
    :param p2: Second particle.
    :return: True if particles collide, False otherwise.
    """
    distance = distance_euclidienne(p1, p2)
    return distance <= (p1.radius + p2.radius)