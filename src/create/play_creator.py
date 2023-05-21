import pygame
import esper
from src.create.prefab_creator import create_sprite, create_square
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_bullet_state import BulletStates, CBulletState
from src.ecs.components.c_enemy_fleet import CEnemyFleet
from src.ecs.components.c_enemy_state import CEnemyState
from src.ecs.components.c_follow_entity import CFollowEntity
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator


def create_player(world: esper.World):
    player_config = ServiceLocator.configs_service.get("assets/cfg/player.json")
    surface = ServiceLocator.images_service.get(player_config["image"])
    pos = pygame.Vector2(
        player_config["spawn_point"]["x"], player_config["spawn_point"]["y"]
    )
    vel = pygame.Vector2(0, 0)
    player_entity = create_sprite(world, pos, vel, surface)
    world.add_component(player_entity, CTagPlayer(player_config["input_speed"]))
    world.add_component(player_entity, CPlayerState(player_config["lives"]))
    player_tr = world.component_for_entity(player_entity, CTransform)
    player_v = world.component_for_entity(player_entity, CVelocity)
    player_tag = world.component_for_entity(player_entity, CTagPlayer)
    player_state = world.component_for_entity(player_entity, CPlayerState)
    return (player_entity, player_tr, player_v, player_tag, player_state)


def create_all_enemies(world: esper.World):
    level_cfg = ServiceLocator.configs_service.get("assets/cfg/level_01.json")
    enemies_cfg = ServiceLocator.configs_service.get("assets/cfg/enemies.json")
    sep_y = 13
    fleet_entity = world.create_entity()
    world.add_component(fleet_entity, CEnemyFleet(1, level_cfg["enemy_speed"]["x"]))

    enemy_a_config = enemies_cfg["enemy_04"]
    enemy_b_config = enemies_cfg["enemy_03"]
    enemy_c_config = enemies_cfg["enemy_02"]
    enemy_d_config = enemies_cfg["enemy_01"]
    global_speed = pygame.Vector2(0, 0)

    start_pos: pygame.Vector2 = pygame.Vector2(94, 39)
    score_value = enemy_a_config["score_value"]
    score_value_after_hit = enemy_a_config["score_value_after_hit"]
    image = enemy_a_config["image"]
    animations = enemy_a_config["animations"]
    for x in range(2):
        for y in range(1):
            pos = pygame.Vector2(start_pos.x + 53 * x, start_pos.y + sep_y * y)
            create_enemy(
                world,
                pos,
                global_speed,
                score_value,
                score_value_after_hit,
                image,
                animations,
            )

    start_pos.x = 77
    start_pos.y = 54
    score_value = enemy_b_config["score_value"]
    score_value_after_hit = enemy_b_config["score_value_after_hit"]
    image = enemy_b_config["image"]
    animations = enemy_b_config["animations"]
    for x in range(6):
        for y in range(1):
            pos = pygame.Vector2(start_pos.x + 18 * x, start_pos.y + sep_y * y)
            create_enemy(
                world,
                pos,
                global_speed,
                score_value,
                score_value_after_hit,
                image,
                animations,
            )

    start_pos.x = 58
    start_pos.y = 66
    score_value = enemy_c_config["score_value"]
    score_value_after_hit = enemy_c_config["score_value_after_hit"]
    image = enemy_c_config["image"]
    animations = enemy_c_config["animations"]
    for x in range(8):
        for y in range(1):
            pos = pygame.Vector2(start_pos.x + 18 * x, start_pos.y + sep_y * y)
            create_enemy(
                world,
                pos,
                global_speed,
                score_value,
                score_value_after_hit,
                image,
                animations,
            )

    start_pos.x = 42
    start_pos.y = 80
    score_value = enemy_d_config["score_value"]
    score_value_after_hit = enemy_d_config["score_value_after_hit"]
    image = enemy_d_config["image"]
    animations = enemy_d_config["animations"]
    for x in range(10):
        for y in range(3):
            pos = pygame.Vector2(start_pos.x + 18 * x, start_pos.y + sep_y * y)
            create_enemy(
                world,
                pos,
                global_speed,
                score_value,
                score_value_after_hit,
                image,
                animations,
            )


def create_enemy(
    world: esper.World,
    pos: pygame.Vector2,
    velocity: pygame.Vector2,
    score_value: float,
    score_value_after_hit: float,
    image_path: str,
    animations: dict,
) -> None:
    image = ServiceLocator.images_service.get(image_path)
    enemy_entity = create_sprite(world, pos, velocity, image)
    world.add_component(enemy_entity, CTagEnemy(score_value, score_value_after_hit))
    world.add_component(enemy_entity, CAnimation(animations))

    enemy_state = CEnemyState()
    enemy_state.fold_pos = pos.copy()
    world.add_component(enemy_entity, enemy_state)


def create_bullet_player(world: esper.World, player_entity: int) -> CBulletState:
    bullet_cfg = ServiceLocator.configs_service.get("assets/cfg/bullets.json")
    player_bullet_cfg = bullet_cfg["player"]
    size = pygame.Vector2(
        player_bullet_cfg["size"]["w"], player_bullet_cfg["size"]["h"]
    )
    vel = pygame.Vector2(0, 0)
    pos = pygame.Vector2(0, 0)
    color = pygame.Color(
        player_bullet_cfg["color"]["r"],
        player_bullet_cfg["color"]["g"],
        player_bullet_cfg["color"]["b"],
    )
    player_bullet_entity = create_square(world, size, pos, vel, color)
    world.add_component(player_bullet_entity, CTransform(pygame.Vector2()))
    world.add_component(
        player_bullet_entity, CFollowEntity(player_entity, pygame.Vector2(7, -2))
    )
    speed = pygame.Vector2(
        player_bullet_cfg["velocity"]["x"], player_bullet_cfg["velocity"]["y"]
    )
    c_bullet_state = CBulletState("player", speed)
    world.add_component(player_bullet_entity, c_bullet_state)
    return c_bullet_state


def create_bullet_enemy(world: esper.World, pos: pygame.Vector2, vel_x: float):
    bullet_cfg = ServiceLocator.configs_service.get("assets/cfg/bullets.json")
    enemy_bullet_cfg = bullet_cfg["enemy"]
    size = pygame.Vector2(enemy_bullet_cfg["size"]["w"], enemy_bullet_cfg["size"]["h"])
    vel = pygame.Vector2(0, 0)
    color = pygame.Color(
        enemy_bullet_cfg["color"]["r"],
        enemy_bullet_cfg["color"]["g"],
        enemy_bullet_cfg["color"]["b"],
    )
    enemy_bullet_entity = create_square(world, size, pos, vel, color)
    speed = pygame.Vector2(
        enemy_bullet_cfg["velocity"]["x"] + vel_x, enemy_bullet_cfg["velocity"]["y"]
    )
    c_bullet_state = CBulletState("enemy", speed)
    c_bullet_state.state = BulletStates.FIRING
    world.add_component(enemy_bullet_entity, c_bullet_state)
    return c_bullet_state


def create_explosion(world: esper.World, pos: pygame.Vector2, explosion_type: str):
    explosion_cfg = ServiceLocator.configs_service.get("assets/cfg/explosions.json")
    explosion_info = explosion_cfg[explosion_type]
    explosion_surface = ServiceLocator.images_service.get(explosion_info["image"])
    vel = pygame.Vector2(0, 0)

    explosion_entity = create_sprite(world, pos, vel, explosion_surface)
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity, CAnimation(explosion_info["animations"]))
    ServiceLocator.sounds_service.play_once(explosion_info["sound"])
    return explosion_entity
