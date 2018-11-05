"""Everything related to the logic for blocking expansions"""
from sc2.constants import BURROW, BURROWDOWN_ZERGLING


class BlockExpansions:
    """Needs few improvements like refill the force in case of failing until it succeeds(for a while at least)"""

    def __init__(self, ai):
        self.ai = ai

    async def should_handle(self, iteration):
        """Requirements for handle"""
        local_controller = self.ai
        zerglings = local_controller.zerglings.idle
        return (
            zerglings
            and not local_controller.burrowed_lings
            and len(zerglings) >= 6
            and local_controller.already_pending_upgrade(BURROW) == 1
        )

    async def handle(self, iteration):
        """Take the 6 'safest' zerglings and send them to the closest enemy expansion locations to burrow"""
        local_controller = self.ai
        zerglings = local_controller.zerglings.idle
        local_controller.burrowed_lings = [
            unit.tag for unit in zerglings.sorted_by_distance_to(local_controller.ordered_expansions[1])[:6]
        ]
        for list_index, zergling in enumerate(zerglings.tags_in(local_controller.burrowed_lings)):
            location = local_controller.ordered_expansions[-list_index - 1]

            # are we allowed to query into the dark?
            # if await local_controller.can_place(HATCHERY, location):

            local_controller.add_action(zergling.move(location))
            local_controller.add_action(zergling(BURROWDOWN_ZERGLING, queue=True))
            # print("burrowed", zergling.tag, location)

            # else:
            #     local_controller.burrowed_lings.remove(zergling.tag)
