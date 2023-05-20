from enum import Enum
import pygame


class BulletStates(Enum):
    IDLE = 0
    FIRING = 1


class CBulletState:
    def __init__(self, tag: str, velocity: pygame.Vector2) -> None:
        self.tag = tag
        self.velocity = velocity
        self.state: BulletStates = BulletStates.IDLE
