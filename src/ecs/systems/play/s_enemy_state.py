import math

import esper
from src.create.play_creator import create_bullet_enemy
from src.ecs.components.c_animation import CAnimation, set_animation

from src.ecs.components.c_enemy_state import CEnemyState, EnemyStates
from src.ecs.components.c_play_level_manager import CPlayLevelManager
from src.ecs.components.c_player_state import CPlayerState, PlayerStates
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator


def system_enemy_state(
    world: esper.World,
    lvl_mgr: CPlayLevelManager,
    player_tr: CTransform,
    player_st: CPlayerState,
    delta_time: float,
):
    query = world.get_components(
        CEnemyState, CVelocity, CSurface, CTransform, CAnimation
    )
    for _, (c_st, c_v, c_s, c_tr, c_a) in query:
        _calculate_bullet_generation(world, c_st, c_tr, c_s, player_tr, player_st)
        if c_st.state == EnemyStates.IDLE:
            _do_enemy_idle(c_st, c_tr, c_v, c_a, player_st, lvl_mgr)
        elif c_st.state == EnemyStates.ATTACK:
            _do_enemy_attack(c_st, c_tr, c_v, player_tr, delta_time)
        elif c_st.state == EnemyStates.BACK_TO_FOLD:
            _do_enemy_back_to_fold(c_st, c_tr, c_v, c_a, delta_time, lvl_mgr)


def _calculate_bullet_generation(
    world: esper.World,
    c_st: CEnemyState,
    c_tr: CTransform,
    c_s: CSurface,
    player_tr: CTransform,
    player_st: CPlayerState,
):
    if c_st.state == EnemyStates.BACK_TO_FOLD or player_st.state == PlayerStates.DEAD:
        return
    rnd = c_st.rng.randint(0, 2000)
    max_rdn = c_st.fire_chance
    if c_st.state == EnemyStates.ATTACK:
        max_rdn = c_st.fire_chance_attack
    if rnd > max_rdn:
        pos = c_tr.pos.copy()
        pos.x += 5
        pos.y += 5
        vel_x = 0
        if c_st.state == EnemyStates.ATTACK:
            vel_x = abs(player_tr.pos.x - pos.x)
            vel_x = min(5, vel_x)
            vel_x *= math.copysign(vel_x, player_tr.pos.x - pos.x)
        create_bullet_enemy(world, pos, vel_x)


def _do_enemy_idle(
    c_st: CEnemyState,
    c_tr: CTransform,
    c_v: CVelocity,
    c_a: CAnimation,
    player_st: CPlayerState,
    lvl_mgr: CPlayLevelManager,
):
    c_tr.pos.x = c_st.fold_pos.x
    c_tr.pos.y = c_st.fold_pos.y
    if lvl_mgr.current_attacks > lvl_mgr.current_attacks_max:
        return

    rnd = c_st.rng.randint(0, 2000)
    if rnd > lvl_mgr.current_attack_chance and player_st.state != PlayerStates.DEAD:
        lvl_mgr.current_attacks += 1
        c_st.old_velocity = c_v.vel.copy()
        c_st.gravity_vector.y = -75
        set_animation(c_a, "ATTACK")
        enemies_cfg = ServiceLocator.configs_service.get("assets/cfg/enemies.json")
        c_st.attack_channel = ServiceLocator.sounds_service.play_once(
            enemies_cfg["launch_sound"]
        )
        c_st.state = EnemyStates.ATTACK


def _do_enemy_attack(
    c_st: CEnemyState,
    c_tr: CTransform,
    c_v: CVelocity,
    player_tr: CTransform,
    delta_time: float,
):
    c_tr.rot_deg -= delta_time * 225
    if c_tr.rot_deg < -180:
        c_tr.rot_deg = -180
    c_st.gravity_vector.y += delta_time * 200
    if c_st.gravity_vector.y > 65:
        c_st.gravity_vector.y = 65
    target_pos = player_tr.pos.copy()
    target_vel = target_pos - c_tr.pos
    target_vel.y = 0

    c_st.follow_vector = c_st.follow_vector.lerp(target_vel, delta_time * 10)
    if c_st.follow_vector.magnitude() > 65:
        c_st.follow_vector.scale_to_length(65)
    c_v.vel = c_st.follow_vector + c_st.gravity_vector
    if c_tr.pos.y > 240:
        c_st.follow_vector.xy = 0, 0
        c_st.gravity_vector.xy = 0, 0
        c_tr.pos.y = -50
        c_st.state = EnemyStates.BACK_TO_FOLD
        c_st.attack_channel = None


def _do_enemy_back_to_fold(
    c_st: CEnemyState,
    c_tr: CTransform,
    c_v: CVelocity,
    c_a: CAnimation,
    delta_time: float,
    lvl_mgr: CPlayLevelManager,
):
    c_st.gravity_vector = c_st.fold_pos - c_tr.pos
    c_st.gravity_vector.scale_to_length(50)
    c_v.vel = c_st.gravity_vector
    dist = c_tr.pos.distance_to(c_st.fold_pos)
    if dist < 1:
        c_tr.pos.x = c_st.fold_pos.x
        c_tr.pos.y = c_st.fold_pos.y
        c_tr.rot_deg = 0
        c_st.gravity_vector.xy = 0, 0
        lvl_mgr.current_attacks -= 1
        set_animation(c_a, "IDLE")
        c_st.state = EnemyStates.IDLE
    elif dist < 50:
        c_tr.rot_deg += delta_time * 180
        if c_tr.rot_deg > 0:
            c_tr.rot_deg = 0
