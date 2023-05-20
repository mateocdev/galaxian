import esper
from src.ecs.components.c_changing_text import CChangingText
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_level_counter import CTagLevelCounter
from src.ecs.components.tags.c_tag_life import CTagLife
from src.ecs.components.tags.c_tag_score import CTagScore
from src.engine.service_locator import ServiceLocator


def system_interface_tracker(world: esper.World):
    lives = 0
    player_query = world.get_component(CPlayerState)
    for _, c_st in player_query:
        lives = c_st.lives
    life_query = world.get_components(CSurface, CTagLife)
    for _, (c_s, _) in life_query:
        lives -= 1
        if lives < 0:
            c_s.visible = False
        else:
            c_s.visible = True

    score_query = world.get_components(CTagScore, CChangingText)
    for _, (c_tag, c_chg) in score_query:
        if not c_tag.high_score:
            c_chg.text = f"{ServiceLocator.globals_service.player_score:02d}"
        else:
            if ServiceLocator.globals_service.player_score > ServiceLocator.globals_service.player_high_score:
                c_chg.text = f"{ServiceLocator.globals_service.player_score:02d}"
            else:
                c_chg.text = f"{ServiceLocator.globals_service.player_high_score:02d}"

    level_query = world.get_components(CTagLevelCounter, CChangingText)
    for _, (_, c_chg) in level_query:
        c_chg.text = f"{ServiceLocator.globals_service.current_level:02d}"
