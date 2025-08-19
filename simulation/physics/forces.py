import math
import numpy as np
from typing import NamedTuple

from simulation.physics.particle import Particle, ParticleFragment
from simulation.utils.positions import Position2D, Velocity2D
from simulation.utils.constants import G, DEFAULT_SOFTENING, FragParams


class ParticleData(NamedTuple):
    mass:float
    radius:float

def distance_euclidienne(
    p1: Particle, p2: Particle, softening: float = DEFAULT_SOFTENING
) -> float:
    """
    Calculate the Euclidean distance between two particles.

    :param p1: First particle.
    :param p2: Second particle.
    :param softening: Small value added to the squared distance to stabilize force.
    :return: Euclidean distance between the two particles.
    """
    dx = p1.position.x - p2.position.x
    dy = p1.position.y - p2.position.y
    return (dx**2 + dy**2 + softening**2) ** 0.5


def force_gravitationnelle(p1: Particle, p2: Particle) -> float:
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


def is_collision(p1: Particle, p2: Particle) -> bool:
    """
    Check if two particles collide based on their positions and radii.

    :param p1: First particle.
    :param p2: Second particle.
    :return: True if particles collide, False otherwise.
    """
    distance = distance_euclidienne(p1, p2)
    return distance <= (p1.radius + p2.radius)


def resolve_collision(p1: Particle, p2: Particle) -> None:
    """
    Resolve the collision between two particles by inverting their velocities.

    :param p1: First particle.
    :param p2: Second particle.
    """
    print(f"Collision non explosive between particles {p1} and {p2}")
    dx, dy = p1.position - p2.position
    dist = distance_euclidienne(p1, p2)
    if dist != 0:
        nx, ny = dx / dist, dy / dist  # Normalized direction vector
    else:
        nx, ny = 1, 0

    v1 = p1.velocity.vx * nx + p1.velocity.vy * ny
    v2 = p2.velocity.vx * nx + p2.velocity.vy * ny

    # Nouvelles vitesses normales (collision élastique)
    m1, m2 = p1.mass, p2.mass
    v1n_new = (v1 * (m1 - m2) + 2 * m2 * v2) / (m1 + m2)
    v2n_new = (v2 * (m2 - m1) + 2 * m1 * v1) / (m1 + m2)

    # Mise à jour des vitesses finales
    p1.velocity += (v1n_new - v1) * nx, (v1n_new - v1) * ny
    p2.velocity += (v2n_new - v2) * nx, (v2n_new - v2) * ny
    print(f"New velocities: {p1.velocity}, {p2.velocity}")

def resolve_colision_fragment(p1: Particle, p2: Particle) -> None:
    """
    Resolve the collision between two particles by exploding them into fragments.
    :param p1: First particle.
    :param p2: Second particle.
    """
    # Energy of the collision
    vrelative = p1.velocity - p2.velocity
    vrelative_norm = vrelative.length()

    relative_mass = p1.mass * p2.mass / (p1.mass + p2.mass)
    energy = 0.5 * relative_mass * vrelative_norm**2
    print(f"Collision energy: {energy}")

    # Decide if the collision is explosive
    victim = p1 if p1.mass < p2.mass else p2
    impactor = p2 if p1.mass < p2.mass else p1
    E_seuil = FragParams.Q_star * victim.mass

    if not (energy > E_seuil):
        # Normal collision resolution
        resolve_collision(p1, p2)
        return
    
    # Explosive collision resolution
    rate_break = min(0.09, FragParams.c_N * (energy / E_seuil - 1) ** FragParams.beta)
    M_frag = rate_break * victim.mass
    M_surv = victim.mass - M_frag
    print(f"Fragment mass: {M_frag}, Surviving mass: {M_surv}")

    # Fragment Number
    N = FragParams.N_min + math.floor(FragParams.c_N * (energy / E_seuil) ** FragParams.alpha)
    N = min(N, FragParams.max_fragments)
    print(f"Number of fragments: {N}")

    # Repartition of mass
    fragments = generate_fragment(N, M_frag, FragParams.s, FragParams.min_mass)
    masses = np.array([frag.mass for frag in fragments])

    # Speed of the fragments
    angles = np.random.uniform(0, 2 * np.pi, N)
    v_eject = np.sqrt(energy / masses) * FragParams.k_ej
    print(f"Fragment ejection speed: {v_eject}")
    vx = victim.velocity.vx + v_eject * np.cos(angles)
    vy = victim.velocity.vy + v_eject * np.sin(angles)
    print(f"Fragments velocities: {vx}, {vy}")

    # Create new particles for fragments
    particles = []

    for i, frag in enumerate(fragments):
        print(f"Creating fragment {i+1}/{N} with mass {frag.mass} and radius {frag.radius}")
        new_particle = ParticleFragment(
            mass=frag.mass,
            position=Position2D(victim.position.x, victim.position.y),
            velocity=Velocity2D(vx[i], vy[i]),
            radius=frag.radius,
            color=victim.color
        )
        particles.append(new_particle)

    victim.radius = victim.radius * M_surv / victim.mass  # Update the radius based on the new mass
    victim.mass = M_surv  # Update the mass of the surviving particle

    if victim.radius < FragParams.min_particle_radius:
        victim.lifetime = 0  # If the radius is too small, set lifetime to 0

    print(f"Surviving particle updated: {victim.mass} kg, radius {victim.radius}")
    resolve_collision(victim, impactor)  # Resolve collision for the original particles

    print(f"Collision explosive between particles {p1} and {p2}, generating {len(particles)} fragments.")
    return particles


def generate_fragment(N:int, M_frag, s:float = FragParams.s, min_mass:float = FragParams.min_mass) -> ParticleData:
    """
    Generate fraagment particles after a collision.

    :param N: Number of fragments to generate.
    :param M_frag: Total mass of the fragments.
    :param s: exponent for mass distribution.
    :return: List of generated fragment particles.
    """
    raw_sample = (np.random.pareto(s, N) + 1) * min_mass
    masses = raw_sample / raw_sample.sum() * M_frag

    radius = np.sqrt(masses / (np.pi * FragParams.rho))

    fragments = []

    for mass, rad in zip(masses, radius):
        fragments.append(
            ParticleData(
                mass=mass,
                radius=max(rad, FragParams.min_particle_radius)  # Ensure radius is not less than minimum
            )
        )
    
    return fragments