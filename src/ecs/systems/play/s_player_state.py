import esper
from src.ecs.components.c_play_level_manager import CPlayLevelManager, PlayLevelState
from src.ecs.components.c_player_state import CPlayerState, PlayerStates
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.service_locator import ServiceLocator

from src.create.interface_creator import create_game_over
from src.create.play_creator import create_bullet_player


def system_player_state(
    world: esper.World, c_lvl_mgr: CPlayLevelManager, delta_time: float
):
    player_cfg = ServiceLocator.configs_service.get("assets/cfg/player.json")
    query = world.get_components(CPlayerState, CSurface, CTransform)
    for pl_ent, (c_st, c_s, c_tr) in query:
        if c_st.state == PlayerStates.ALIVE:
            pass
        elif c_st.state == PlayerStates.DEAD:
            c_s.visible = False
            c_st.curr_dead_time += delta_time
            if c_st.curr_dead_time >= c_st.dead_time:
                if c_st.lives > 0:
                    c_st.lives -= 1
                    c_tr.pos.x = player_cfg["spawn_point"]["x"]
                    c_tr.pos.y = player_cfg["spawn_point"]["y"]
                    c_st.curr_dead_time = 0
                    c_s.visible = True
                    c_st.state = PlayerStates.ALIVE
                    c_lvl_mgr.bullet_st = create_bullet_player(world, pl_ent)
                else:
                    if c_lvl_mgr.state != PlayLevelState.GAME_OVER:
                        level_cfg = ServiceLocator.configs_service.get(
                            "assets/cfg/level_01.json"
                        )
                        ServiceLocator.sounds_service.play_once(
                            level_cfg["game_over_sound"]
                        )
                        c_lvl_mgr.state = PlayLevelState.GAME_OVER
                        create_game_over_text(world)
