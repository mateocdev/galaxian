import esper
from src.ecs.components.c_enemy_fleet import CEnemyFleet
from src.ecs.components.c_enemy_state import CEnemyState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_enemy_movement(world:esper.World, delta_time:float):
    left_most_x = None
    left_most_x_tr = None
    right_most_x = None
    right_most_x_tr = None
    query = world.get_components(CEnemyState, CTagEnemy, CTransform)
    for _, (c_st, _, c_t) in query:
        if left_most_x is None or c_st.fold_pos.x < left_most_x:
            left_most_x = c_st.fold_pos.x
            left_most_x_tr = c_t
        if right_most_x is None or c_st.fold_pos.x > right_most_x:
            right_most_x = c_st.fold_pos.x
            right_most_x_tr = c_t
    
    if left_most_x is None and right_most_x is None:
        query = world.get_component(CEnemyFleet)
        for _, c_sqd in query:
            c_sqd.dir = 1
            dir = c_sqd.dir
        return
    
    dir, vel = _get_fleet_direction(world)
    if left_most_x < 20 or right_most_x > 226:
        if left_most_x < 20:
            dir = _change_fleet_direction(world)
            left_most_x_tr.pos.x = 20
        elif right_most_x > 226:
            dir = _change_fleet_direction(world)
            right_most_x_tr.pos.x = 226

    query = world.get_components(CEnemyState, CTagEnemy)
    for _, (c_st, _) in query:
        c_st.fold_pos.x += dir * vel * delta_time

def _get_fleet_direction(world:esper.World) -> int:
    query = world.get_component(CEnemyFleet)
    for _, c_sqd in query:
        return c_sqd.dir, c_sqd.dir_vel

def _change_fleet_direction(world:esper.World) -> int:
    dir = 1
    query = world.get_component(CEnemyFleet)
    for _, c_sqd in query:
        c_sqd.dir *= -1
        dir = c_sqd.dir
    return dir