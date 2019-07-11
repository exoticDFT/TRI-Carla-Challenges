import util.actor

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
        if not util.actor.in_range(
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


def spawn_actor(world, blueprints, transform, verbose=False):
    '''
    Tries to spawn an actor in the Carla world.

    Parameters:
    world : carla.World
        The Carla world in which to spawn actors.
    blueprints : carla.BlueprintLibrary
        A set of Carla blueprint templates used for creating a blueprint.
    transform : carla.Transform
        The transform (pose) used spawn the actor. Usually determined from 
        carla.Map.get_spawn_points().
    verbose : bool, optional
        Used to determine whether some information should be displayed.
     
    Returns
    -------
    carla.Actor
        A Carla actor if Carla world was able to spawn an actor in the
        provided transform, otherwise None.
    '''
    blueprint = util.actor.create_random_blueprint(blueprints)
    actor = world.try_spawn_actor(blueprint, transform)

    if actor:
        if "vehicle" in actor.type_id:
            actor.set_autopilot(True)

        if verbose:
            print("Spawning actor")
            print("   Id:", actor.id)
            print("   Type Id:", actor.type_id)
            print("   Transform:", transform)

    return actor