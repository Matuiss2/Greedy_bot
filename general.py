"""Everything that cannot be grouped yet goes here"""
from sc2.constants import (
    CANCEL,
    CANCEL_MORPHHIVE,
    CANCEL_MORPHLAIR,
    CANCEL_MORPHOVERSEER,
    HATCHERY,
    HIVE,
    INFESTATIONPIT,
    LAIR,
    MORPH_OVERSEER,
    OVERLORD,
    OVERLORDCOCOON,
    OVERSEER,
    UPGRADETOHIVE_HIVE,
    UPGRADETOLAIR_LAIR,
)


class extra_things:
    def __init__(self):
        self.location_index = 0

    def cancel_attacked_hatcheries(self):
        """find the hatcheries that are building, and have low health and cancel then,
        can be better, its easy to burst 400 hp, will look into that later,
         checking how fast the hp is going down might be a good idea"""
        if self.close_enemy_production and self.time < 300:
            for building in self.units(HATCHERY).filter(lambda x: 0.2 < x.build_progress < 1 and x.health < 400):
                self.actions.append(building(CANCEL))

    async def detection(self):
        """Morph the overseer"""
        lords = self.units(OVERLORD)
        if (
            (self.units(LAIR) or self.units(HIVE))
            and self.can_afford(OVERSEER)
            and lords
            and not self.units(OVERSEER)
            and not any([await self.is_morphing(h) for h in self.units(OVERLORDCOCOON)])
        ):
            self.actions.append(lords.random(MORPH_OVERSEER))

    async def is_morphing(self, homecity):
        """Check if a base or overlord is morphing, good enough for now"""
        abilities = await self.get_available_abilities(homecity)
        morphing_upgrades = (CANCEL_MORPHLAIR, CANCEL_MORPHHIVE, CANCEL_MORPHOVERSEER)
        for morph in morphing_upgrades:
            if morph in abilities:
                return True
        return False

    async def morphing_townhalls(self):
        """Works well, can definitely be optimized"""
        lair = self.units(LAIR)
        hive = self.units(HIVE)
        base = self.units(HATCHERY)
        # Hive
        if (
            self.units(INFESTATIONPIT).ready
            and not hive
            and self.can_afford(HIVE)
            and not any([await self.is_morphing(h) for h in lair])
            and lair.ready.idle
        ):
            self.actions.append(lair.ready.first(UPGRADETOHIVE_HIVE))
        # Lair
        if (
            len(self.townhalls) >= 3
            and self.can_afford(UPGRADETOLAIR_LAIR)
            and not (lair or hive)
            and not any([await self.is_morphing(h) for h in base])
            and base.ready.idle
        ):
            self.actions.append(base.ready.furthest_to(self._game_info.map_center)(UPGRADETOLAIR_LAIR))
