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

def is_collision(p1:Particle, p2:Particle) -> bool:
    """
    Check if two particles collide based on their positions and radii.

    :param p1: First particle.
    :param p2: Second particle.
    :return: True if particles collide, False otherwise.
    """
    distance = distance_euclidienne(p1, p2)
    return distance <= (p1.radius + p2.radius)

def resolve_collision(p1:Particle, p2:Particle) -> None:
    """
    Resolve the collision between two particles by inverting their velocities.

    :param p1: First particle.
    :param p2: Second particle.
    """
    dx, dy = p1.position - p2.position
    dist = distance_euclidienne(p1, p2)
    nx, ny = dx / dist, dy / dist  # Normalized direction vector

    v1 = p1.velocity.vx * nx + p1.velocity.vy * ny
    v2 = p2.velocity.vx * nx + p2.velocity.vy * ny

    # Nouvelles vitesses normales (collision élastique)
    m1, m2 = p1.mass, p2.mass
    v1n_new = (v1 * (m1 - m2) + 2 * m2 * v2) / (m1 + m2)
    v2n_new = (v2 * (m2 - m1) + 2 * m1 * v1) / (m1 + m2)

    # Mise à jour des vitesses finales
    p1.velocity += (v1n_new - v1) * nx, (v1n_new - v1) * ny
    p2.velocity += (v2n_new - v2) * nx, (v2n_new - v2) * ny