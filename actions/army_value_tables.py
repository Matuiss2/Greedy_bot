"""Everything related to army value tables go here"""
from sc2 import Race
from sc2.constants import (
    ADEPT,
    ARCHON,
    BANELING,
    BANSHEE,
    BATTLECRUISER,
    BROODLING,
    BROODLORD,
    BUNKER,
    CARRIER,
    CYCLONE,
    COLOSSUS,
    CORRUPTOR,
    DARKTEMPLAR,
    DISRUPTOR,
    DRONE,
    GHOST,
    HELLION,
    HELLIONTANK,
    HYDRALISK,
    HIGHTEMPLAR,
    IMMORTAL,
    LARVA,
    INFESTEDTERRAN,
    INFESTEDTERRANSEGG,
    INFESTOR,
    LIBERATOR,
    LOCUSTMP,
    LOCUSTMPFLYING,
    LURKERMP,
    LURKERMPBURROWED,
    MARAUDER,
    MARINE,
    MEDIVAC,
    MOTHERSHIP,
    MUTALISK,
    ORACLE,
    OVERLORD,
    OVERSEER,
    PHOENIX,
    PHOTONCANNON,
    PROBE,
    QUEEN,
    RAVAGER,
    REAPER,
    ROACH,
    SCV,
    SENTRY,
    SIEGETANK,
    SIEGETANKSIEGED,
    SPINECRAWLER,
    STALKER,
    SWARMHOSTMP,
    TEMPEST,
    THOR,
    ULTRALISK,
    VIKINGASSAULT,
    VIKINGFIGHTER,
    VIPER,
    VOIDRAY,
    ZEALOT,
    ZERGLING,
)


def general_calculation(table, targets):
    """Returns the sum of all targets unit values, if the id is unknown, add it as value 1"""
    total = 0
    for enemy in targets:
        table.setdefault(enemy.type_id, 1)
        total += table[enemy.type_id]
    return total


class EnemyArmyValue:
    """Separate the enemy army values by unit and race"""
    massive_counter = 4
    counter = 3
    advantage = 2
    normal = 1
    countered = 0.5
    massive_countered = 0.25
    worker = 0.1

    def protoss_value_for_zerglings(self, combined_enemies):
        """Calculate the enemy army value for zerglings vs protoss"""
        protoss_as_zergling_table = {
            COLOSSUS: self.massive_counter,
            ADEPT: self.counter,
            ARCHON: self.counter,
            STALKER: self.normal,
            DARKTEMPLAR: self.normal,
            PHOTONCANNON: self.counter,
            ZEALOT: self.advantage,
            SENTRY: self.countered,
            PROBE: self.worker,
            HIGHTEMPLAR: self.countered,
            DISRUPTOR: self.counter,
            IMMORTAL: self.advantage,
        }
        return general_calculation(protoss_as_zergling_table, combined_enemies)

    def protoss_value_for_hydralisks(self, combined_enemies):
        """Calculate the enemy army value for hydralisks vs protoss"""
        protoss_as_hydralisks_table = {
            PHOENIX: self.countered,
            ORACLE: self.normal,
            COLOSSUS: self.counter,
            ADEPT: self.advantage,
            ARCHON: self.advantage,
            STALKER: self.normal,
            DARKTEMPLAR: self.countered,
            PHOTONCANNON: self.counter,
            ZEALOT: self.normal,
            SENTRY: self.massive_countered,
            PROBE: self.worker,
            HIGHTEMPLAR: self.countered,
            CARRIER: self.counter,
            DISRUPTOR: self.advantage,
            IMMORTAL: self.counter,
            TEMPEST: self.advantage,
            VOIDRAY: self.normal,
            MOTHERSHIP: self.counter,
        }
        return general_calculation(protoss_as_hydralisks_table, combined_enemies)

    def protoss_value_for_ultralisks(self, combined_enemies):
        """Calculate the enemy army value for ultralisks vs protoss"""
        protoss_as_ultralisks_table = {
            COLOSSUS: self.normal,
            ADEPT: self.countered,
            ARCHON: self.normal,
            STALKER: self.countered,
            DARKTEMPLAR: self.countered,
            PHOTONCANNON: self.normal,
            ZEALOT: self.countered,
            SENTRY: self.countered,
            PROBE: self.worker,
            HIGHTEMPLAR: self.massive_countered,
            DISRUPTOR: self.normal,
            IMMORTAL: self.counter,
        }
        return general_calculation(protoss_as_ultralisks_table, combined_enemies)

    def terran_value_for_zerglings(self, combined_enemies):
        """Calculate the enemy army value for zerglings vs terran"""
        terran_as_zergling_table = {
            BUNKER: self.counter,
            HELLION: self.advantage,
            HELLIONTANK: self.counter,
            CYCLONE: self.advantage,
            GHOST: self.advantage,
            MARAUDER: self.normal,
            MARINE: self.normal,
            REAPER: self.normal,
            SCV: self.worker,
            SIEGETANKSIEGED: self.counter,
            SIEGETANK: self.advantage,
            THOR: self.advantage,
            VIKINGASSAULT: self.normal,
        }
        return general_calculation(terran_as_zergling_table, combined_enemies)

    def terran_value_for_hydralisks(self, combined_enemies):
        """Calculate the enemy army value for hydralisks vs terran"""
        terran_as_hydralisk_table = {
            BUNKER: self.normal,
            HELLION: self.normal,
            HELLIONTANK: self.advantage,
            CYCLONE: self.normal,
            GHOST: self.normal,
            MARAUDER: self.advantage,
            MARINE: self.countered,
            REAPER: self.countered,
            SCV: self.worker,
            SIEGETANKSIEGED: self.massive_counter,
            SIEGETANK: self.advantage,
            THOR: self.advantage,
            VIKINGASSAULT: self.countered,
            BANSHEE: self.normal,
            BATTLECRUISER: self.counter,
            LIBERATOR: self.advantage,
            MEDIVAC: self.massive_countered,
            VIKINGFIGHTER: self.massive_countered,
        }
        return general_calculation(terran_as_hydralisk_table, combined_enemies)

    def terran_value_for_ultralisks(self, combined_enemies):
        """Calculate the enemy army value for ultralisks vs terran"""
        terran_as_ultralisk_table = {
            BUNKER: self.countered,
            HELLION: self.massive_countered,
            HELLIONTANK: self.countered,
            CYCLONE: self.normal,
            GHOST: self.normal,
            MARAUDER: self.advantage,
            MARINE: self.massive_countered,
            REAPER: self.countered,
            SCV: self.worker,
            SIEGETANKSIEGED: self.counter,
            SIEGETANK: self.normal,
            THOR: self.counter,
            VIKINGASSAULT: self.countered,
        }
        return general_calculation(terran_as_ultralisk_table, combined_enemies)

    def zerg_value_for_zerglings(self, combined_enemies):
        """Calculate the enemy army value for zerglings vs zerg"""
        zerg_as_zergling_table = {
            LARVA: 0,
            QUEEN: self.normal,
            ZERGLING: self.normal,
            BANELING: self.advantage,
            ROACH: self.advantage,
            RAVAGER: self.advantage,
            HYDRALISK: self.advantage,
            LURKERMP: self.advantage,
            DRONE: self.worker,
            LURKERMPBURROWED: self.massive_counter,
            INFESTOR: self.countered,
            INFESTEDTERRAN: self.normal,
            INFESTEDTERRANSEGG: self.massive_countered,
            SWARMHOSTMP: self.countered,
            LOCUSTMP: self.counter,
            ULTRALISK: self.massive_counter,
            SPINECRAWLER: self.advantage,
            BROODLING: self.normal,
        }
        return general_calculation(zerg_as_zergling_table, combined_enemies)

    def zerg_value_for_hydralisk(self, combined_enemies):
        """Calculate the enemy army value for hydralisks vs zerg"""
        zerg_as_hydralisk_table = {
            LARVA: 0,
            QUEEN: self.normal,
            ZERGLING: self.countered,
            BANELING: self.advantage,
            ROACH: self.normal,
            RAVAGER: self.advantage,
            HYDRALISK: self.normal,
            LURKERMP: self.normal,
            DRONE: self.worker,
            LURKERMPBURROWED: self.massive_counter,
            INFESTOR: self.countered,
            INFESTEDTERRAN: self.countered,
            INFESTEDTERRANSEGG: self.massive_countered,
            SWARMHOSTMP: self.massive_countered,
            LOCUSTMP: self.counter,
            ULTRALISK: self.massive_counter,
            SPINECRAWLER: self.normal,
            LOCUSTMPFLYING: self.countered,
            OVERLORD: 0,
            OVERSEER: 0,
            MUTALISK: self.normal,
            CORRUPTOR: 0,
            VIPER: self.countered,
            BROODLORD: self.counter,
            BROODLING: self.countered,
        }
        return general_calculation(zerg_as_hydralisk_table, combined_enemies)

    def zerg_value_for_ultralisks(self, combined_enemies):
        """Calculate the enemy army value for ultralisks vs zerg"""
        zerg_as_ultralisk_table = {
            LARVA: 0,
            QUEEN: self.countered,
            ZERGLING: self.massive_countered,
            BANELING: self.massive_countered,
            ROACH: self.normal,
            RAVAGER: self.normal,
            HYDRALISK: self.normal,
            LURKERMP: self.normal,
            DRONE: self.worker,
            LURKERMPBURROWED: self.counter,
            INFESTOR: self.countered,
            INFESTEDTERRAN: self.countered,
            INFESTEDTERRANSEGG: self.massive_countered,
            SWARMHOSTMP: self.massive_countered,
            LOCUSTMP: self.counter,
            ULTRALISK: self.normal,
            SPINECRAWLER: self.normal,
            BROODLING: self.countered,
        }
        return general_calculation(zerg_as_ultralisk_table, combined_enemies)

    def enemy_value(self, unit, target_group, hydra_target_group):
        """Chooses the right function to calculate returns the right value based on the situation"""
        local_controller = self.ai
        if local_controller.enemy_race == Race.Protoss:
            if unit.type_id == ZERGLING:
                return self.protoss_value_for_zerglings(target_group)
            if unit.type_id == HYDRALISK:
                return self.protoss_value_for_hydralisks(hydra_target_group)
            return self.protoss_value_for_ultralisks(target_group)
        if local_controller.enemy_race == Race.Terran:
            if unit.type_id == ZERGLING:
                return self.terran_value_for_zerglings(target_group)
            if unit.type_id == HYDRALISK:
                return self.terran_value_for_hydralisks(hydra_target_group)
            return self.terran_value_for_ultralisks(target_group)
        if unit.type_id == ZERGLING:
            return self.zerg_value_for_zerglings(target_group)
        if unit.type_id == HYDRALISK:
            return self.zerg_value_for_hydralisks(hydra_target_group)
        return self.zerg_value_for_ultralisks(target_group)
