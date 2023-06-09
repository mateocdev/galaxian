import pygame
import esper

from src.ecs.components.c_input_command import CInputCommand
from src.ecs.systems.s_input import system_input
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_rendering_debug import system_rendering_debug
import src.engine.game_engine
from src.engine.service_locator import ServiceLocator
from src.engine.services.globals_service import DebugViewMode

class Scene:
    def __init__(self, game_engine:'src.engine.game_engine.GameEngine') -> None:
        self.ecs_world = esper.World()
        self.game_engine = game_engine

    def do_process_events(self, event:pygame.event):
        system_input(self.ecs_world, event, self.do_action)

    def simulate(self, delta_time):
        self.do_update(delta_time)
        self.ecs_world._clear_dead_entities()

    def clean(self):
        self.ecs_world.clear_database()
        self.do_clean()
    
    def switch_scene(self, new_scene:str):
        self.game_engine.switch_scene(new_scene)

    def do_create(self):
        pass

    def do_update(self, delta_time:float):
        pass

    def do_draw(self, screen):
        system_rendering(self.ecs_world, screen)
        if ServiceLocator.globals_service.debug_view is not DebugViewMode.NONE:
            system_rendering_debug(self.ecs_world, screen)

    def do_action(self, action:CInputCommand):
        pass
    
    def do_clean(self):
        pass

    

