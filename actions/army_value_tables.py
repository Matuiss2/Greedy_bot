from sc2 import Race
from sc2.constants import (
    ADEPT,
    ARCHON,
    BANSHEE,
    BATTLECRUISER,
    CARRIER,
    CYCLONE,
    COLOSSUS,
    DARKTEMPLAR,
    DISRUPTOR,
    GHOST,
    HELLION,
    HELLIONTANK,
    HYDRALISK,
    HIGHTEMPLAR,
    IMMORTAL,
    LIBERATOR,
    MARAUDER,
    MARINE,
    MEDIVAC,
    MOTHERSHIP,
    ORACLE,
    PHOENIX,
    PHOTONCANNON,
    PROBE,
    REAPER,
    SCV,
    SIEGETANK,
    SIEGETANKSIEGED,
    STALKER,
    SENTRY,
    TEMPEST,
    THOR,
    VIKINGASSAULT,
    VIKINGFIGHTER,
    VOIDRAY,
    ZEALOT,
    ZERGLING,
)


def general_calculation(table, targets):
    total = 0
    for enemy in targets:
        total += table[enemy.type_id]
    return total


class EnemyArmyValue:
    massive_counter = 4
    counter = 3
    advantage = 2
    normal = 1
    countered = 0.5
    massive_countered = 0.25
    worker = 0.1

    def protoss_value_for_zergling(self, combined_enemies):
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
        }
        return general_calculation(protoss_as_hydralisks_table, combined_enemies)

    def protoss_value_for_ultralisks(self, combined_enemies):
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

    def terran_value_for_zergling(self, combined_enemies):
        terran_as_zergling_table = {
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
        terran_as_hydralisk_table = {
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
        terran_as_ultralisk_table = {
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

    def enemy_value(self, unit, target_group, hydra_targect_group):
        local_controller = self.ai
        if local_controller.enemy_race == Race.Protoss:
            if unit.type_id == ZERGLING:
                return self.protoss_value_for_zergling(target_group)
            if unit.type_id == HYDRALISK:
                return self.protoss_value_for_hydralisks(hydra_targect_group)
            return self.protoss_value_for_ultralisks(target_group)
        if local_controller.enemy_race == Race.Terran:
            if unit.type_id == ZERGLING:
                return self.terran_value_for_zergling(target_group)
            if unit.type_id == HYDRALISK:
                return self.terran_value_for_hydralisks(hydra_targect_group)
            return self.terran_value_for_ultralisks(target_group)
