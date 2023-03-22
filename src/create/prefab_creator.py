import random
import pygame
import esper

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet

from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer

## MODIFICADO PARA PRÁCTICA 2
def create_square(world:esper.World, size:pygame.Vector2,
                    pos:pygame.Vector2, vel:pygame.Vector2, col:pygame.Color) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity,
                CSurface(size, col))
    world.add_component(cuad_entity,
                CTransform(pos))
    world.add_component(cuad_entity, 
                CVelocity(vel))
    return cuad_entity

## MODIFICADO PARA PRÁCTICA 2
def create_enemy(world:esper.World, pos:pygame.Vector2, enemy_info:dict) -> int:
    size = pygame.Vector2(enemy_info["size"]["x"], 
                          enemy_info["size"]["y"])
    color = pygame.Color(enemy_info["color"]["r"],
                         enemy_info["color"]["g"],
                         enemy_info["color"]["b"])
    vel_max = enemy_info["velocity_max"]
    vel_min = enemy_info["velocity_min"]
    vel_range = random.randrange(vel_min, vel_max)
    velocity = pygame.Vector2(random.choice([-vel_range, vel_range]),
                              random.choice([-vel_range, vel_range]))
    enemy_entity = create_square(world, size, pos, velocity, color)
    world.add_component(enemy_entity, CTagEnemy())
    return enemy_entity


def create_player(world:esper.World) -> int:
    player_entity = create_square(world, 
                                  size=pygame.Vector2(25, 25), 
                                  pos=pygame.Vector2(320-12.5, 180-12.5),
                                  vel=pygame.Vector2(0,0),
                                  col=pygame.Color(255,255,255))
    world.add_component(player_entity, CTagPlayer())
    return player_entity


def create_enemy_spawner(world:esper.World, level_data:dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity,
                        CEnemySpawner(level_data["enemy_spawn_events"]))
    
def create_player_bullet(world:esper.World, 
                         player_pos:pygame.Vector2,
                         mouse_pos:pygame.Vector2,
                         bullet_data:dict):
    vel = (mouse_pos - player_pos)
    vel = vel.normalize() * bullet_data["speed"]
    pos = pygame.Vector2(player_pos.x, player_pos.y)
    bullet_entity = create_square(world, 
                                  size=pygame.Vector2(bullet_data["size"]["w"],
                                                      bullet_data["size"]["h"]),
                                  pos=pos,
                                  vel=vel,
                                  col= pygame.Color(bullet_data["color"]["r"],
                                                    bullet_data["color"]["g"],
                                                    bullet_data["color"]["b"]))
    world.add_component(bullet_entity, CTagBullet())

def create_player_input(world:esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()
    world.add_component(input_left, 
                                    CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right, 
                                    CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    world.add_component(input_up, 
                                    CInputCommand("PLAYER_UP", pygame.K_UP))
    world.add_component(input_down, 
                                    CInputCommand("PLAYER_DOWN", pygame.K_DOWN))
    
    input_mouse_left_down = world.create_entity()
    world.add_component(input_mouse_left_down,
                                    CInputCommand("FIRE", pygame.BUTTON_LEFT))
