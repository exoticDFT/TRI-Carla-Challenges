import util.carla_common

import carla

class Base:
    def __init__(
        self,
        scene_name,
        map_name,
        world
    ):
        self.name = scene_name
        self.map = map_name
        self.actors = []
        self.ego_vehicle = None
        self.time_of_day = 0.0
        self.scene_time = 0.0
        self.world = world


    def add_actor(self, actor):
        self.actors.append(actor)


    def remove_actor(self, actor):
        try:
            self.actors.remove(actor)
            actor.destroy()

        except KeyError:
            print('Carla actor', actor.id, 'is not in the scene.')