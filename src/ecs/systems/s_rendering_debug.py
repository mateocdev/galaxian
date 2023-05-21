import esper
import pygame
from src.create.general_creator import TextAlignment

from src.ecs.components.c_changing_text import CChangingText
from src.ecs.components.c_enemy_state import CEnemyState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator
from src.engine.services.globals_service import DebugViewMode


def system_rendering_debug(world: esper.World, screen: pygame.Surface):
    components = world.get_components(CTransform, CSurface)
    for _, (c_t, c_s) in components:
        if not c_s.visible:
            continue

        if ServiceLocator.globals_service.debug_view is DebugViewMode.RECTS:
            if c_t.rot_deg != 0:
                final_surface = c_s.surf.subsurface(c_s.area)
                final_surface = pygame.transform.rotate(final_surface, c_t.rot_deg)
                final_rect = final_surface.get_rect(center=c_s.area.center)
                final_rect.topleft = c_t
            else:
                final_rect = c_s.area.move(c_t.pos.x, c_t.pos.y)
                final_rect.topleft = c_t.pos
            pygame.draw.rect(screen, pygame.Color(255, 255, 0), final_rect, 1, 1)

        if ServiceLocator.globals_service.debug_view is DebugViewMode.ENEMIES:
            c_e_st = world.try_component(_, CEnemyState)
            if c_e_st is not None:
                c_e_v = world.component_for_entity(_, CVelocity)
                pygame.draw.line(
                    screen,
                    pygame.Color(0, 255, 0),
                    c_t.pos,
                    (c_t.pos + c_e_st.follow_vector),
                ),
                pygame.draw.line(
                    screen, pygame.Color(255, 255, 255), c_t.pos, (c_t.pos + c_e_v.vel)
                )
                pygame.draw.line(
                    screen,
                    pygame.Color(0, 255, 255),
                    c_t.pos,
                    (c_t.pos + c_e_st.gravity_vector),
                )
