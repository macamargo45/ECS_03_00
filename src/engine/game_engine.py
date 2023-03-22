import json
import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.systems.s_bullets_screen import system_bullets_screen
from src.ecs.systems.s_collision_enemy import system_collision_enemy

from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_input import system_input
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce

from src.ecs.components.c_input import CInputCommand, InputCommandPhase
from src.ecs.components.c_velocity import CVelocity

from src.create.prefab_creator import create_enemy_spawner, create_player, create_player_bullet, create_player_input

class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()
        pygame.display.set_caption(self.window_cfg["title"])
        self.screen = pygame.display.set_mode(
            (self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]), 
            pygame.SCALED)

        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg["framerate"]
        self.delta_time = 0
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                     self.window_cfg["bg_color"]["g"],
                                     self.window_cfg["bg_color"]["b"])
        self.ecs_world = esper.World()

    def _load_config_files(self):
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("assets/cfg/enemies.json") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open("assets/cfg/level_01.json") as level_01_file:
            self.level_01_cfg = json.load(level_01_file)
        with open("assets/cfg/bullets.json") as bullets_file:
            self.bullet_cfg = json.load(bullets_file)

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        # SPAWNER
        create_enemy_spawner(self.ecs_world, self.level_01_cfg)
        
        # PLAYER AND PLAYER VELOCITY COMPONENT
        self.player_entity = create_player(self.ecs_world)
        self.cv_pl = self.ecs_world.component_for_entity(self.player_entity, 
                                                         CVelocity)
        self.tr_pl = self.ecs_world.component_for_entity(self.player_entity, 
                                                         CTransform)
        self.sf_pl = self.ecs_world.component_for_entity(self.player_entity, 
                                                         CSurface)
        # INPUT 
        create_player_input(self.ecs_world)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
    
    def _process_events(self):
        for event in pygame.event.get():
            system_input(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        self.ecs_world._clear_dead_entities()

        system_enemy_spawner(self.ecs_world, self.enemies_cfg, self.delta_time)
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)
        system_collision_enemy(self.ecs_world, self.player_entity)
        system_bullets_screen(self.ecs_world, self.screen)

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, input_command:CInputCommand):
        if input_command.name == "PLAYER_UP":
            if input_command.phase == InputCommandPhase.DOWN:
                self.cv_pl.vel.y -= 100
            elif input_command.phase == InputCommandPhase.UP:
                self.cv_pl.vel.y += 100
        if input_command.name == "PLAYER_DOWN":
            if input_command.phase == InputCommandPhase.DOWN:
                self.cv_pl.vel.y += 100
            elif input_command.phase == InputCommandPhase.UP:
                self.cv_pl.vel.y -= 100
        if input_command.name == "PLAYER_LEFT":
            if input_command.phase == InputCommandPhase.DOWN:
                self.cv_pl.vel.x -= 100
            elif input_command.phase == InputCommandPhase.UP:
                self.cv_pl.vel.x += 100
        if input_command.name == "PLAYER_RIGHT":
            if input_command.phase == InputCommandPhase.DOWN:
                self.cv_pl.vel.x += 100
            elif input_command.phase == InputCommandPhase.UP:
                self.cv_pl.vel.x -= 100

        if input_command.name == "FIRE":
            center = self.sf_pl.surf.get_rect(topleft=self.tr_pl.pos).center
            pos = pygame.Vector2(center[0], center[1])
            create_player_bullet(
                world=self.ecs_world,
                player_pos=pos,
                mouse_pos=input_command.vector,
                bullet_data=self.bullet_cfg["player_bullet"])

    
