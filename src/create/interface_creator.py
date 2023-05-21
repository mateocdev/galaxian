from enum import Enum
import pygame
import esper


from src.create.prefab_creator import TextAlignment, create_sprite, create_text
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_vertical_card import CVerticalCard
from src.ecs.components.tags.c_tag_level_counter import CTagLevelCounter
from src.ecs.components.tags.c_tag_life import CTagLife
from src.ecs.components.tags.c_tag_score import CTagScore
from src.engine.service_locator import ServiceLocator


def create_menu_interface(world: esper.World, use_prefab: bool) -> None:
    interface_config = ServiceLocator.config_services.get("assets/cfg/interface.json")
    v_card_cfg = interface_config["vertical_card"]
    title_text_color = pygame.color.Color(
        interface_config["title_text_color"]["r"],
        interface_config["title_text_color"]["g"],
        interface_config["title_text_color"]["b"],
    )
    title_text_size = interface_config["title_text_size"]

    lives_txt = create_text(
        world,
        "LIVES",
        title_text_size,
        title_text_color,
        pygame.Vector2(40, 20),
        TextAlignment.LEFT,
        False,
    )
    high_score_txt = create_text(
        world,
        "HIGH SCORE",
        title_text_size,
        title_text_color,
        pygame.Vector2(80, 18),
        TextAlignment.LEFT,
        False,
    )

    if use_prefab:
        add_v_card_component(
            world,
            lives_txt,
            title_text_size,
            v_card_cfg["v_speed"],
            v_card_cfg["v_offset"],
        )
        add_v_card_component(
            world,
            high_score_txt,
            title_text_size,
            v_card_cfg["v_speed"],
            v_card_cfg["v_offset"],
        )


def create_interface_live(world: esper.World):
    player_config = ServiceLocator.config_services.get("assets/cfg/player.json")
    lives = player_config["lives"]
    interface_config = ServiceLocator.config_services.get("assets/cfg/interface.json")
    interface_lives_config = interface_config["lives"]
    lives_surface = ServiceLocator.images_services.get(interface_lives_config["image"])
    for i in range(lives):
        pos = pygame.Vector2(
            interface_lives_config["pos"]["x"] + i * interface_lives_config["pos"]["y"]
        )
        pos.x += i * lives_surface.get_rect().w
        vel = pygame.Vector2(0, 0)
        live_entity = create_sprite(world, pos, vel, lives_surface)
        world.add_component(live_entity, CTagLife())


def create_interface_counter_level(world: esper.World):
    interface_config = ServiceLocator.config_services.get("assets/cfg/interface.json")
    text_counter_color = pygame.color.Color(
        interface_config["normal_text_color"]["r"],
        interface_config["normal_text_color"]["g"],
        interface_config["normal_text_color"]["b"],
    )
    flag_surface = ServiceLocator.images_services.get(
        interface_config["level_flag"]["image"]
    )
    flag_pos = pygame.Vector2(
        interface_config["level_flag"]["pos"]["x"],
        interface_config["level_flag"]["pos"]["y"],
    )
    flag_vel = pygame.Vector2(0, 0)
    create_sprite(world, flag_pos, flag_vel, flag_surface)
    flag_txt_pos = pygame.Vector2(
        interface_config["level_flag"]["pos"]["x"],
        interface_config["level_flag"]["pos"]["y"],
    )
    flag_txt_pos.x += 30
    flag_txt_pos.y += 5
    level_text = create_text(
        world, "1", 10, text_counter_color, flag_txt_pos, TextAlignment.RIGHT, True
    )
    world.add_component(level_text, CTagLevelCounter())


def add_v_card_component(
    world: esper.World, entity: int, pos_y: float, speed: int, offset: int
):
    world.add_component(entity, CVerticalCard(speed, offset + pos_y, pos_y))
    world.add_component(entity, CVelocity(pygame.Vector2(0, 0)))


def create_pause_text(world: esper.World) -> tuple[CSurface, CBlink]:
    interface_config = ServiceLocator.config_services.get("assets/cfg/interface.json")
    color = pygame.Color(
        interface_config["title_text_color"]["r"],
        interface_config["title_text_color"]["g"],
        interface_config["title_text_color"]["b"],
    )
    pos = pygame.Vector2(
        interface_config["pause_text"]["pos"]["x"],
        interface_config["pause_text"]["pos"]["y"],
    )
    size = interface_config["pause_text"]["size"]
    get_text = interface_config["pause_text"]["text"]
    text = create_text(world, get_text, size, color, pos, TextAlignment.CENTER, False)
    paused = world.component_for_entity(text, CSurface)
    blink = CBlink(interface_config["interface_blink_rate"])
    world.add_component(paused, blink)
    paused.visible = False
    blink.visible = False
    return paused, blink


def create_win_text(world: esper.World) -> tuple[CSurface, CBlink]:
    interface_config = ServiceLocator.config_services.get("assets/cfg/interface.json")
    color = pygame.Color(
        interface_config["normal_text_color"]["r"],
        interface_config["normal_text_color"]["g"],
        interface_config["normal_text_color"]["b"],
    )
    pos = pygame.Vector2(
        interface_config["win_text"]["pos"]["x"],
        interface_config["win_text"]["pos"]["y"],
    )
    size = interface_config["win_text"]["size"]
    get_text = interface_config["win_text"]["text"]
    text = create_text(world, get_text, size, color, pos, TextAlignment.CENTER, False)
    win = world.component_for_entity(text, CSurface)
    color = pygame.Color(
        interface_config["title_text_color"]["r"],
        interface_config["title_text_color"]["g"],
        interface_config["title_text_color"]["b"],
    )
    pos = pygame.Vector2(
        interface_config["win_text"]["pos"]["x"],
        interface_config["win_text"]["pos"]["y"],
    )
    size = interface_config["next_level"]["size"]
    get_text = interface_config["next_level"]["text"]
    text_2 = create_text(world, get_text, size, color, pos, TextAlignment.CENTER, False)
    return win, text_2


def create_game_start_text(world: esper.World) -> int:
    interface_config = ServiceLocator.config_services.get("assets/cfg/interface.json")
    color = pygame.Color(
        interface_config["normal_text_color"]["r"],
        interface_config["normal_text_color"]["g"],
        interface_config["normal_text_color"]["b"],
    )
    pos = pygame.Vector2(
        interface_config["game_start"]["pos"]["x"],
        interface_config["game_start"]["pos"]["y"],
    )
    size = interface_config["game_start"]["size"]
    get_text = interface_config["game_start"]["text"]
    text = create_text(world, get_text, size, color, pos, TextAlignment.CENTER, False)
    return text


def create_game_over(world: esper.World):
    interface_config = ServiceLocator.config_services.get("assets/cfg/interface.json")
    color = pygame.Color(
        interface_config["normal_text_color"]["r"],
        interface_config["normal_text_color"]["g"],
        interface_config["normal_text_color"]["b"],
    )
    pos = pygame.Vector2(
        interface_config["game_over"]["pos"]["x"],
        interface_config["game_over"]["pos"]["y"],
    )
    size = interface_config["game_over"]["size"]
    get_text = interface_config["game_over"]["text"]
    text = create_text(world, get_text, size, color, pos, TextAlignment.CENTER, False)
