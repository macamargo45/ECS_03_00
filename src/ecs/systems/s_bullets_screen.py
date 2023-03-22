import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet

def system_bullets_screen(world:esper.World, screen:pygame.Surface):
    scr_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagBullet)
    for bullet_entity, (c_t, c_s, _) in components:
        s_bullet_rect = c_s.surf.get_rect(topleft=c_t.pos)
        if not scr_rect.contains(s_bullet_rect):
            world.delete_entity(bullet_entity)