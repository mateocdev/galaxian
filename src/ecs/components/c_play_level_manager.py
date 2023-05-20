from enum import Enum
from src.ecs.components.c_blink import CBlink

from src.ecs.components.c_bullet_state import CBulletState
from src.ecs.components.c_surface import CSurface

class PlayLevelState(Enum):
    START = 0
    PLAY = 1
    PAUSED = 2
    WON_LEVEL = 3
    GAME_OVER = 4

class CPlayLevelManager:
    def __init__(self, bullet_st:CBulletState, paused_s:CSurface,
                 paused_blk:CBlink, ready_text_entity:int, player_entity:int) -> None:
        self.state:PlayLevelState = PlayLevelState.START
        self.current_attacks = 0
        self.current_attacks_max = 1
        self.current_attack_chance = 1999

        self.time_on_state = 0
        self.time_to_next_level_max = 4

        self.time_to_start_max = 2.5

        self.start_text_ent = -1
        self.win_text_ent = -1
        self.win_text_ent_2 = -1

        self.ready_text_entity = ready_text_entity
        self.player_entity = player_entity
        self.bullet_st:CBulletState = bullet_st
        self.paused_s:CSurface = paused_s
        self.paused_blk:CBlink = paused_blk