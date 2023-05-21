import pygame
import esper

from src.ecs.components.c_bullet_state import BulletStates, CBulletState
from src.ecs.components.c_follow_entity import CFollowEntity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator


def system_bullet_state(
    world: esper.World, player_entity: int, screen_rect: pygame.Rect
):
    bullet_config = ServiceLocator.configs_service.get("assets/cfg/bullets.json")
    query = world.get_components(
        CBulletState, CTransform, CVelocity, CSurface, CFollowEntity
    )
    for _, (bullet_state, transform, velocity, surface, follow_entity) in query:
        bullet_rect = surface.area.copy()
        bullet_rect.topleft = transform.pos.copy()
        if bullet_state.state == BulletStates.FIRING:
            if velocity.vel.xy == (0, 0) and bullet_state.tag == "player":
                ServiceLocator.sounds_service.play_once(
                    bullet_config[bullet_state.tag]["sound"]
                )

            if world.has_component(_, CFollowEntity):
                world.remove_component(_, CFollowEntity)

            velocity.vel = bullet_state.velocity.copy()
            if not screen_rect.contains(bullet_rect):
                if bullet_state.tag == "enemy":
                    world.delete_entity(_)
                else:
                    bullet_state.state = BulletStates.IDLE
        elif bullet_state.state == BulletStates.IDLE:
            velocity.vel.xy = (0, 0)
            world.add_component(_, CFollowEntity(player_entity, pygame.Vector2(7, -2)))
