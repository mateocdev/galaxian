import json
import pygame
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_vertical_card import CVerticalCard
from src.ecs.systems.menu.s_vertical_card_mover import system_vertical_card_mover
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_interface_tracker import system_interface_tracker
from src.ecs.systems.s_movement import system_movement

from src.engine.scenes.scene import Scene
import src.engine.game_engine

from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.systems.s_starfield import system_starfield
from src.create import interface_creator, menu_creator, world_creator
from src.engine.service_locator import ServiceLocator


class SceneMenu(Scene):
    def do_create(self):
        ServiceLocator.globals_service.player_score = 0

        world_creator.create_starfield(self.ecs_world)
        menu_creator.create_press_start_text(self.ecs_world)
        menu_creator.create_title(self.ecs_world)
        interface_creator.create_menu_interface(self.ecs_world, True)

        # CREAR ACCIONES  DE ESCENA
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(
            start_game_action, CInputCommand("START", pygame.K_z)
        )

    def do_action(self, action: CInputCommand) -> None:
        if action.name == "START" and action.phase == CommandPhase.START:
            self._remove_v_cards_or_start_game()

    def do_update(self, delta_time: float):
        system_starfield(self.ecs_world, delta_time)
        system_movement(self.ecs_world, delta_time)
        system_vertical_card_mover(self.ecs_world)
        system_blink(self.ecs_world, delta_time)
        system_interface_tracker(self.ecs_world)

    def _remove_v_cards_or_start_game(self):
        v_cards = self.ecs_world.get_components(CVerticalCard, CTransform)
        if len(v_cards) > 0:
            for _, (c_v, c_tr) in v_cards:
                c_tr.pos.y = c_v.target_end_y
        else:
            self.switch_scene("PLAY_SCENE")
