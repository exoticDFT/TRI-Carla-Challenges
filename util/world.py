import util.carla_common

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


def remove_distant_actors(
    world,
    location=carla.Location(0, 0, 0),
    max_distance=100.0,
    actor_filter='vehicle.*',
    verbose=False
):
    '''
    Removes actors from the Carla world when outside a given area.

    Parameters:
    world : carla.World
        The Carla world in which to remove actors.
    location : carla.Location, optional
        The location used for determining the center of the area.
    max_distance : float, optional
        The maximum distance an actor can be from the location center.
    actor_filter : str, optional
        A string containing the filter to apply to the world's actor list.
        Only actors with this filter will be removed.
    verbose : bool, optional
        Used to determine whether some information should be displayed.
    '''
    to_remove = [
        actor
        for actor in world.get_actors().filter(actor_filter)
        if not util.carla_common.is_actor_in_range(
            actor, 
            location,
            max_distance,
            verbose
        )
    ]

    for actor in to_remove:
        actor.destroy()

        if verbose:
            print("Actor", actor.id, "removed from scenario.")

    if verbose:
        print(
            'Total actors remaining:',
            len(world.get_actors().filter('vehicle.*'))
        )