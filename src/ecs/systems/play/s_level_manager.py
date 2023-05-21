import esper

from src.ecs.components.c_play_level_manager import CPlayLevelManager, PlayLevelState
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.create.interface_creator import create_win_text
from src.create.play_creator import create_all_enemies, create_player_bullet
from src.engine.service_locator import ServiceLocator


def system_level_manager(
    world: esper.World, c_lvl_mgr: CPlayLevelManager, delta_time: float
):
    if c_lvl_mgr.state == PlayLevelState.START:
        c_lvl_mgr.time_on_state += delta_time
        if c_lvl_mgr.time_on_state > c_lvl_mgr.time_to_start_max:
            create_all_enemies(world)
            world.delete_entity(c_lvl_mgr.ready_text_entity)
            c_lvl_mgr.state = PlayLevelState.PLAY
        return
    elif c_lvl_mgr.state == PlayLevelState.PLAY:
        query = world.get_component(CTagEnemy)
        if len(query) < 20:
            c_lvl_mgr.current_attacks_max = 2
            c_lvl_mgr.current_attack_chance = 1900
        else:
            c_lvl_mgr.current_attacks_max = 1
            c_lvl_mgr.current_attack_chance = 1999

        if len(query) <= 0:
            c_lvl_mgr.time_on_state = 0
            c_lvl_mgr.win_text_ent, c_lvl_mgr.win_text_ent_2 = create_win_text(world)
            c_lvl_mgr.state = PlayLevelState.WON_LEVEL
    elif c_lvl_mgr.state == PlayLevelState.WON_LEVEL:
        c_lvl_mgr.time_on_state += delta_time
        if c_lvl_mgr.time_on_state > 4:
            c_lvl_mgr.time_on_state = 0

            ServiceLocator.globals_service.current_level += 1
            c_lvl_mgr.current_attacks = 0
            world.delete_entity(c_lvl_mgr.win_text_ent)
            world.delete_entity(c_lvl_mgr.win_text_ent_2)
            c_lvl_mgr.win_text_ent = -1
            c_lvl_mgr.win_text_ent_2 = -1
            create_all_enemies(world)
            c_lvl_mgr.state = PlayLevelState.PLAY
    elif c_lvl_mgr.state == PlayLevelState.GAME_OVER:
        pass
    elif c_lvl_mgr.state == PlayLevelState.PAUSED:
        pass
