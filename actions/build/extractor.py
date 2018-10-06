from sc2.constants import (EXTRACTOR)

class BuildExtractor:

    def __init__(self, ai):
        self.ai = ai
        self.drone = None
        self.geyser = None

    async def should_handle(self, iteration):
        """Couldnt find another way to build the geysers its way to inefficient,
         also the logic can be improved, sometimes it over collect vespene sometime it under collect"""
        if not self.ai.vespene < self.ai.minerals * 2:
            return False
        if not (self.ai.townhalls.ready and self.ai.can_afford(EXTRACTOR)):
            return False

        gas = self.ai.extractors
        gas_amount = len(gas)  # so it calculate just once per step
        vgs = self.ai.state.vespene_geyser.closer_than(10, self.ai.townhalls.ready.random)
        for geyser in vgs:
            self.drone = self.ai.select_build_worker(geyser.position)
            if not self.drone:
                return False
            if not self.ai.already_pending(EXTRACTOR):
                if not gas and self.ai.pools:
                    self.geyser = geyser
                    return True
                if gas_amount == 1 and len(self.ai.townhalls) >= 3:
                    self.geyser = geyser
                    return True
            if self.ai.time > 960 and gas_amount < 10:
                self.geyser = geyser
                return True
            pit = self.ai.pits
            if pit and gas_amount + self.ai.already_pending(EXTRACTOR) < 8:
                return False

        return False

    async def handle(self, iteration):
        self.ai.actions.append(self.drone.build(EXTRACTOR, self.geyser))
        return True
