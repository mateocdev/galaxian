import esper
import pygame
from src.create.prefab_creator import TextAlignment

from src.ecs.components.c_changing_text import CChangingText
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface


def system_rendering(world: esper.World, screen: pygame.Surface):
    components = world.get_components(
        CTransform,
        CSurface)
    for _, (c_t, c_s) in components:
        if not c_s.visible:
            continue

        if world.has_component(_, CChangingText):
            c_c_t = world.component_for_entity(_, CChangingText)
            if c_c_t.alignment is TextAlignment.RIGHT:
                c_t.pos.x += c_s.area.right
            elif c_c_t.alignment is TextAlignment.CENTER:
                c_s.pos.x += c_s.area.centerx

            c_s.surf = c_c_t.font.render(c_c_t.text, True, c_s.color)
            c_s.area = c_s.surf.get_rect()

            if c_c_t.alignment is TextAlignment.RIGHT:
                c_t.pos.x -= c_s.area.right
            elif c_c_t.alignment is TextAlignment.CENTER:
                c_s.pos.x -= c_s.area.centerx

            if c_t.rot_deg != 0:
                final_surf = c_s.surf.subsurface(c_s.area)
                final_surf = pygame.transform.rotate(final_surf, c_t.rot_deg)
                final_rect = final_surf.get_rect(center=c_s.area.center)
                final_rect.topleft = c_t.pos
                screen.blit(final_surf, final_rect)
            else:
                screen.blit(c_s.surf, c_t.pos, area=c_s.area)
                r = c_s.area.copy()
                r.topleft = c_t.pos
