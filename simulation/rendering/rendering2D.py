import pygame

from simulation.physics.particle import Particle
from simulation.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, DEFAULT_BACKGROUND_COLOR, DEFAULT_PARTICLE_COLOR, FPS

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

def render_particles(particles:list[Particle]) -> None:
    """
    Render particles on the screen.

    :param particles: List of particles to render.
    """
    screen.fill(DEFAULT_BACKGROUND_COLOR)  # Clear the screen with black
    for particle in particles:
        pygame.draw.circle(screen, DEFAULT_PARTICLE_COLOR, (int(particle.position.x), int(particle.position.y)), particle.radius)

def main_game_loop():
    def decorator(func):
        def wrapper(*args, **kwargs):
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    
                func(*args, **kwargs)

                pygame.display.flip()
                clock.tick(FPS)
            pygame.quit()
        return wrapper
    return decorator