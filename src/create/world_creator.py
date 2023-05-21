import random
import pygame
import esper

from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_star import CTagStar
from src.engine.service_locator import ServiceLocator

def create_starfield(ecs: esper.World) -> None:
    starfield_cfg = ServiceLocator.configs_service.get("assets/cfg/starfield.json")
    number_of_stars = starfield_cfg["number_of_stars"]
    speed_range = (starfield_cfg["vertical_speed"]["min"], starfield_cfg["vertical_speed"]["max"])
    blink_rate_range = (starfield_cfg["blink_rate"]["min"], starfield_cfg["blink_rate"]["max"])
    star_colors = starfield_cfg["star_colors"]

    for _ in range(number_of_stars):
        star_entity = ecs.create_entity()

        size = pygame.Vector2(1, 1)
        color_choice = random.choice(star_colors)
        color = pygame.color.Color(color_choice["r"], color_choice["g"], color_choice["b"])

        pos = pygame.Vector2(random.randint(10, 246), random.randint(10, 230))
        vertical_speed = random.randint(speed_range[0], speed_range[1])
        vel = pygame.Vector2(0, vertical_speed)

        blink_rate = random.uniform(blink_rate_range[0], blink_rate_range[1])
        current_blink_rate = random.uniform(blink_rate_range[0], blink_rate_range[1])
        ecs.add_component(star_entity, CSurface(size, color))
        ecs.add_component(star_entity, CTransform(pos))
        ecs.add_component(star_entity, CVelocity(vel))
        ecs.add_component(star_entity, CBlink(blink_rate, current_blink_rate))
        ecs.add_component(star_entity, CTagStar())