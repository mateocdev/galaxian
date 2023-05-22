import pygame

class SoundsService:
    def __init__(self) -> None:
        self._sounds:dict[str, pygame.mixer.Sound] = {}

    def play_once(self, path:str) -> pygame.mixer.Channel:
        if path not in self._sounds:
            self._sounds[path] = pygame.mixer.Sound(path)
        return self._sounds[path].play()
    
    def play_loop(self, path:str) -> pygame.mixer.Channel:
        if path not in self._sounds:
            self._sounds[path] = pygame.mixer.Sound(path)
        return self._sounds[path].play(-1)
    
    def stop(self, channel:pygame.mixer.Channel):
        channel.stop()