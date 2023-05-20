from enum import Enum
import pygame

class TextAlignment(Enum):
    LEFT = 0,
    RIGHT = 1
    CENTER = 2
    
class CChangingText:
    def __init__(self, text:str, font:pygame.font.Font, alignment:TextAlignment) -> None:
        self.font = font
        self.text = text
        self.alignment:TextAlignment = alignment