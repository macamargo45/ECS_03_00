from enum import Enum

import pygame

class InputCommandPhase(Enum):
    NA = 0
    DOWN = 1
    UP = 2


class CInputCommand:
    def __init__(self, name:str, key_event:int) -> None:
        self.name = name
        self.key_event = key_event
        self.phase  = InputCommandPhase.NA
        self.vector = pygame.Vector2(0, 0)