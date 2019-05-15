#!/bin/env/python

# Import modules
import util.carla_common as cc

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


def spawn_traffic_circle_agents(max_agents, world, verbose=False):
    '''
    Continuously spawns agents around the traffic circle in Town03.

    Parameters
    ----------
    max_agents : int
        The maximum number of agents allowed in the scenario at any given time.
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

    while True:
        num_agents = len(world.get_actors().filter('vehicle.*'))

        if num_agents < max_agents:
            cc.spawn_actor(
                world,
                blueprints,
                spawn_points[random.choice(sp_indices)],
                verbose
            )
            cc.sleep_random_time(verbose=verbose)


def remove_non_traffic_circle_agents(world, verbose=False):
    '''
    Monitors the Carla world and actively removes any agents that have
    wondered too far away from the traffic circle in Town03.

    Parameters
    ----------
    world : carla.World
        The Carla world in which to remove actors.
    verbose : bool, optional
        Used to determine whether some information should be displayed.
    '''
    circle_center = carla.Location(0, 0, 0) # map/circle center
    dist_from_center = 100.0 # 100 meters from traffic circle center

    while True:
        cc.remove_distant_actors(
            world,
            circle_center,
            dist_from_center,
            'vehicle.*',
            verbose
        )

        if verbose:
            print('Sleeping for 5.0 seconds.')
            
        time.sleep(5.0)


def event_4(args):
    '''
    Creates a scenario for the TRI Carla Challenge #4.

    Parameters
    ----------
    args : list
        A list of arguments used for the scenario generation.
    '''
    # Connect to the Carla server
    client = cc.create_client(args.host, args.port, args.timeout)
        
    # Use provided seed or system time if none is provided
    random.seed(a=args.seed)

    try:
        world = client.get_world()
        
        spawn_traffic_circle_agents(10, world, True)
        remove_non_traffic_circle_agents(world, True)

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