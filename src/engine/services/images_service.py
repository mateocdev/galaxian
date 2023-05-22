import pygame


class ImagesService:
    def __init__(self) -> None:
        self._images = {}

    def get(self, path: str) -> pygame.Surface:
        if path not in self._images:
            self._images[path] = pygame.image.load(path).convert_alpha()
        return self._images[path]

    def get_from_surface(self, size: pygame.Vector2, color: pygame.Color):
        path = f"generated_{size}_{color}"
        if path not in self._images:
            self._images[path] = pygame.Surface(size)
            self._images[path].fill(color)
        return self._images[path]
