import pygame
import esper

from src.ecs.components.c_enemy_state import CEnemyState, EnemyStates
from src.ecs.components.c_play_level_manager import CPlayLevelManager
from src.ecs.components.c_player_state import CPlayerState, PlayerStates
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.systems.play.s_collision_bullet import kill_player

def system_collision_player(world:esper.World, c_lvl_mgr:CPlayLevelManager):
    query = world.get_components(CPlayerState, CSurface, CTransform)
    for _, (c_pl_st, c_pl_s, c_pl_t) in query:
        player_rect = c_pl_s.area.copy()
        player_rect.topleft = c_pl_t.pos.copy()
        _check_enemy_collision(world, player_rect, c_pl_st, c_pl_s, c_pl_t, c_lvl_mgr)

def _check_enemy_collision(world:esper.World, player_rect:pygame.Rect, 
                           c_pl_st:CPlayerState, c_pl_s:CSurface, c_pl_t:CTransform, 
                           c_lvl_mgr:CPlayLevelManager):
    enemy_query = world.get_components(CEnemyState, CSurface, CTransform)
    for e_ent, (c_e_st, c_e_s, c_e_t) in enemy_query:
        enemy_rect = c_e_s.area.copy()
        enemy_rect.topleft = c_e_t.pos.copy()
        if player_rect.colliderect(enemy_rect) and c_pl_st.state == PlayerStates.ALIVE:
            if c_e_st.state == EnemyStates.ATTACK:
                c_lvl_mgr.current_attacks -= 1
                c_e_st.attack_channel.stop()
            world.delete_entity(e_ent)
            kill_player(world, c_pl_st, c_pl_s, c_pl_t)
