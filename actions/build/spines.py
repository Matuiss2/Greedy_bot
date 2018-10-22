"""Everything related to building logic for the spines goes here"""
from sc2.constants import SPINECRAWLER


class BuildSpines:
    """New placement untested"""

    def __init__(self, ai):
        self.ai = ai
        self.lairs = None

    async def should_handle(self, iteration):
        """Requirements to run handle"""
        local_controller = self.ai
        if not local_controller.pools.ready or not local_controller.townhalls:
            return False

        return (
            local_controller.close_enemy_production
            and len(local_controller.spines) < 4
            and local_controller.already_pending(SPINECRAWLER) < 2
        ) or (
            local_controller.spores.ready
            and not local_controller.spines
            and not local_controller.already_pending(SPINECRAWLER)
            and not local_controller.close_enemy_production
        )

    async def handle(self, iteration):
        """Build the spines on the first base near the ramp in case there is a proxy"""
        local_controller = self.ai
        map_center = local_controller._game_info.map_center
        if local_controller.spores.ready:
            spore_position = local_controller.spores.ready.furthest_to(map_center).position
            await local_controller.build(SPINECRAWLER, near=spore_position)
            return True
        else:
            await local_controller.build(
                SPINECRAWLER,
                near=local_controller.townhalls.furthest_to(map_center).position.towards(
                    local_controller.main_base_ramp.depot_in_middle, 14
                ),
            )
            return True
