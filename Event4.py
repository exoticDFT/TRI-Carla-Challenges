#!/bin/env/python

# Import modules
import carla

try:
    import pygame
except ImportError:
    raise RuntimeError(
        'Cannot import pygame. Please make sure the pygame package is installed.'
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

        blueprint = create_blueprint(blueprints)
        spawned_agents = []

        for i in sp_indices:
            actor = world.try_spawn_actor(blueprint, spawn_points[i])

            if actor:
                print("Spawning actor", i, "with id:", actor.id)

            spawned_agents.append(actor)
            time.sleep(4.0)

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


def create_carla_client(host, port, timeout):
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