from simulation.physics.particle import *
from simulation.rendering.rendering2D import *

def init_environment():
    """
    Initialize the simulation environment.
    
    This function sets up the necessary components for the simulation,
    including loading configurations and initializing particle systems.
    """
    
    # Initialize particle systems
    particles = [
        Particle(mass=1.0, position=Position2D(0, 0), velocity=Velocity2D(1, 0)),
        Particle(mass=2.0, position=Position2D(1, 1), velocity=Velocity2D(0, 1)),
    ]
    
    return particles

particles = init_environment()

@main_game_loop()
def main():
    render_particles(particles)