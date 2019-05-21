# Import modules
import carla

import random
import time

# modules
def create_client(host='127.0.0.1', port=2000, timeout=3.0):
    '''
    Creates a Carla client to be used in a Carla runtime script.

    Parameters
    ----------
    host : str, optional
        The string containing the host address.
    port : int, optional
        The port in which the client will connect.
    timeout : float, optional
        The time in which to wait for a response from the server.

    Returns
    -------
    carla.Client
        A Carla client that is connected to the provided server.
    '''
    client = carla.Client(host, port)
    client.set_timeout(timeout)

    return client


def create_random_blueprint(blueprints):
    '''
    Creates a random Carla actor blueprint based on some provided blueprint
    library.

    Parameters
    ----------
    blueprints : carla.BlueprintLibrary
        A set of Carla blueprint templates used for creating a blueprint.

    Returns
    -------
    carla.ActorBlueprint
        A Carla blueprint to be used for a Carla actor.
    '''
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
    '''
    Checks if a Carla actor is within a certain distance from a location.

    Parameters
    ----------
    actor : carla.Actor
        The Carla actor in which to check its distance
    origin : carla.Location, optional
        The origin location in which the actor's distance will be determined.
    max_distance : float, optional
        The maximum distance the actor is from the origin used to evaluate
        whether it is within the range.
    verbose : bool, optional
        Used to determine whether some information should be displayed.

    Returns
    -------
    bool
        True if actor is in the range, False otherwise.
    '''
    dist_from_origin = actor.get_location().distance(origin)

    if verbose:
        print("Actor", actor.id, "is", dist_from_origin, "meters away.")

    if dist_from_origin <= max_distance:
        return True
    else:
        return False


def sleep_random_time(start=2.0, end=6.0, verbose=False):
    '''
    Sleeps the thread for some random time between the provided range.

    Parameters:
    start : float
        The minimum time in which to sleep.
    end : float
        The maximum time in which to sleep.
    verbose : bool
        Used to determine whether some information should be displayed.
    '''
    sleep_time = random.uniform(start, end)

    if verbose:
        print('Sleeping for', sleep_time, 'seconds.')

    time.sleep(sleep_time)