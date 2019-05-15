import carla

def draw_spawn_points(world, timeout=-1.0):
    '''
    Draws all the available spawn points in the current Carla world.

    Parameters
    ----------
    world : carla.World
        The Carla world in which to draw the spawn point indices.
    timeout : float, optional
        The total number of seconds in which to keep the labels in the 
        environment. (Default is -1.0, which leaves the label in the 
        environment indefinitely.)
    '''
    map = world.get_map()
    spawn_points = map.get_spawn_points()

    for num, spawn_point in enumerate(spawn_points):
        world.debug.draw_string(
            spawn_point.location,
            str(num),
            life_time=timeout
        )