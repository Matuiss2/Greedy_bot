"""Upgrades made by evolution chambers"""
from sc2.constants import (
    RESEARCH_ZERGGROUNDARMORLEVEL1,
    RESEARCH_ZERGGROUNDARMORLEVEL2,
    RESEARCH_ZERGGROUNDARMORLEVEL3,
    RESEARCH_ZERGMELEEWEAPONSLEVEL1,
    RESEARCH_ZERGMELEEWEAPONSLEVEL2,
    RESEARCH_ZERGMELEEWEAPONSLEVEL3,
    RESEARCH_ZERGMISSILEWEAPONSLEVEL1,
    RESEARCH_ZERGMISSILEWEAPONSLEVEL2,
    RESEARCH_ZERGMISSILEWEAPONSLEVEL3,
)


class UpgradeEvochamber:
    """Ok for now"""

    def __init__(self, ai):
        self.ai = ai
        self.selected_evos = None
        self.upgrades_added = False
        self.upgrade_list = [
            RESEARCH_ZERGMELEEWEAPONSLEVEL1,
            RESEARCH_ZERGMELEEWEAPONSLEVEL2,
            RESEARCH_ZERGMELEEWEAPONSLEVEL3,
            RESEARCH_ZERGGROUNDARMORLEVEL1,
            RESEARCH_ZERGGROUNDARMORLEVEL2,
            RESEARCH_ZERGGROUNDARMORLEVEL3,
        ]
        self.ranged_upgrades = {
            RESEARCH_ZERGMISSILEWEAPONSLEVEL1,
            RESEARCH_ZERGMISSILEWEAPONSLEVEL2,
            RESEARCH_ZERGMISSILEWEAPONSLEVEL3,
        }

    async def should_handle(self, iteration):
        """Requirements to run handle"""
        self.selected_evos = self.ai.evochambers.ready.idle
        return self.selected_evos

    async def handle(self, iteration):
        """Execute the action of upgrading armor, melee and ranged attacks"""
        local_controller = self.ai
        action = local_controller.add_action
        if local_controller.hydradens and not self.upgrades_added:
            self.upgrades_added = True
            self.upgrade_list.extend(self.ranged_upgrades)
        for evo in self.selected_evos:
            for upgrade in await local_controller.get_available_abilities(evo):
                if upgrade in self.upgrade_list and local_controller.can_afford(upgrade):
                    action(evo(upgrade))
                    return True
        return True
