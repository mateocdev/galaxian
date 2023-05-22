import random
import pygame
import esper

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState
from src.engine.service_locator import ServiceLocator
from src.ecs.components.c_changing_text import CChangingText, TextAlignment


def create_square(
    world: esper.World,
    size: pygame.Vector2,
    pos: pygame.Vector2,
    vel: pygame.Vector2,
    col: pygame.Color,
) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity, CSurface(size, col))
    world.add_component(cuad_entity, CTransform(pos))
    world.add_component(cuad_entity, CVelocity(vel))
    return cuad_entity


def create_sprite(
    world: esper.World,
    pos: pygame.Vector2,
    vel: pygame.Vector2,
    surface: pygame.Surface,
) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, CTransform(pos))
    world.add_component(sprite_entity, CVelocity(vel))
    world.add_component(sprite_entity, CSurface.from_surface(surface))
    return sprite_entity


def create_text(
    world: esper.World,
    txt: str,
    size: int,
    color: pygame.Color,
    pos: pygame.Vector2,
    alignment: TextAlignment,
    text_changes: bool,
) -> int:
    font = ServiceLocator.fonts_service.get("./assets/fnt/PressStart2P.ttf", size)
    text_entity = world.create_entity()
    world.add_component(text_entity, CSurface.from_text(txt, font, color))
    txt_s = world.component_for_entity(text_entity, CSurface)
    origin = pygame.Vector2(0, 0)
    if alignment is TextAlignment.RIGHT:
        origin.x -= txt_s.area.right
    elif alignment is TextAlignment.CENTER:
        origin.x -= txt_s.area.centerx
    world.add_component(text_entity, CTransform(pos + origin))
    if text_changes:
        world.add_component(text_entity, CChangingText(txt, font, alignment))
    return text_entity


def create_action(world: esper.World, name: str, key: int):
    action_entity = world.create_entity()
    world.add_component(action_entity, CInputCommand(name, key))
