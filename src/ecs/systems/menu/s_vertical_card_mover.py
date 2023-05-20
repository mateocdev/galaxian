import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_vertical_card import CVerticalCard
from src.ecs.components.c_velocity import CVelocity

def system_vertical_card_mover(world:esper.World):
    query = world.get_components(CTransform, CVelocity, CVerticalCard)
    for ent, (c_tr, c_v, c_vc) in query:
        if not c_vc.started:
            c_vc.started = True
            c_tr.pos.y = c_vc.target_start_y
        else:
            c_v.vel.y = c_vc.speed
            if c_tr.pos.y <= c_vc.target_end_y:
                c_tr.pos.y = c_vc.target_end_y
                c_v.vel.y = 0
                world.remove_component(ent, CVerticalCard)