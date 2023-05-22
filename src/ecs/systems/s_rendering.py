import esper
import pygame
from src.create.prefab_creator import TextAlignment

from src.ecs.components.c_changing_text import CChangingText
from src.ecs.components.c_enemy_state import CEnemyState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.engine.service_locator import ServiceLocator


def system_rendering(world: esper.World, screen: pygame.Surface):
    components = world.get_components(CTransform, CSurface)
    for ent, (c_t, c_s) in components:
        if not c_s.visible:
            continue
        if world.has_component(ent, CChangingText):
            c_txt = world.component_for_entity(ent, CChangingText)
            if c_txt.alignment is TextAlignment.RIGHT:
                c_t.pos.x += c_s.area.right
            elif c_txt.alignment is TextAlignment.CENTER:
                c_s.pos.x += c_s.area.centerx

            c_s.surf = c_txt.font.render(c_txt.text, True, c_s.color)
            c_s.area = c_s.surf.get_rect()

            if c_txt.alignment is TextAlignment.RIGHT:
                c_t.pos.x -= c_s.area.right
            elif c_txt.alignment is TextAlignment.CENTER:
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
