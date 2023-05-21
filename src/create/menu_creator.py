import pygame
import esper

from src.create.prefab_creator import TextAlignment, create_sprite
from src.create.interface_creator import add_v_card_component, create_text

from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator


def create_press_start_text(world: esper.World) -> None:
    interface_config = ServiceLocator.config_services.get("assets/cfg/interface.json")
    v_card_config = interface_config["vertical_card"]
    color = pygame.Color(
        interface_config["title_text_color"]["r"],
        interface_config["title_text_color"]["g"],
        interface_config["title_text_color"]["b"],
    )
    pos = pygame.Vector2(
        interface_config["press_start"]["pos"]["x"],
        interface_config["press_start"]["pos"]["y"],
    )
    size = interface_config["press_start"]["size"]
    get_text = interface_config["press_start"]["text"]
    text = create_text(world, get_text, size, color, pos, TextAlignment.CENTER, False)
    world.add_component(text, CBlink(interface_config["interface_blink_rate"]))
    world.add_component(text, CVelocity(pygame.Vector2(0, 0)))
    add_v_card_component(
        world,
        text,
        pos.y,
        v_card_config["v_speed"],
        v_card_config["v_offset"],
    )


def create_title(world: esper.World):
    interface_config = ServiceLocator.config_services.get("assets/cfg/interface.json")
    logo_config = interface_config["logo"]
    v_card_config = interface_config["vertical_card"]
    image = ServiceLocator.images_service.get(logo_config["image"])
    pos = pygame.Vector2(
        logo_config["pos"]["x"] - (image.get_width() / 2), logo_config["pos"]["y"]
    )
    vel = pygame.Vector2(0, 0)
    logo = create_sprite(world, pos, vel, image)
    add_v_card_component(
        world,
        logo,
        pos.y,
        v_card_config["v_speed"],
        v_card_config["v_offset"],
    )
