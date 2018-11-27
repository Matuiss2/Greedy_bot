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
)


def general_calculation(table, combined_enemies):
    total = 0
    for enemy in combined_enemies:
        total += table[enemy.type_id]
    return total


class EnemyArmyValue:
    def __init__(self):
        self.massive_counter = 4
        self.counter = 3
        self.advantage = 2
        self.normal = 1
        self.countered = 0.5
        self.massive_countered = 0.25
        self.worker = 0.1

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
