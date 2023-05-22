import pygame

from src.engine.service_locator import ServiceLocator


class CSurface:
    def __init__(self, size: pygame.Vector2, color: pygame.Color) -> None:
        self.surf = ServiceLocator.images_service.get_from_surface(size, color)
        self.area: pygame.Rect = self.surf.get_rect()
        self.visible = True
        self.color = color

    @classmethod
    def from_surface(cls, surface: pygame.Surface):
        c_surf = cls(pygame.Vector2(0, 0), pygame.Color(0, 0, 0))
        c_surf.surf = surface
        c_surf.area = surface.get_rect()
        return c_surf

    @classmethod
    def from_text(cls, text: str, font: pygame.font.Font, color: pygame.color):
        c_surf = cls(pygame.Vector2(0, 0), pygame.Color(0, 0, 0))
        c_surf.surf = font.render(text, True, color)
        c_surf.area = c_surf.surf.get_rect()
        c_surf.color = color
        return c_surf
