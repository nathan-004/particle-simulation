from simulation.physics.particle import *
from simulation.rendering.rendering2D import *
from simulation.physics.forces import distance_euclidienne, force_gravitationnelle, collision

def init_environment():
    """
    Initialize the simulation environment.
    
    This function sets up the necessary components for the simulation,
    including loading configurations and initializing particle systems.
    """
    
    # Initialize particle systems
    particles = [
        Particle(mass=1000.0, position=Position2D(520, 500), velocity=Velocity2D(0, 0), radius=15),  # "planète" centrale
        Particle(mass=10.0, position=Position2D(570, 500), velocity=Velocity2D(0, 4), radius=8),     # "satellite" en orbite
        Particle(mass=10.0, position=Position2D(570, 500), velocity=Velocity2D(0, 4), radius=8),
        Particle(mass=10.0, position=Position2D(570, 500), velocity=Velocity2D(0, 4), radius=8),
    ]
    
    return particles

particles = init_environment()

@main_game_loop()
def main():
    for particle in particles:
        force_totale_x = 0
        force_totale_y = 0

        for other_particle in particles:
            if particle != other_particle:
                if collision(particle, other_particle):
                    particle.invert_velocity()  # Invert velocity on collision
                    other_particle.invert_velocity()  # Invert velocity of the other particle
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

        particle.velocity += (ax, ay)
    
    for particle in particles:
        particle.update_position()

    render_particles(particles)