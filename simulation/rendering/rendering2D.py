import pygame
import time

from simulation.physics.particle import Particle
from simulation.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, DEFAULT_BACKGROUND_COLOR, DEFAULT_PARTICLE_COLOR, FPS
from simulation.utils.positions import Position2D, Velocity2D

pygame.init()
pygame.font.init()

fps_text = pygame.font.SysFont('Comic Sans MS', 30)
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
        pygame.draw.circle(screen, particle.color, (int(particle.position.x), int(particle.position.y)), particle.radius)
        if len(particle.trail) > 1:
            pygame.draw.lines(screen, particle.color, False, particle.trail, 1)
        particle.trail.append(pygame.Vector2(particle.position.x, particle.position.y))

def main_game_loop():
    def decorator(func):
        def wrapper(*args, **kwargs):
            while running:
                new_object = None
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        new_object = (1000, Position2D(event.pos[0], event.pos[1]) , Velocity2D(0, 0), 1, "black", 1)

                func(*args, **kwargs, add_object = new_object)

                fps_text_surface = fps_text.render(f"FPS : {clock.get_fps()}", False, (255, 255, 255))
                screen.blit(fps_text_surface, (0,0))
                pygame.display.flip()
                clock.tick(FPS)
            pygame.quit()
        return wrapper
    return decorator