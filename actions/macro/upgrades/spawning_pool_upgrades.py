"""Upgrading zerglings atk-speed and speed"""
from sc2.constants import AbilityId, UpgradeId


class SpawningPoolUpgrades:
    """Ok for now"""

    def __init__(self, main):
        self.main = main
        self.selected_research = None

    async def should_handle(self):
        """Requirements to upgrade stuff from pools"""
        if self.main.can_upgrade(
            UpgradeId.ZERGLINGMOVEMENTSPEED, AbilityId.RESEARCH_ZERGLINGMETABOLICBOOST, self.main.settled_pool.idle
        ):
            self.selected_research = AbilityId.RESEARCH_ZERGLINGMETABOLICBOOST
            return True
        if (
            self.main.can_upgrade(
                UpgradeId.ZERGLINGATTACKSPEED, AbilityId.RESEARCH_ZERGLINGADRENALGLANDS, self.main.settled_pool.idle
            )
            and self.main.hives
        ):
            self.selected_research = AbilityId.RESEARCH_ZERGLINGADRENALGLANDS
            return True

    async def handle(self):
        """Execute the action of upgrading zergling atk-speed and speed"""
        self.main.add_action(self.main.settled_pool.idle.first(self.selected_research))
