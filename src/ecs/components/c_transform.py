import pygame

class CTransform:
    def __init__(self, pos:pygame.Vector2) -> None:
        self.pos = pos
        self.rot_deg = 0