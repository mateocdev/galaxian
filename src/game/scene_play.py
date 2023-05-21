import pygame

from src.create import prefab_creator, interface_creator, play_creator, world_creator
from src.ecs.components.c_bullet_state import BulletStates, CBulletState
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_play_level_manager import CPlayLevelManager, PlayLevelState
from src.ecs.systems.play.s_bullet_state import system_bullet_state
from src.ecs.systems.play.s_collision_bullet import system_collision_bullet
from src.ecs.systems.play.s_collision_player import system_collision_player
from src.ecs.systems.play.s_enemy_movement import system_enemy_movement
from src.ecs.systems.play.s_enemy_state import system_enemy_state
from src.ecs.systems.play.s_level_manager import system_level_manager
from src.ecs.systems.s_interface_tracker import system_interface_tracker
from src.ecs.systems.play.s_player_movement import system_player_movement
from src.ecs.systems.play.s_player_state import system_player_state
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.play.s_explosion_kill import system_explosion_kill
from src.ecs.systems.play.s_follow_entity import system_follow_entity
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_starfield import system_starfield
from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.engine.services.globals_service import DebugViewMode


class ScenePlay(Scene):
    def do_create(self):
        # CONFIGURAR ESTADO GLOBAL
        if ServiceLocator.globals_service.from_play:
            ServiceLocator.globals_service.player_score = 0
        ServiceLocator.globals_service.from_play = False
        ServiceLocator.globals_service.current_level = 1

        # ENTIDADES
        world_creator.create_starfield(self.ecs_world)
        (
            self.pl_entity,
            self.pl_tr,
            self.pl_v,
            self.pl_tg,
            self.pl_st,
        ) = play_creator.create_player(self.ecs_world)
        bullet_st = play_creator.create_player_bullet(self.ecs_world, self.pl_entity)

        # INTERFAZ
        interface_creator.create_menu_interface(self.ecs_world, False)
        interface_creator.create_interface_lives(self.ecs_world)
        interface_creator.create_interface_level_counter(self.ecs_world)
        paused_s, paused_blk = interface_creator.create_paused_text(self.ecs_world)
        ready_ent = interface_creator.create_ready_text(self.ecs_world)

        # ESTADO DE ESCENA
        c_lvl_st = self.ecs_world.create_entity()
        self.c_lvl_mgr = CPlayLevelManager(
            bullet_st, paused_s, paused_blk, ready_ent, self.pl_entity
        )
        self.ecs_world.add_component(c_lvl_st, self.c_lvl_mgr)

        # ACCIONES
        prefab_creator.create_action(self.ecs_world, "LEFT", pygame.K_LEFT)
        prefab_creator.create_action(self.ecs_world, "RIGHT", pygame.K_RIGHT)
        prefab_creator.create_action(self.ecs_world, "FIRE_NORMAL", pygame.K_z)
        prefab_creator.create_action(self.ecs_world, "PAUSE", pygame.K_p)
        prefab_creator.create_action(
            self.ecs_world, "SWITCH_DEBUG_MODE", pygame.K_LCTRL
        )

        # MUSIC DE INTRO
        self.level_cfg = ServiceLocator.configs_service.get("assets/cfg/level_01.json")
        ServiceLocator.sounds_service.play_once(self.level_cfg["start_game_sound"])

    def do_update(self, delta_time: float):
        system_level_manager(self.ecs_world, self.c_lvl_mgr, delta_time)
        if self.c_lvl_mgr.state != PlayLevelState.PAUSED:
            system_movement(self.ecs_world, delta_time)
            system_follow_entity(self.ecs_world)
            system_enemy_movement(self.ecs_world, delta_time)
            system_enemy_state(
                self.ecs_world, self.c_lvl_mgr, self.pl_tr, self.pl_st, delta_time
            )
            system_player_movement(self.ecs_world)
            system_bullet_state(
                self.ecs_world, self.pl_entity, self.game_engine.screen.get_rect()
            )
            system_collision_bullet(self.ecs_world, self.c_lvl_mgr)
            system_collision_player(self.ecs_world, self.c_lvl_mgr)
            system_animation(self.ecs_world, delta_time)

        system_starfield(self.ecs_world, delta_time)
        system_player_state(self.ecs_world, self.c_lvl_mgr, delta_time)
        system_explosion_kill(self.ecs_world)
        system_interface_tracker(self.ecs_world)
        system_blink(self.ecs_world, delta_time)

    def do_action(self, action: CInputCommand) -> None:
        if action.name == "LEFT":
            if action.phase == CommandPhase.START:
                self.pl_v.vel.x -= self.pl_tg.input_speed
            else:
                self.pl_v.vel.x += self.pl_tg.input_speed
        if action.name == "RIGHT":
            if action.phase == CommandPhase.START:
                self.pl_v.vel.x += self.pl_tg.input_speed
            else:
                self.pl_v.vel.x -= self.pl_tg.input_speed
        if action.name == "PAUSE" and action.phase == CommandPhase.END:
            if self.c_lvl_mgr.state == PlayLevelState.PLAY:
                self.c_lvl_mgr.state = PlayLevelState.PAUSED
            elif self.c_lvl_mgr.state == PlayLevelState.PAUSED:
                self.c_lvl_mgr.state = PlayLevelState.PLAY
            is_paused = self.c_lvl_mgr.state == PlayLevelState.PAUSED
            self.c_lvl_mgr.paused_s.visible = is_paused
            self.c_lvl_mgr.paused_blk.enabled = is_paused
            if is_paused:
                ServiceLocator.sounds_service.play_once(
                    self.level_cfg["pause_game_sound"]
                )

        if action.name == "FIRE_NORMAL" and action.phase == CommandPhase.START:
            if self.c_lvl_mgr.state == PlayLevelState.GAME_OVER:
                ServiceLocator.globals_service.from_play = True
                self.switch_scene("MENU_SCENE")
            elif self.c_lvl_mgr.state == PlayLevelState.PLAY:
                self._do_fire_normal_action()

        if action.name == "SWITCH_DEBUG_MODE" and action.phase == CommandPhase.START:
            if ServiceLocator.globals_service.debug_view == DebugViewMode.NONE:
                ServiceLocator.globals_service.debug_view = DebugViewMode.RECTS

            elif ServiceLocator.globals_service.debug_view == DebugViewMode.RECTS:
                ServiceLocator.globals_service.debug_view = DebugViewMode.ENEMIES

            elif ServiceLocator.globals_service.debug_view == DebugViewMode.ENEMIES:
                ServiceLocator.globals_service.debug_view = DebugViewMode.NONE

    def _do_fire_normal_action(self):
        self.c_lvl_mgr.bullet_st.state = BulletStates.FIRING
