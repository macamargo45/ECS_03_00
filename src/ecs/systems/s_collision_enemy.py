import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_collision_enemy(world:esper.World, player_entity:int):
    c_pl_s = world.component_for_entity(player_entity, CSurface)
    c_pl_tr = world.component_for_entity(player_entity, CTransform)
    pl_rect = c_pl_s.surf.get_rect(topleft=c_pl_tr.pos)

    bullet_components = world.get_components(CTagBullet, CSurface, CTransform)
    enemy_components = world.get_components(CTagEnemy, CSurface, CTransform)
    for ene_entity, (_, c_ene_s, c_ene_tr) in enemy_components:
        ene_rect = c_ene_s.surf.get_rect(topleft=c_ene_tr.pos)
        if ene_rect.colliderect(pl_rect):
            c_pl_tr.pos.x = 320 - 12.5
            c_pl_tr.pos.y = 180 - 12.5
            world.delete_entity(ene_entity)

        for bullet_entity,  (_, c_bull_s, c_bull_tr) in bullet_components:
            bull_rect = c_bull_s.surf.get_rect(topleft=c_bull_tr.pos)
            if ene_rect.colliderect(bull_rect):
                world.delete_entity(ene_entity)
                world.delete_entity(bullet_entity)

        