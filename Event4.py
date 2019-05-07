#!/bin/env/python

# Import modules
import carla

try:
    import pygame
except ImportError:
    raise RuntimeError(
        'Cannot import pygame. Please verify the pygame package is installed.'
    )

import argparse
import random
import time

# Modules
def parse_arguments():
    argparser = argparse.ArgumentParser(
        description='TRI Carla Challenge - Event 4',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    argparser.add_argument(
        '-s',
        '--seed',
        default=None,
        help='The random number seed used during scenario generation'
    )
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='The ip address of the host server'
    )
    argparser.add_argument(
        '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port used for listening'
    )
    argparser.add_argument(
        '-t',
        '--timeout',
        metavar='T',
        default=3.0,
        type=float,
        help='Timeout, in seconds, of the Carla client when contacting server'
    )

    args = argparser.parse_args()
    args.description = argparser.description

    return args


def spawn_vehicle(world, blueprints, location, verbose=False):
    blueprint = create_blueprint(blueprints)
    actor = world.try_spawn_actor(blueprint, location)

    if actor and "vehicle" in actor.type_id:
        actor.set_autopilot(True)

        if verbose:
            print("Spawning vehicle")
            print("   Id:", actor.id)
            print("   Type Id:", actor.type_id)

    return actor


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


def spawn_traffic_circle_agents(max_agents, world, verbose=False):
    blueprints = world.get_blueprint_library().filter('vehicle.*')

    spawn_points = world.get_map().get_spawn_points()
    sp_indices = [114, 115, 116, 117, 118, 126, 127]

    while True:
        num_agents = len(world.get_actors().filter('vehicle.*'))

        if num_agents < max_agents:
            spawn_vehicle(
                world,
                blueprints,
                spawn_points[random.choice(sp_indices)],
                verbose
            )
            sleep_random_time(verbose=verbose)


def remove_non_traffic_circle_agents(world, verbose=False):
    circle_center = carla.Location(0, 0, 0) # map/circle center
    dist_from_center = 100.0 # 100 meters from traffic circle center

    while True:
        remove_distant_actors(
            world,
            circle_center,
            dist_from_center,
            'vehicle.*',
            verbose
        )

        if verbose:
            print('Sleeping for 5.0 seconds.')
            
        time.sleep(5.0)


def sleep_random_time(start=2.0, end=6.0, verbose=False):
    sleep_time = random.uniform(start, end)

    if verbose:
        print('Sleeping for', sleep_time, 'seconds.')

    time.sleep(sleep_time)
    
    
def event_4(args):
    '''Create a scenario for the TRI Carla Challenge #4'''
    # Connect to the Carla server
    client = create_carla_client(args.host, args.port, args.timeout)

    try:
        world = client.get_world()
        blueprints = world.get_blueprint_library().filter('vehicle.*')

        spawn_points = world.get_map().get_spawn_points()
        sp_indices = [114, 115, 116, 117, 118, 126, 127]

        # Use provided seed or system time if none is provided
        random.seed(a=args.seed)

        for i in sp_indices:
            spawn_vehicle(world, blueprints, spawn_points[i], True)
            time.sleep(4.0)

        while time.time() < time.time() + 60*3:
            remove_distant_actors(world, verbose=True)
            time.sleep(5.0)

    finally:
        pass


def create_blueprint(blueprints):
    blueprint = random.choice(blueprints)

    if blueprint.has_attribute('color'):
        color = random.choice(
            blueprint.get_attribute('color').recommended_values
        )
        blueprint.set_attribute('color', color)

    blueprint.set_attribute('role_name', 'autopilot')

    return blueprint


def create_carla_client(
    host='127.0.0.1',
    port=2000,
    timeout=3.0
):
    '''Create a Carla client to be used in a Carla runtime script'''
    client = carla.Client(host, port)
    client.set_timeout(timeout)

    return client


# Define the main module
def main():
    args = parse_arguments()
    event_4(args)


# Main execution
if __name__ == '__main__':
    main()