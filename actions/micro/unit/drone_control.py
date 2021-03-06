"""Everything related to scouting with drones goes here"""


class DroneControl:
    """Ok for now, maybe can be replaced later for zerglings"""

    def __init__(self, main):
        self.main = main
        self.scout = False

    async def should_handle(self):
        """Sends the scouting drone on the beginning"""
        return not self.scout

    async def handle(self):
        """It sends a drone to scout the map, for bases or proxies"""
        selected_drone = self.main.drones.random
        self.scout = True
        for point in self.main.ordered_expansions[1:6]:
            self.main.add_action(selected_drone.move(point, queue=True))
        for point in self.main.enemy_start_locations:
            self.main.add_action(selected_drone.move(point, queue=True))
