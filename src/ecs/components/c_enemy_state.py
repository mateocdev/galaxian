from enum import Enum
import random
import pygame


class EnemyStates(Enum):
    IDLE = (0,)
    HIT = (1,)
    BACK_TO_FOLD = 2


class CEnemyState:
    def __init__(self) -> None:
        self.state: EnemyStates = EnemyStates.IDLE
        self.gravity_vector: pygame.Vector2 = pygame.Vector2(0, 0)
        self.follow_vector: pygame.Vector2 = pygame.Vector2(0, 0)
        self.old_velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.fold_pos: pygame.Vector2 = pygame.Vector2(0, 0)

        self.attack_channel: pygame.mixer.Channel = None
        self.rng: random.Random = random.Random()
        self.fire_chance: int = 1999
        self.fire_chance_attack: int = 1950
