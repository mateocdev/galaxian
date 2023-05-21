import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_star import CTagStar


def system_starfield(world: esper.World,
                     dt: float):
    query = world.get_components(
        CTransform,
        CVelocity,
        CTagStar)
    for _, (c_t, c_v, _) in query:
        c_t.pos += c_v.vel * dt
        if c_t.pos.y > 600:
            c_t.pos.y = -10
