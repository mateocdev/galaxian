from enum import Enum

class PlayerStates(Enum):
    ALIVE = 0,
    DEAD = 1

class CPlayerState:
    def __init__(self, lives) -> None:
        self.state:PlayerStates = PlayerStates.ALIVE
        self.lives = lives
        self.dead_time = 4
        self.curr_dead_time = 0