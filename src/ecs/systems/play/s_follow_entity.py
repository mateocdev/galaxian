import esper

from src.ecs.components.c_follow_entity import CFollowEntity
from src.ecs.components.c_transform import CTransform

def system_follow_entity(world:esper.World):
    query = world.get_components(CTransform, CFollowEntity)
    for _, (c_t, c_f) in query:
        if not world.entity_exists(c_f.entity_to_follow_in):
            continue
        c_f_tr = world.try_component(c_f.entity_to_follow_in, CTransform)
        if c_f_tr is not None:
            c_t.pos.x = c_f_tr.pos.x + c_f.offset.x
            c_t.pos.y = c_f_tr.pos.y + c_f.offset.y