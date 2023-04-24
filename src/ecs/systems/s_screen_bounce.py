

import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_screen_bounce(world: esper.World, screen: pygame.Surface):
    screen_rect = screen.get_rect()
    enemies = world.get_components(CTransform, CVelocity, CSurface, CTagEnemy)

    for entity, (transform, velocity, surface, enemy) in enemies:
        if enemy.enemy_type == "Hunter":
            continue

        surface_rect = surface.area.copy()
        surface_rect.topleft = transform.pos
        if surface_rect.left < 0:
            velocity.vel.x = abs(velocity.vel.x)
            surface_rect.left = 0
            transform.pos.x = surface_rect.left
        elif surface_rect.right > screen_rect.width:
            velocity.vel.x = -abs(velocity.vel.x)
            surface_rect.right = screen_rect.width
            transform.pos.x = surface_rect.right - surface_rect.width

        if surface_rect.top < 0:
            velocity.vel.y = abs(velocity.vel.y)
            surface_rect.top = 0
            transform.pos.y = surface_rect.top
        elif surface_rect.bottom > screen_rect.height:
            velocity.vel.y = -abs(velocity.vel.y)
            surface_rect.bottom = screen_rect.height
            transform.pos.y = surface_rect.bottom - surface_rect.height
