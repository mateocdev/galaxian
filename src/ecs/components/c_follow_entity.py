import pygame

class CFollowEntity():
    def __init__(self, entity_to_follow:int, offset:pygame.Vector2) -> None:
        self.entity_to_follow_in:int = entity_to_follow
        self.offset = offset