"""Everything related to building logic for the extractors goes here"""
from sc2.constants import UnitTypeId


class ExtractorConstruction:
    """Can probably be improved,
    but I think the problem is more on the vespene collection than the extractor building"""

    def __init__(self, main):
        self.main = main

    async def should_handle(self):
        """Couldn't find another way to build the geysers its heavily based on Burny's approach,
         still trying to find the optimal number"""
        if (
            self.main.vespene > self.main.minerals
            or not self.main.building_requirement(UnitTypeId.EXTRACTOR, self.main.ready_bases, one_at_time=True)
            or len(self.main.extractors) >= 10
        ):
            return False
        if not self.main.hives and len(self.main.extractors) >= 6:
            return False
        if (
            not self.main.extractors
            and self.main.pools
            or len(self.main.extractors) < 3 <= self.main.ready_base_amount
            or self.main.ready_base_amount > 3
        ):
            return True

    async def handle(self):
        """Just finish the action of building the extractor"""
        for geyser in self.main.state.vespene_geyser.closer_than(10, self.main.ready_bases.random):
            drone = self.main.select_build_worker(geyser.position)
            if drone:
                self.main.add_action(drone.build(UnitTypeId.EXTRACTOR, geyser))