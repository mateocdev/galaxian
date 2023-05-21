import random
import pygame
import esper

from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_star import CTagStar
from src.engine.service_locator import ServiceLocator


def create_starfield(world: esper.World) -> None:
    starfield_config = ServiceLocator.config_services.get("assets/cfg/starfield.json")
    number_of_stars = starfield_config["number_of_stars"]
    speed = (
        starfield_config["vertical_speed"]["min"],
        starfield_config["vertical_speed"]["max"],
    )
    blink = (
        starfield_config["blink_rate"]["min"],
        starfield_config["blink_rate"]["max"],
    )
    star_colors = starfield_config["star_colors"]

    for _ in range(number_of_stars):
        star_entity = world.create_entity()
        size = pygame.Vector2(random.randint(1, 3), random.randint(1, 3))
        color_choice = random.randint(0, len(star_colors) - 1)
        color = pygame.Color(
            star_colors[color_choice]["r"],
            star_colors[color_choice]["g"],
            star_colors[color_choice]["b"],
        )
        pos = pygame.Vector2(random.randint(10, 246), random.randint(10, 230))
        vel = pygame.Vector2(0, random.randint(speed[0], speed[1]))
        blink_rate = random.uniform(blink[0], blink[1])
        current_blink_rate = random.uniform(blink[0], blink[1])
        world.add_component(star_entity, CTagStar())
        world.add_component(star_entity, CTransform(pos))
        world.add_component(star_entity, CVelocity(vel))
        world.add_component(star_entity, CSurface(size, color))
        world.add_component(star_entity, CBlink(blink_rate, current_blink_rate))
