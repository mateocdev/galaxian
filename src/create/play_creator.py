import pygame
import esper
from src.create.general_creator import create_sprite, create_square
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
    player_config = ServiceLocator.config_services.get("assets/cfg/player.json")
    surface = ServiceLocator.images_services.get(player_config["image"])
    pos = pygame.Vector2(
        player_config["spawn_point"]["x"], player_config["spawn_point"]["y"]
    )
    vel = pygame.Vector2(0, 0)
    player = create_sprite(world, pos, vel, surface)
    world.add_component(player, CTagPlayer(player_config["input_speed"]))
    world.add_component(player, CPlayerState(player_config["lives"]))
    player_tr = world.component_for_entity(player, CTransform)
    player_v = world.component_for_entity(player, CVelocity)
    player_tag = world.component_for_entity(player, CTagPlayer)
    player_state = world.component_for_entity(player, CPlayerState)
    return player, player_tr, player_v, player_tag, player_state


def create_all_enemies(world: esper.World):
    enemies_config = ServiceLocator.config_services.get("assets/cfg/enemies.json")
    level_config = ServiceLocator.config_services.get("assets/cfg/level_01.json")
    fleet_entity = world.create_entity()
    world.add_component(fleet_entity, CEnemyFleet(1, level_config["enemy_speed"]["x"]))
    enemy_04_config = enemies_config["enemy_04"]
    enemy_03_config = enemies_config["enemy_03"]
    enemy_02_config = enemies_config["enemy_02"]
    enemy_01_config = enemies_config["enemy_01"]
    global_speed = pygame.Vector(0, 0)

    start_pos = pygame.Vector2(
        enemy_04_config["spawn_point"]["x"], enemy_04_config["spawn_point"]["y"]
    )
    score_value = enemy_04_config["score_value"]
    score_value_attack = enemy_04_config["score_value_attack"]
    image = enemy_04_config["image"]
    animations = enemy_04_config["animations"]
    for x in range(2):
        for y in range(1):
            pos = pygame.Vector2(start_pos.x + x * 100, start_pos.y + y * 100)
            create_enemy(
                world,
                pos,
                global_speed,
                score_value,
                score_value_attack,
                image,
                animations,
            )

    start_pos.x = 80
    start_pos.y = 60
    score_value = enemy_03_config["score_value"]
    score_value_attack = enemy_03_config["score_value_attack"]
    image = enemy_03_config["image"]
    animations = enemy_03_config["animations"]
    for x in range(6):
        for y in range(2):
            pos = pygame.Vector2(start_pos.x + x * 100, start_pos.y + y * 100)
            create_enemy(
                world,
                pos,
                global_speed,
                score_value,
                score_value_attack,
                image,
                animations,
            )

    start_pos.x = 60
    start_pos.y = 70
    score_value = enemy_02_config["score_value"]
    score_value_attack = enemy_02_config["score_value_attack"]
    image = enemy_02_config["image"]
    animations = enemy_02_config["animations"]
    for x in range(10):
        for y in range(3):
            pos = pygame.Vector2(start_pos.x + x * 100, start_pos.y + y * 100)
            create_enemy(
                world,
                pos,
                global_speed,
                score_value,
                score_value_attack,
                image,
                animations,
            )

    start_pos.x = 40
    start_pos.y = 80
    score_value = enemy_01_config["score_value"]
    score_value_attack = enemy_01_config["score_value_attack"]
    image = enemy_01_config["image"]
    animations = enemy_01_config["animations"]
    for x in range(14):
        for y in range(4):
            pos = pygame.Vector2(start_pos.x + x * 100, start_pos.y + y * 100)
            create_enemy(
                world,
                pos,
                global_speed,
                score_value,
                score_value_attack,
                image,
                animations,
            )


def create_enemy(
    world: esper.World,
    pos: pygame.Vector2,
    velocity: pygame.Vector2,
    score_value: float,
    score_value_attack: float,
    image_path: str,
    animations: dict,
) -> None:
    image = ServiceLocator.images_services.get(image_path)
    enemy = create_sprite(world, pos, velocity, image)
    world.add_component(enemy, CTagEnemy(score_value, score_value_attack))
    world.add_component(enemy, CAnimation(animations))
    enemy_state = CEnemyState()
    enemy_state.fold_pos = pos.copy()
    world.add_component(enemy, enemy_state)


def create_bullet_player(world: esper.World, player: int) -> CBulletState:
    bullet_config = ServiceLocator.config_services.get("assets/cfg/bullets.json")
    player_bullet_config = bullet_config["player_bullet"]
    size = pygame.Vector2(
        player_bullet_config["size"]["x"], player_bullet_config["size"]["y"]
    )
    vel = pygame.Vector2(0, 0)
    pos = pygame.Vector2(0, 0)
    color = pygame.Color(
        player_bullet_config["color"]["r"],
        player_bullet_config["color"]["g"],
        player_bullet_config["color"]["b"],
    )
    bullet = create_square(world, pos, vel, size, color)
    world.add_component(bullet, CTransform(pygame.Vector2(0, 0)))
    world.add_component(bullet, CFollowEntity(player, pygame.Vector2(0, -1)))
    speed = pygame.Vector2(
        player_bullet_config["speed"]["x"], player_bullet_config["speed"]["y"]
    )
    bullet_state = CBulletState("player", speed)
    world.add_component(bullet, bullet_state)
    return bullet_state


def create_explosion(world: esper.World, pos: pygame.Vector2, explosion_type: str):
    explosion_config = ServiceLocator.config_services.get("assets/cfg/explosions.json")
    explosion_info = explosion_config[explosion_type]
    explosion_surface = ServiceLocator.images_services.get(explosion_info["image"])
    vel = pygame.Vector2(0, 0)

    explosion = create_sprite(world, pos, vel, explosion_surface)
    world.add_component(explosion, CTagExplosion())
    world.add_component(explosion, CAnimation(explosion_info["animations"]))
    ServiceLocator.audio_services.play_sound(explosion_info["sound"])
    return explosion


def create_bullet_enemy(world: esper.World, pos: pygame.Vector2, vel_x: float):
    bullet_config = ServiceLocator.config_services.get("assets/cfg/bullets.json")
    enemy_bullet_config = bullet_config["enemy_bullet"]
    size = pygame.Vector2(
        enemy_bullet_config["size"]["w"], enemy_bullet_config["size"]["h"]
    )
    vel = pygame.Vector2(0, 0)
    color = pygame.Color(
        enemy_bullet_config["color"]["r"],
        enemy_bullet_config["color"]["g"],
        enemy_bullet_config["color"]["b"],
    )
    bullet = create_square(world, pos, vel, size, color)
    speed = pygame.Vector2(
        enemy_bullet_config["velocity"]["x"] + vel_x,
        enemy_bullet_config["velocity"]["y"],
    )
    bullet_s = CBulletState("enemy", speed)
    bullet_s.state = BulletStates.FIRING
    world.add_component(bullet, bullet_s)
    return bullet_s
