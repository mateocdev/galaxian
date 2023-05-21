""" import asyncio
import json
import pygame
import esper
from src.ecs.systems.s_animation import system_animation

from src.ecs.systems.play.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.play.s_collision_enemy_bullet import system_collision_enemy_bullet

from src.ecs.systems.play.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.play.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.play.s_rendering import system_rendering
from src.ecs.systems.play.s_screen_bounce import system_screen_bounce
from src.ecs.systems.play.s_screen_player import system_screen_player
from src.ecs.systems.play.s_screen_bullet import system_screen_bullet

from src.ecs.systems.play.s_player_state import system_player_state
from src.ecs.systems.play.s_explosion_kill import system_explosion_kill
from src.ecs.systems.play.s_enemy_hunter_state import system_enemy_hunter_state

from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.c_input_command import CInputCommand
from src.engine.scenes.scene import Scene
from src.game.scene_menu import SceneMenu
from src.game.scene_play import ScenePlay

from src.ecs.components.c_input_command import CInputCommand, CommandPhase

from src.create.prefab_creator import (
    create_enemy_spawner,
    create_input_player,
    create_player_square,
    create_bullet,
    create_text,
) """
import json
import asyncio
import pygame

from src.ecs.components.c_input_command import CInputCommand
from src.engine.scenes.scene import Scene
from src.game.scene_menu import SceneMenu
from src.game.scene_play import ScenePlay


class GameEngine:
    def __init__(self) -> None:
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self._window_cfg = json.load(window_file)

        pygame.init()
        pygame.display.set_caption(self._window_cfg["title"])
        self.screen = pygame.display.set_mode(
            (self._window_cfg["size"]["w"], self._window_cfg["size"]["h"]),
            pygame.SCALED,
        )

        self._clock = pygame.time.Clock()
        self._framerate = self._window_cfg["framerate"]
        self._delta_time = 0
        self._bg_color = pygame.Color(
            self._window_cfg["bg_color"]["r"],
            self._window_cfg["bg_color"]["g"],
            self._window_cfg["bg_color"]["b"],
        )
        self.is_running = False

        self._scenes: dict[str, Scene] = {}
        self._scenes["MENU_SCENE"] = SceneMenu(self)
        self._scenes["PLAY_SCENE"] = ScenePlay(self)
        self._current_scene: Scene = None
        self._scene_name_to_switch: str = None

        """     def _load_config_files(self):
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("assets/cfg/enemies.json") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open("assets/cfg/level_01.json") as level_01_file:
            self.level_01_cfg = json.load(level_01_file)
        with open("assets/cfg/player.json") as player_file:
            self.player_cfg = json.load(player_file)
        with open("assets/cfg/bullet.json") as bullet_file:
            self.bullet_cfg = json.load(bullet_file)
        with open("assets/cfg/explosion.json") as explosion_file:
            self.explosion_cfg = json.load(explosion_file) """

    async def run(self, start_scene_name: str) -> None:
        self._create()
        self.is_running = True
        self._current_scene = self._scenes[start_scene_name]
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            self._handle_switch_scene()
            await asyncio.sleep(0)
        self._do_clean()

    def _create(self):
        """if self.is_started:
            self._player_entity = create_player_square(
                self.ecs_world, self.player_cfg, self.level_01_cfg["player_spawn"]
            )
            self._player_c_v = self.ecs_world.component_for_entity(
                self._player_entity, CVelocity
            )
            self._player_c_t = self.ecs_world.component_for_entity(
                self._player_entity, CTransform
            )
            self._player_c_s = self.ecs_world.component_for_entity(
                self._player_entity, CSurface
            )

            create_enemy_spawner(self.ecs_world, self.level_01_cfg)
            create_input_player(self.ecs_world)
        create_text(
            self.ecs_world,
            "Controles: Flechas, click normal, click derecho con balas en el mundo.",
            pygame.Vector2(5, 25),
            pygame.Color(255, 255, 255),
            6,
        )
        create_text(
            self.ecs_world,
            "Ejercicio 04",
            pygame.Vector2(
                self.screen.get_rect().centerx - 70, self.screen.get_rect().top + 2
            ),
            pygame.Color(255, 0, 0),
            12,
        )"""
        self._current_scene.do_create()

    def switch_scren(self, new_scene_name: str):
        self._scene_name_to_switch = new_scene_name

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
        if self.delta_time > 0.05:
            self.delta_time = 0.05

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        self._current_scene.simulate(self.delta_time)
        """         system_enemy_spawner(self.ecs_world, self.enemies_cfg, self.delta_time)
        system_movement(self.ecs_world, self.delta_time)

        system_screen_bounce(self.ecs_world, self.screen)
        system_screen_player(self.ecs_world, self.screen)
        system_screen_bullet(self.ecs_world, self.screen)

        system_collision_enemy_bullet(self.ecs_world, self.explosion_cfg)
        system_collision_player_enemy(
            self.ecs_world, self._player_entity, self.level_01_cfg, self.explosion_cfg
        )

        system_explosion_kill(self.ecs_world)

        system_player_state(self.ecs_world)
        system_enemy_hunter_state(
            self.ecs_world, self._player_entity, self.enemies_cfg["TypeA"]
        )
        system_enemy_hunter_state(
            self.ecs_world, self._player_entity, self.enemies_cfg["TypeB"]
        )
        system_enemy_hunter_state(
            self.ecs_world, self._player_entity, self.enemies_cfg["TypeC"]
        )
        system_enemy_hunter_state(
            self.ecs_world, self._player_entity, self.enemies_cfg["TypeD"]
        )

        system_animation(self.ecs_world, self.delta_time)

        self.ecs_world._clear_dead_entities()
        self.num_bullets = len(self.ecs_world.get_component(CTagBullet)) """

    def _draw(self):
        self.screen.fill(self.bg_color)
        self._current_scene.do_draw(self.screen)
        """system_rendering(self.ecs_world, self.screen)"""
        pygame.display.flip()

    def _do_clean(self):
        if self._current_scene is not None:
            self._current_scene.do_clean()
        """ self.ecs_world.clear_database() """
        pygame.quit()

    def _handle_switch_scene(self):
        if self._scene_name_to_switch is not None:
            self._current_scene.clean()
            self._current_scene = self._scenes[self._scene_name_to_switch]
            self._current_scene.do_create()
            self._scene_name_to_switch = None

    def _do_action(self, c_input: CInputCommand):
        self._current_scene.do_action(c_input)
        """         if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.x -= self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.x += self.player_cfg["input_velocity"]
        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.x += self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.x -= self.player_cfg["input_velocity"]

        if (
            c_input.name == "PLAYER_FIRE"
            and self.num_bullets < self.level_01_cfg["player_spawn"]["max_bullets"]
        ):
            if not self.is_paused:
                create_bullet(
                    self.ecs_world,
                    c_input.mouse_pos,
                    self._player_c_t.pos,
                    self._player_c_s.area.size,
                    self.bullet_cfg,
                )

        if c_input.name == "PLAYER_PAUSE" and c_input.phase == CommandPhase.START:
            self.is_paused = not self.is_paused
            if self.is_paused:
                self._pause_entity = create_text(
                    self.ecs_world,
                    "Pausado",
                    pygame.Vector2(5, 5),
                    pygame.Color(0, 255, 0),
                    10,
                )
            elif self._pause_entity:
                self.ecs_world.delete_entity(self._pause_entity) """
