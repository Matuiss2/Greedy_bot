"""All data that are related to quantity of the stuff on our possession are here"""


class OurQuantityData:
    """This is the data container for all our stuff amounts"""

    def __init__(self):
        self.hydra_amount = self.zergling_amount = self.drone_amount = self.overlord_amount = self.base_amount = None
        self.ready_overlord_amount = self.ready_base_amount = None

    def initialize_building_amounts(self):
        """Defines the amount of buildings on our possession separating by type"""
        self.base_amount = len(self.townhalls)

    def initialize_unit_amounts(self):
        """Defines the amount of units on our possession separating by type"""
        self.hydra_amount = len(self.hydras)
        self.zergling_amount = len(self.zerglings)
        self.drone_amount = len(self.drones)
        self.overlord_amount = len(self.overlords)

    def initialize_completed_amounts(self):
        """Defines the amount of units and buildings that are finished on our possession separating by type"""
        self.ready_overlord_amount = len(self.overlords.ready)
        self.ready_base_amount = len(self.townhalls.ready)