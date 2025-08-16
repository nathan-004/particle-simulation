from random import randint
from typing import Optional

from simulation.physics.particle import *
from simulation.rendering.rendering2D import *
from simulation.physics.forces import distance_euclidienne, force_gravitationnelle, is_collision, resolve_collision
from simulation.utils.constants import FPS, SCREEN_WIDTH, SCREEN_HEIGHT

def init_particle(mass, position:Optional[tuple], velocity:Optional[tuple], radius:float, n:int):
    """
    Initialize a particle with its properties.

    :param mass: Mass of the particle.
    :param position: Initial position of the particle.
    :param velocity: Initial velocity of the particle.
    :param radius: Radius of the particle.
    :param n: Number of particles to initialize.
    :return: List of initialized particles.
    """
    particles = []
    for _ in range(n):
        if position is None:
            x = randint(0, SCREEN_WIDTH)
            y = randint(0, SCREEN_HEIGHT)
            position_ = (x, y)
        else:
            position_ = position
        if velocity is None:
            vx = randint(-6, 6)
            vy = randint(-6, 6)
            velocity_ = (vx, vy)
        else:
            velocity_ = velocity
        particle = Particle(mass=mass, position=Position2D(*position_), velocity=Velocity2D(*velocity_), radius=radius)
        particles.append(particle)
    return particles

def init_environment():
    """
    Initialize the simulation environment.
    
    This function sets up the necessary components for the simulation,
    including loading configurations and initializing particle systems.
    """
    # Initialize particle systems
    particles = [
        Particle(mass=1000.0, position=Position2D(400, 300), velocity=Velocity2D(0, 0), radius=15, color=(0, 100, 255)),      # Terre (bleu)
        Particle(mass=10.0, position=Position2D(500, 300), velocity=Velocity2D(0, 6), radius=8, color=(220, 220, 220)),      # Lune 1 (blanc)
        Particle(mass=10.0, position=Position2D(400, 400), velocity=Velocity2D(6, 0), radius=8, color=(255, 200, 0)),        # Lune 2 (jaune)
        Particle(mass=10.0, position=Position2D(300, 300), velocity=Velocity2D(0, -6), radius=8, color=(255, 80, 80)),       # Lune 3 (rouge)
        Particle(mass=10.0, position=Position2D(400, 200), velocity=Velocity2D(-6, 0), radius=8, color=(80, 255, 80)),     # Lune 4 (vert)
    ]

    # particles = [
    #     *init_particle(mass=100.0, position=None, velocity=None, radius=50, n=2),
    #     Particle(mass=5000.0, position=Position2D(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), velocity=Velocity2D(0, 0), radius=15)
    # ]
    
    return particles

particles = init_environment()

@main_game_loop()
def main():
    dt = 1  # Time step for the simulation
    for idx, particle in enumerate(particles):
        force_totale_x = 0
        force_totale_y = 0

        for other_particle in particles:
            if particle != other_particle:
                if is_collision(particle, other_particle):
                    continue
                force = force_gravitationnelle(particle, other_particle)
                distance = distance_euclidienne(particle, other_particle)
                
                # Calculate the direction of the force
                dx, dy = other_particle.position - particle.position
                
                if distance > 0:
                    force_totale_x += (force * dx / distance)
                    force_totale_y += (force * dy / distance)
        
        ax = force_totale_x / particle.mass
        ay = force_totale_y / particle.mass

        particle.velocity += (ax * dt, ay * dt)
    
    for idx, particle in enumerate(particles):
        for other_particle in particles[idx + 1:]:
            if is_collision(particle, other_particle):
                resolve_collision(particle, other_particle)

    for particle in particles:
        particle.update_position(dt)

    render_particles(particles)