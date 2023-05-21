import pygame
import esper

from src.ecs.components.c_bullet_state import BulletStates, CBulletState
from src.ecs.components.c_follow_entity import CFollowEntity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator


def system_bullet_state(world: esper.World,
                        player_entity: int,
                        screen_rect: pygame.Rect
                        ):
    bullet_config = ServiceLocator.configs_service.get(
        "assets/cfg/bullets.json")
    query = world.get_components(
        CBulletState, CTransform, CVelocity, CSurface, CFollowEntity)
    for _, (bullet_state, transform, velocity, surface, follow_entity) in query:
        bullet_rect = surface.area.copy()
        bullet_rect.topleft = transform.pos.copy()
        if bullet_state.state == BulletStates.FIRING:
            if velocity.vel.xy == (0, 0) and follow_entity.tag == "player":
                ServiceLocator.sounds_services.play_once(
                    bullet_config[follow_entity.tag]["sound"])

            if world.has_component(_, CFollowEntity):
                world.remove_component(_, CFollowEntity)

            velocity.vel = follow_entity.velocity.copy()
            if not screen_rect.contains(bullet_rect):
                if follow_entity.tag == "enemy":
                    world.delete_entity(_)
                else:
                    follow_entity.state = BulletStates.IDLE
        elif follow_entity.state == BulletStates.IDLE:
            velocity.vel.xy = (0, 0)
            world.add_component(_, CFollowEntity(
                player_entity, pygame.Vector2(7, -2)))
