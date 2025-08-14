import pygame

from simulation.physics.particle import Particle

pygame.init()

screen = pygame.display.set_mode((1500, 1000))
running = True

def render_particles(particles:list[Particle]) -> None:
    """
    Render particles on the screen.

    :param particles: List of particles to render.
    """
    screen.fill((0, 0, 0))  # Clear the screen with black
    for particle in particles:
        pygame.draw.circle(screen, (255, 255, 255), (int(particle.position.x), int(particle.position.y)), 5)

def main_game_loop():
    def decorator(func):
        def wrapper(*args, **kwargs):
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    
                func(*args, **kwargs)

                pygame.display.flip()
            pygame.quit()
        return wrapper
    return decorator