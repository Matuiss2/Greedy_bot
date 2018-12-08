"""Upgrading ultras special armor"""
from sc2.constants import CHITINOUSPLATING, RESEARCH_CHITINOUSPLATING


class UpgradeChitinousPlating:
    """Ok for now"""

    def __init__(self, ai):
        self.ai = ai
        self.selected_caverns = None

    async def should_handle(self):
        """Requirements to run handle"""
        local_controller = self.ai
        self.selected_caverns = local_controller.caverns.idle
        return local_controller.can_upgrade(CHITINOUSPLATING, RESEARCH_CHITINOUSPLATING, self.selected_caverns)

    async def handle(self):
        """Execute the action of upgrading ultra armor"""
        self.ai.add_action(self.selected_caverns.first(RESEARCH_CHITINOUSPLATING))
        return True
