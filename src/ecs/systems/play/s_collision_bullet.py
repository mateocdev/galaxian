import pygame
import esper

from src.create.play_creator import create_explosion
from src.ecs.components.c_bullet_state import BulletStates, CBulletState
from src.ecs.components.c_enemy_state import CEnemyState, EnemyStates
from src.ecs.components.c_play_level_manager import CPlayLevelManager
from src.ecs.components.c_player_state import CPlayerState, PlayerStates
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.service_locator import ServiceLocator


def _check_enemy_collision(world: esper.World, bullet_rect: pygame.Rect,
                           c_b_st: CBulletState, c_lvl_mgr: CPlayLevelManager):
    enemy_query = world.get_components(
        CTagEnemy, CEnemyState, CSurface, CTransform)
    for e_ent, (c_e_tag, c_e_st, c_e_s, c_e_t) in enemy_query:
        enemy_rect = c_e_s.area.copy()
        enemy_rect.topleft = c_e_t.pos.copy()
        if bullet_rect.colliderect(enemy_rect) and c_b_st.state == BulletStates.FIRING and c_b_st.tag == "player":
            if c_e_st.state == EnemyStates.ATTACK:
                c_e_st.attack_channel.stop()
                c_lvl_mgr.current_attacks -= 1
                ServiceLocator.globals_service.player_score += c_e_tag.score_value_attack
                if ServiceLocator.globals_service.player_score > ServiceLocator.globals_service.player_high_score:
                    ServiceLocator.globals_service.player_high_score = ServiceLocator.globals_service.player_score
            else:
                ServiceLocator.globals_service.player_score += c_e_tag.score_value
                if ServiceLocator.globals_service.player_score > ServiceLocator.globals_service.player_high_score:
                    ServiceLocator.globals_service.player_high_score = ServiceLocator.globals_service.player_score
            world.delete_entity(e_ent)
            create_explosion(world, c_e_t.pos, "enemy")
            c_b_st.state = BulletStates.IDLE


def _check_player_collision(world: esper.World, bullet_rect: pygame.Rect, bullet_state: CBulletState, b_ent: int):
    player_query = world.get_components(CPlayerState, CSurface, CTransform)
    for _, (c_pl_st, c_pl_s, c_pl_t) in player_query:
        player_rect = c_pl_s.area.copy()
        player_rect.topleft = c_pl_t.pos.copy()
        if bullet_rect.colliderect(player_rect) \
                and bullet_state.state == BulletStates.FIRING and bullet_state.tag == "enemy" and c_pl_st.state == PlayerStates.ALIVE:
            world.delete_entity(b_ent)
            kill_player(world, c_pl_st, c_pl_s, c_pl_t)


def kill_player(world: esper, c_st: CPlayerState, c_s: CSurface, c_t: CTransform):
    c_st.state = PlayerStates.DEAD
    blast_pos = c_t.pos.copy() - pygame.Vector2(c_s.area.centerx, c_s.area.centery)
    bullet_query = world.get_component(CBulletState)
    for b_ent, c_b_st in bullet_query:
        if c_b_st.tag == "player":
            world.delete_entity(b_ent)
    create_explosion(world, blast_pos, "player")


def system_collision_bullet(world: esper.World, c_lvl_mgr: CPlayLevelManager):
    query = world.get_components(CTransform, CSurface, CBulletState)
    for _, (transform, surface, bullet_state) in query:
        bullet_rect = surface.area.copy()
        bullet_rect.topleft = transform.pos.copy()
        _check_enemy_collision(world, bullet_rect, bullet_state, c_lvl_mgr)
        _check_player_collision(world, bullet_rect, bullet_state, _)
