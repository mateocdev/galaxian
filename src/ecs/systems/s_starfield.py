import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_star import CTagStar


def system_starfield(world: esper.World, dt: float):
    query = world.get_components(CTransform, CVelocity, CTagStar)
    for _, (c_tr, c_vel, _) in query:
        c_tr.pos += c_vel.vel * dt
        if c_tr.pos.y > 240:
            c_tr.pos.y = 0
