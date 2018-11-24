"""Everything related to building logic for the extractors goes here"""
from sc2.constants import EXTRACTOR


class BuildExtractor:
    """Can be improved, the ratio mineral-vespene still sightly off"""

    def __init__(self, ai):
        self.ai = ai
        self.drone = None
        self.geyser = None

    async def should_handle(self, iteration):
        """Couldn't find another way to build the geysers its way to inefficient,
         still trying to find the optimal number"""
        local_controller = self.ai
        finished_bases = local_controller.townhalls.ready
        if (local_controller.vespene * 1.25 > local_controller.minerals) or (
            not (finished_bases and local_controller.can_afford(EXTRACTOR))
        ):
            return False
        gas = local_controller.extractors
        gas_amount = len(gas)
        vgs = local_controller.state.vespene_geyser.closer_than(10, finished_bases.random)
        for geyser in vgs:
            self.drone = local_controller.select_build_worker(geyser.position)
            if not self.drone or local_controller.already_pending(EXTRACTOR):
                return False
            self.geyser = geyser
            if (not gas and local_controller.pools) or (gas_amount < 3 <= len(local_controller.townhalls)):
                return True
            return (
                (local_controller.time > 900 or local_controller.spires)
                and gas_amount < 11
                or (local_controller.hydradens and gas_amount < 7)
            )

    async def handle(self, iteration):
        """Just finish the action of building the extractor"""
        self.ai.add_action(self.drone.build(EXTRACTOR, self.geyser))
        return True
