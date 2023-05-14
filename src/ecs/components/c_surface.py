import pygame

class CSurface:
    def __init__(self, size:pygame.Vector2, color:pygame.Color) -> None:
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.area = self.surf.get_rect()

    @classmethod
    def from_surface(cls, surface:pygame.Surface):
        c_surf = cls(pygame.Vector2(0,0), pygame.Color(0,0,0))
        c_surf.surf = surface
        c_surf.area = surface.get_rect()
        return c_surf
    
    @classmethod
    def from_text(cls, text:str, color: pygame.Color, size: int):
        c_surf = cls(pygame.Vector2(0, 0), pygame.Color(0,0,0))
        font = pygame.font.Font("assets/fnt/PressStart2P.ttf", size)
        surface = font.render(text, True, color)
        c_surf.surf = surface
        c_surf.area = surface.get_rect()
        return c_surf