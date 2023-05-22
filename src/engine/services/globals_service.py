from enum import Enum

class DebugViewMode(Enum):
    NONE = 1
    RECTS = 2
    ENEMIES = 3
    
class GlobalsService:
    def __init__(self) -> None:
        self.player_score = 0
        self.player_high_score = 0
        self.current_level = 0
        self.from_play = False
        self.debug_view:DebugViewMode = DebugViewMode.NONE