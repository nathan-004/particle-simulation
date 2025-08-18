from dataclasses import dataclass

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1000
DEFAULT_BACKGROUND_COLOR = (0, 0, 0)  # RGB for black
DEFAULT_PARTICLE_COLOR = (255, 255, 255)  # RGB for white

FPS = 60  # Frames per second for the simulation
MAX_PARTICLE_TRAIL_LENGTH = 100  # Maximum length of the particle trail

G = 2.5 # Gravitational constant
DEFAULT_SOFTENING = 0  # Softening factor for distance calculations
PARTICLE_RADIUS = 5  # Default radius for particles

# Collision parameters
Q_star = 10**2 / 2 # Resistance factor for collisions (J/kg)
c_N = 3.0
beta = 0.8
N_min = 2  # Minimum number of fragments after a collision
alpha = 0.8
s = 2
min_mass = 1.0
rho = 0.5 # Density of the particles
k_ej = 0.1  # Ejection velocity factor
max_fragments = 30  # Maximum number of fragments to generate
min_particle_radius = 1  # Minimum radius for fragments
fragment_lifetime = FPS * 1

@dataclass(frozen=True)
class FragParams:
    Q_star: float = Q_star
    c_N: float = c_N
    beta: float = beta
    N_min: int = N_min
    alpha:float = alpha
    s:float = s
    min_mass: float = min_mass
    rho: float = rho
    k_ej: float = k_ej
    max_fragments: int = max_fragments
    min_particle_radius: int = min_particle_radius
    fragment_lifetime: int = fragment_lifetime