from typing import Callable
import pygame
import esper

from src.ecs.components.c_input import CInputCommand, InputCommandPhase

def system_input(world:esper.World, event:pygame.event.Event, 
                 do_action:Callable[[CInputCommand], None]):
    components = world.get_component(CInputCommand)
    c_input:CInputCommand
    for _, c_input in components:
        if event.type == pygame.KEYDOWN \
            and event.key == c_input.key_event:
            c_input.phase = InputCommandPhase.DOWN
            do_action(c_input)
        elif event.type == pygame.KEYUP \
            and event.key == c_input.key_event:
            c_input.phase = InputCommandPhase.UP
            do_action(c_input)
        # MOUSE BUTTON
        if event.type == pygame.MOUSEBUTTONDOWN \
            and event.button  == c_input.key_event:
            c_input.vector.xy = pygame.mouse.get_pos()
            do_action(c_input)

