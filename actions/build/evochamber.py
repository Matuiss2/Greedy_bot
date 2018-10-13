"""Everything related to building logic for the evolution chamber goes here"""
from sc2.constants import EVOLUTIONCHAMBER


class BuildEvochamber:
    """Ok for now"""

    def __init__(self, ai):
        self.ai = ai

    async def should_handle(self, iteration):
        """Builds the evolution chambers, placement can maybe be improved(far from priority),
        also there is some occasional bug that prevents both to be built at the same time,
        probably related to placement"""
        pool = self.ai.pools
        evochamber = self.ai.evochambers
        if (
            pool.ready
            and self.ai.can_afford(EVOLUTIONCHAMBER)
            and len(self.ai.townhalls) >= 3
            and len(evochamber) + self.ai.already_pending(EVOLUTIONCHAMBER) < 2
        ):
            return True
        return False

    async def handle(self, iteration):
        """Build it behind the mineral line if there is space, if not uses later placement"""
        position = await self.ai.get_production_position()
        if position:
            await self.ai.build(EVOLUTIONCHAMBER, position)
            return True

        furthest_base = self.ai.townhalls.furthest_to(self.ai.game_info.map_center)
        second_base = (self.ai.townhalls - {furthest_base}).closest_to(furthest_base)
        await self.ai.build(
                EVOLUTIONCHAMBER, second_base.position.towards_with_random_angle(self.ai.game_info.map_center, -14)
            )
        return True
