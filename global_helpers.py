"""Every helper for the bot goes here"""
from sc2.constants import UnitTypeId


class Globals:
    """Global wrappers"""

    def building_requirements(self, unit_type, requirement=True, one_at_time=False):
        """
        Global requirements for building every structure
        Parameters
        ----------
        unit_type: The only mandatory parameter, the unit type id to be built
        requirement: The basic requirement for the unit to be built
        one_at_time: If True, don't build it if there is another unit of the same type pending already

        Returns
        -------
        True if requirements gets met
        """
        if one_at_time and self.already_pending(unit_type):
            return False
        return requirement and self.can_afford(unit_type)

    def can_build_unique(self, unit_type, building, requirement=True):
        """
        Global requirements for building unique buildings
        Parameters
        ----------
        unit_type: The unit type id to be built
        building: This units list, to check if its empty
        requirement: The basic requirement for the unit to be built

        Returns
        -------
        True if requirements gets met
        """
        return (
            self.can_afford(unit_type)
            and not building
            and self.building_requirements(unit_type, requirement, one_at_time=True)
        )

    def can_train(self, unit_type, requirement=True, larva=True):
        """
        Global requirements for creating an unit, locks production so hive and ultra cavern gets built
        Parameters
        ----------
        unit_type: The unit type id to be trained
        requirement: The basic requirement for the unit to be trained
        larva: If False the unit doesn't need larva (only queen)

        Returns
        -------
        True if requirements gets met
        """
        if self.hives and not self.caverns:
            return False
        if self.pits.ready and not self.hives and not self.already_pending(UnitTypeId.HIVE):
            return False
        return (not larva or self.larvae) and self.can_afford(unit_type) and requirement

    def can_upgrade(self, upgrade, research, host_building):
        """
        Global requirements for upgrades
        Parameters
        ----------
        upgrade: The upgrade id to be researched
        research: The ability id to make the building research
        host_building: The building that is hosting the research

        Returns
        -------
        True if requirements gets met
        """
        return not self.already_pending_upgrade(upgrade) and self.can_afford(research) and host_building

    async def place_building(self, building):
        """Build it behind the mineral line if there is space"""
        position = await self.get_production_position()
        if not position:
            return None
        if any(enemy.distance_to(position) < 10 for enemy in self.enemies) and not self.close_enemy_production:
            return None
        selected_drone = self.select_build_worker(position)
        if selected_drone:
            self.add_action(selected_drone.build(building, position))
