#!/bin/env/python
 
import Event4
import util.carla_common
import util.world

import time

def main():
    client = util.carla_common.create_client()

    world = client.get_world()
    for actor in world.get_actors().filter('vehicle.*'):
        actor.destroy()

main()