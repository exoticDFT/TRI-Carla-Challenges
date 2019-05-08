# Import modules
import carla

import random
import time

# modules
def create_client(host='127.0.0.1', port=2000, timeout=3.0):
    '''Create a Carla client to be used in a Carla runtime script'''
    client = carla.Client(host, port)
    client.set_timeout(timeout)

    return client


def create_random_blueprint(blueprints):
    blueprint = random.choice(blueprints)

    if blueprint.has_attribute('color'):
        color = random.choice(
            blueprint.get_attribute('color').recommended_values
        )
        blueprint.set_attribute('color', color)

    blueprint.set_attribute('role_name', 'autopilot')

    return blueprint


def is_actor_in_range(
    actor,
    origin=carla.Location(0.0, 0.0, 0.0),
    max_distance=100.0,
    verbose=False
):
    dist_from_origin = actor.get_location().distance(origin)
    if verbose:
        print("Actor", actor.id, "is", dist_from_origin, "meters away.")

    if dist_from_origin < max_distance:
        return True
    else:
        return False


def remove_distant_actors(
    world,
    location=carla.Location(0, 0, 0),
    max_distance=100.0,
    actor_filter='vehicle.*',
    verbose=False
):
    to_remove = [
        actor
        for actor in world.get_actors().filter(actor_filter)
        if not is_actor_in_range(
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


def sleep_random_time(start=2.0, end=6.0, verbose=False):
    sleep_time = random.uniform(start, end)

    if verbose:
        print('Sleeping for', sleep_time, 'seconds.')

    time.sleep(sleep_time)


def spawn_actor(world, blueprints, location, verbose=False):
    blueprint = create_random_blueprint(blueprints)
    actor = world.try_spawn_actor(blueprint, location)

    if actor and "vehicle" in actor.type_id:
        actor.set_autopilot(True)

        if verbose:
            print("Spawning vehicle")
            print("   Id:", actor.id)
            print("   Type Id:", actor.type_id)

    return actor