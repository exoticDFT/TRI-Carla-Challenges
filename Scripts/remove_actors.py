#!/bin/env/python
 
import Event4
import util.carla_common as cc

import time

def main():
    client = cc.create_client()

    world = client.get_world()

    while True:
        Event4.remove_non_traffic_circle_agents(world, verbose=True)
        print('Total actors remaining:', len(world.get_actors().filter('vehicle.*')))

main()