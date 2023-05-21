import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_player_movement(world:esper.World):
    query = world.get_components(CTagPlayer, CTransform)
    for _, (_, c_tr) in query:
        c_tr.pos.x = max(min(c_tr.pos.x, 226), 20)