#!/bin/env/python

# Import modules
import util.actor
import util.client
import util.carla_common as cc
import util.world

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
    '''
    The argument parser used for the TRI Carla Challenge Event 4 scenario.

    Returns
    -------
    list
        The list of parsed arguments to be used throughout the program.
    '''
    argparser = argparse.ArgumentParser(
        description='TRI Carla Challenge - Event 4',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='The ip address of the host server'
    )
    argparser.add_argument(
        '-n',
        '--num-agents',
        metavar='N',
        default=10,
        type=int,
        help='The maximum number of non-player agents in the scenario'
    )
    argparser.add_argument(
        '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port used for listening'
    )
    argparser.add_argument(
        '-s',
        '--seed',
        metavar='S',
        default=None,
        help='The random number seed used during scenario generation'
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


def spawn_traffic_circle_agents(max_agents, actors, world, verbose=False):
    '''
    Continuously spawns agents around the traffic circle in Town03.

    Parameters
    ----------
    max_agents : int
        The maximum number of agents allowed in the scenario at any given time.
    actors : list
        A list of actors that have been spawned into the Carla world
    world : carla.World
        The Carla world in which to spawn actors.
    verbose : bool, optional
        Used to determine whether some information should be displayed.
    '''
    blueprints = world.get_blueprint_library().filter('vehicle.*')

    spawn_points = world.get_map().get_spawn_points()
    sp_indices = [
        8, 112, 113, 120, 121, 122, 123, 210, 211, 218, 219, 229, 247, 248
    ]

    num_agents = len(actors)

    while num_agents < max_agents:
        actor = util.world.spawn_actor(
            world,
            blueprints,
            spawn_points[random.choice(sp_indices)],
            verbose
        )

        if actor:
            actors.append(actor)

        cc.sleep_random_time(verbose=verbose)
        num_agents = len(actors)


def remove_non_traffic_circle_agents(actors, verbose=False):
    '''
    Monitors the Carla scene and actively removes the agents that have
    wondered too far away from the traffic circle in Town03.

    Parameters
    ----------
    actors : list
        A list of actors that have been spawned into the Carla world
    verbose : bool, optional
        Used to determine whether some information should be displayed.
    '''
    circle_center = carla.Location(0, 0, 0) # map/circle center
    dist_from_center = 100.0 # 100 meters from traffic circle center

    if verbose:
        print("Number of agents:", len(actors))

    for actor in actors:
        if not util.actor.in_range(
            actor,
            circle_center,
            dist_from_center,
            verbose
        ):
            actor.destroy()
            actors.remove(actor)

    if verbose:
        print("Number of agents after removal:", len(actors))


def event_4(args):
    '''
    Creates a scenario for the TRI Carla Challenge #4.

    Parameters
    ----------
    args : list
        A list of arguments used for the scenario generation.
    '''
    # Connect to the Carla server
    client = util.client.create(args.host, args.port, args.timeout)
        
    # Use provided seed or system time if none is provided
    random.seed(a=args.seed)

    try:
        world = client.get_world()
        actors = []

        while True:
            spawn_traffic_circle_agents(args.num_agents, actors, world, True)
            remove_non_traffic_circle_agents(actors, True)

    finally:
        pass


# Define the main module
def main():
    '''
    The main function for the scenario generator.
    '''
    args = parse_arguments()
    event_4(args)


# Main execution
if __name__ == '__main__':
    main()