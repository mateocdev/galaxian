import pygame
import esper

from src.create.prefab_creator import TextAlignment, create_sprite
from src.create.interface_creator import add_v_card_component, create_text

from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator


def create_press_start_text(world: esper.World) -> None:
    interface_cfg = ServiceLocator.configs_service.get("assets/cfg/interface.json")
    v_card_cfg = interface_cfg["vertical_card"]

    title_text_color = pygame.color.Color(
        interface_cfg["title_text_color"]["r"],
        interface_cfg["title_text_color"]["g"],
        interface_cfg["title_text_color"]["b"],
    )
    pos = pygame.Vector2(128, 160)
    press_start_entity = create_text(
        world, "PRESS Z TO START", 8, title_text_color, pos, TextAlignment.CENTER, False
    )
    blink_rate = interface_cfg["interface_blink_rate"]
    world.add_component(press_start_entity, CBlink(blink_rate))
    world.add_component(press_start_entity, CVelocity(pygame.Vector2(0, 0)))
    add_v_card_component(
        world, press_start_entity, pos.y, v_card_cfg["v_speed"], v_card_cfg["v_offset"]
    )


def create_title(world: esper.World):
    interface_cfg = ServiceLocator.configs_service.get("assets/cfg/interface.json")
    logo_cfg = interface_cfg["logo"]
    v_card_cfg = interface_cfg["vertical_card"]

    image = ServiceLocator.images_service.get(logo_cfg["image"])
    vel = pygame.Vector2(0, 0)
    pos = pygame.Vector2(
        logo_cfg["pos"]["x"] - (image.get_width() / 2), logo_cfg["pos"]["y"]
    )

    logo_entity = create_sprite(world, pos, vel, image)
    add_v_card_component(
        world, logo_entity, pos.y, v_card_cfg["v_speed"], v_card_cfg["v_offset"]
    )
