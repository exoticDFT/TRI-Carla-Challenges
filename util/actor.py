import carla

import random

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


def in_range(
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